#!/usr/bin/env python3
"""Fetch selected user documentation from pinned SEAPATH repositories."""

from __future__ import annotations

import argparse
import fnmatch
import io
import json
import os
import posixpath
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path
from urllib.parse import quote, urlsplit
from urllib.error import URLError
from urllib.request import Request, urlopen

import yaml


ROOT = Path(__file__).resolve().parents[1]
SOURCE_CONFIG = ROOT / "docs" / "upstream-sources.json"


def fetch_source(repository: str, revision: str, path: str) -> str:
    url = f"https://raw.githubusercontent.com/{repository}/{revision}/{path}"
    request = Request(url, headers={"User-Agent": "seapath-docs-sync"})
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def fetch_tree(repository: str, revision: str) -> list[str]:
    url = f"https://api.github.com/repos/{repository}/git/trees/{revision}?recursive=1"
    request = Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "seapath-docs-sync",
        },
    )
    with urlopen(request, timeout=30) as response:
        tree = json.loads(response.read().decode("utf-8"))
    if tree.get("truncated"):
        raise RuntimeError(f"GitHub returned a truncated tree for {repository}@{revision}")
    return [entry["path"] for entry in tree["tree"] if entry.get("type") == "blob"]


def render_ansible_module(content: str) -> str:
    def section(name: str) -> str:
        match = re.search(
            rf"^{name}\s*=\s*r?\"\"\"(.*?)\"\"\"", content, re.MULTILINE | re.DOTALL
        )
        return match.group(1) if match else ""

    documentation = yaml.safe_load(section("DOCUMENTATION"))
    lines = [f"# `{documentation['module']}` Ansible module", ""]
    lines.extend([documentation.get("short_description", ""), ""])

    description = documentation.get("description", [])
    if isinstance(description, str):
        description = [description]
    lines.extend(description)
    lines.extend(["", "## Requirements", ""])
    for requirement in documentation.get("requirements", []):
        lines.append(f"- {requirement}")

    lines.extend(["", "## Parameters", ""])
    for name, option in documentation.get("options", {}).items():
        lines.extend([f"### `{name}`", ""])
        option_description = option.get("description", [])
        if isinstance(option_description, str):
            option_description = [option_description]
        lines.extend(
            re.sub(r"\b(?:C|I|M|O|U|V|L)\(([^)]*)\)", r"`\1`", item)
            for item in option_description
        )
        details = []
        if "type" in option:
            details.append(f"Type: `{option['type']}`")
        if option.get("required"):
            details.append("Required")
        if "default" in option:
            details.append(f"Default: `{option['default']}`")
        if "choices" in option:
            choices = ", ".join(f"`{choice}`" for choice in option["choices"])
            details.append(f"Choices: {choices}")
        if details:
            lines.append("; ".join(details) + ".")
        lines.append("")

    examples = section("EXAMPLES").strip()
    if examples:
        lines.extend(["## Examples", "", "```yaml", examples, "```", ""])

    returns = section("RETURN").strip()
    if returns:
        lines.extend(["## Return values", "", "```yaml", returns, "```", ""])
    return "\n".join(lines).strip()


def rewrite_relative_links(content: str, repository: str, revision: str, source_path: str) -> str:
    link_pattern = re.compile(r"(?P<open>!?\[[^\]]*\]\()(?P<target>[^)]+)(?P<close>\))")

    def rewrite(match: re.Match) -> str:
        target = match.group("target")
        stripped = target.strip()
        url, separator, title = stripped.partition(" ")
        if url.startswith(("https://", "http://", "mailto:", "#", "/", "data:")):
            return match.group(0)
        parsed_url = urlsplit(url)
        source_directory = posixpath.dirname(source_path)
        resolved = posixpath.normpath(
            posixpath.join(source_directory, parsed_url.path)
        )
        encoded_path = quote(resolved, safe="/!$&'()*+,;=:@-._~")
        github_path = "raw" if match.group("open").startswith("!") else "blob"
        replacement_url = (
            f"https://github.com/{repository}/{github_path}/{revision}/{encoded_path}"
            f"{('?' + parsed_url.query) if parsed_url.query else ''}"
            f"{('#' + parsed_url.fragment) if parsed_url.fragment else ''}"
        )
        replacement_target = replacement_url + (separator + title if separator else "")
        return match.group("open") + replacement_target + match.group("close")

    return link_pattern.sub(rewrite, content)


def extract_content(content: str, extractor: str | None) -> str:
    if extractor is None:
        return content.strip()

    if extractor == "ansible_module_docs":
        return render_ansible_module(content)

    raise ValueError(f"Unknown documentation extractor: {extractor}")


def sync_sources(config: dict) -> list[Path]:
    pending_writes: list[tuple[Path, str]] = []

    for source in config["sources"]:
        repository = source["repository"]
        revision = source["revision"]
        discovered_roles: list[tuple[Path, Path]] = []
        for file in source["files"]:
            path = file["path"]
            content = fetch_source(repository, revision, path)
            content = extract_content(content, file.get("extract"))
            if file.get("extract") != "ansible_module_docs":
                content = rewrite_relative_links(content, repository, revision, path)
            source_url = f"https://github.com/{repository}/blob/{revision}/{path}"
            header = (
                "<!-- Generated by scripts/sync_upstream_docs.py; do not edit. -->\n\n"
                f"> Source: [`{repository}/{path}`]({source_url}) "
                f"(commit `{revision}`).\n\n"
            )
            pending_writes.append((ROOT / file["output"], header + content + "\n"))

        for discovery in source.get("discover", []):
            paths = fetch_tree(repository, revision)
            role_paths = sorted(
                path
                for path in paths
                if fnmatch.fnmatchcase(path, discovery["pattern"])
            )
            output_dir = Path(discovery["output_dir"])
            for path in role_paths:
                relative_readme = Path(path).relative_to("roles")
                role_directory = relative_readme.parent
                output_path = (
                    output_dir
                    / role_directory.parent
                    / f"{role_directory.name}.md"
                )
                content = fetch_source(repository, revision, path).strip()
                content = rewrite_relative_links(content, repository, revision, path)
                source_url = f"https://github.com/{repository}/blob/{revision}/{path}"
                header = (
                    "<!-- Generated by scripts/sync_upstream_docs.py; do not edit. -->\n\n"
                    f"> Source: [`{repository}/{path}`]({source_url}) "
                    f"(commit `{revision}`).\n\n"
                )
                pending_writes.append((ROOT / output_path, header + content + "\n"))
                discovered_roles.append((role_directory, output_path))

            index_path = output_dir / "index.md"
            index_lines = [
                "<!-- Generated by scripts/sync_upstream_docs.py; do not edit. -->",
                "",
                "# Ansible collection roles",
                "",
                f"Role documentation synchronized from `{repository}` at commit `{revision}`.",
                "",
                "## Roles",
                "",
            ]
            for role_directory, output_path in discovered_roles:
                href = output_path.relative_to(output_dir).as_posix()
                index_lines.append(f"- [{role_directory.as_posix()}]({href})")
            pending_writes.append(
                (ROOT / index_path, "\n".join(index_lines) + "\n")
            )

    generated_root = ROOT / "docs" / "_generated" / "upstream"
    shutil.rmtree(generated_root, ignore_errors=True)
    written = []
    for destination, content in pending_writes:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")
        written.append(destination)
    return written


def build_vm_manager_sphinx(config: dict) -> None:
    source = next(
        item for item in config["sources"] if item["name"] == "vm_manager"
    )
    repository = source["repository"]
    revision = source["revision"]
    archive_url = f"https://codeload.github.com/{repository}/tar.gz/{revision}"
    request = Request(archive_url, headers={"User-Agent": "seapath-docs-sync"})
    with urlopen(request, timeout=60) as response:
        archive_bytes = response.read()

    with tempfile.TemporaryDirectory(prefix="seapath-vm-manager-docs-") as temporary:
        with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:gz") as archive:
            archive.extractall(path=temporary, filter="data")

        extracted_root = Path(temporary)
        source_root = next(
            path
            for path in extracted_root.iterdir()
            if path.is_dir() and (path / "docs" / "conf.py").is_file()
        )
        sphinx_source = source_root / "docs"
        sphinx_output = (
            ROOT / "docs" / "_generated" / "upstream" / "vm-manager" / "sphinx"
        )
        sphinx_output.mkdir(parents=True, exist_ok=True)

        environment = dict(os.environ)
        current_pythonpath = environment.get("PYTHONPATH")
        environment["PYTHONPATH"] = str(source_root) + (
            f":{current_pythonpath}" if current_pythonpath else ""
        )
        subprocess.run(
            [
                sys.executable,
                "-m",
                "sphinx",
                "-b",
                "html",
                "-E",
                "-a",
                str(sphinx_source),
                str(sphinx_output),
            ],
            cwd=sphinx_source,
            env=environment,
            check=True,
        )

    landing_page = sphinx_output.parent / "sphinx-documentation.md"
    landing_page.write_text(
        "\n".join(
            [
                "<!-- Generated by scripts/sync_upstream_docs.py; do not edit. -->",
                "",
                "# vm_manager Sphinx documentation",
                "",
                f"Built from [`{repository}`](https://github.com/{repository}/tree/{revision}/docs) at commit `{revision}`.",
                "",
                "The complete upstream Sphinx documentation is available here:",
                "",
                "- [Open the Sphinx documentation](sphinx/index.html)",
                "- [Overview](sphinx/overview.html)",
                "- [CLI reference](sphinx/cli.html)",
                "- [Python API reference](sphinx/api.html)",
                "",
                "This documentation is built directly from the pinned vm_manager source, including generated CLI and Python API references.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def refresh_revisions(config: dict) -> bool:
    changed = False
    for source in config["sources"]:
        url = f"https://github.com/{source['repository']}.git"
        ref = f"refs/heads/{source['branch']}"
        result = subprocess.run(
            ["git", "ls-remote", url, ref],
            check=True,
            capture_output=True,
            text=True,
        )
        revision = result.stdout.split()[0] if result.stdout.strip() else ""
        if len(revision) != 40:
            raise RuntimeError(f"Could not resolve {url} {ref}")
        if revision != source["revision"]:
            print(f"{source['name']}: {source['revision']} -> {revision}")
            source["revision"] = revision
            changed = True

    if changed:
        SOURCE_CONFIG.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--refresh-revisions",
        action="store_true",
        help="Update pinned revisions to the current upstream main branches",
    )
    args = parser.parse_args()

    config = json.loads(SOURCE_CONFIG.read_text(encoding="utf-8"))
    try:
        if args.refresh_revisions:
            changed = refresh_revisions(config)
            if not changed:
                print("Upstream revisions already current")

        written = sync_sources(config)
        build_vm_manager_sphinx(config)
    except (
        OSError,
        URLError,
        subprocess.CalledProcessError,
        RuntimeError,
        ValueError,
        StopIteration,
        tarfile.TarError,
        yaml.YAMLError,
    ) as error:
        print(f"Upstream documentation sync failed: {error}", file=sys.stderr)
        return 1

    print(f"Generated {len(written)} upstream documentation pages")
    print("Built vm_manager Sphinx documentation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
