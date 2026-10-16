# SEAPATH Documentation

This repository contains the source for the [LF Energy SEAPATH documentation](https://seapath.readthedocs.io/). The documentation is maintained as code with Markdown, [MkDocs](https://www.mkdocs.org/), and Read the Docs.

The content was originally hosted on [Confluence](https://lf-energy.atlassian.net/wiki/spaces/SEAP/overview). The Markdown files in this repository are now the source of truth for the published documentation.

## Repository layout

- `docs/` — documentation pages and assets
- `mkdocs.yml` — site configuration and navigation
- `.readthedocs.yaml` — Read the Docs build configuration
- `requirements.txt` — Python dependencies for building the site

## Preview the documentation locally

Requirements: Python 3.12 or newer and pip.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/sync_upstream_docs.py
mkdocs serve
```

Open the local URL printed by MkDocs (usually <http://127.0.0.1:8000/>). To build the static site instead, run:

```bash
python scripts/sync_upstream_docs.py
mkdocs build
```

The generated site is written to `site/`.

The sync step needs network access to GitHub. It fetches the Ansible Galaxy overview, inventory guide, module reference, and every role README from revisions pinned in `docs/upstream-sources.json`. To update those pins to the current upstream `main` branches and refresh the generated pages, run:

```bash
python scripts/sync_upstream_docs.py --refresh-revisions
```

The Ansible role sidebar is populated from synchronized role pages by `scripts/mkdocs_nav.py`; no per-role navigation edits are needed. Review revision changes and rebuild the site before committing updates. Generated pages under `docs/_generated/` are build output and are not committed.
