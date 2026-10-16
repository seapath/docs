"""Add synchronized Ansible role pages to MkDocs navigation."""

from pathlib import Path


def on_config(config):
    docs_dir = Path(config["docs_dir"])
    roles_dir = docs_dir / "_generated" / "upstream" / "ansible" / "roles"
    role_pages = sorted(
        (
            page
            for page in roles_dir.rglob("*.md")
            if page.name != "index.md"
        ),
        key=lambda page: page.relative_to(roles_dir).as_posix().casefold(),
    )

    role_navigation = [
        {"All roles": "_generated/upstream/ansible/roles/index.md"}
    ]
    for page in role_pages:
        relative_path = page.relative_to(docs_dir).as_posix()
        role_name = page.relative_to(roles_dir).with_suffix("").as_posix()
        role_navigation.append({role_name: relative_path})

    for top_level_item in config["nav"]:
        if not isinstance(top_level_item, dict):
            continue
        collection_nav = top_level_item.get("Ansible Galaxy collection")
        if collection_nav is None:
            continue
        for collection_item in collection_nav:
            if isinstance(collection_item, dict) and "Roles" in collection_item:
                collection_item["Roles"] = role_navigation
                return

    raise ValueError("Could not find Ansible Galaxy collection > Roles in MkDocs nav")
