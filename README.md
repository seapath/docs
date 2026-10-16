# SEAPATH Documentation

This repository contains the source for the [LF Energy SEAPATH documentation](https://seapath.readthedocs.io/). The documentation is maintained as code with Markdown, [MkDocs](https://www.mkdocs.org/), and Read the Docs.

The content was originally hosted on [Confluence](https://lf-energy.atlassian.net/wiki/spaces/SEAP/overview). The Markdown files in this repository are now the source of truth for the published documentation.

## Repository layout

- `docs/` — documentation pages and assets
- `mkdocs.yml` — site configuration and navigation
- `.readthedocs.yaml` — Read the Docs build configuration
- `requirements.txt` — Python dependencies for building the site

## Preview the documentation locally

Requirements: Python 3 and pip.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
mkdocs serve
```

Open the local URL printed by MkDocs (usually <http://127.0.0.1:8000/>). To build the static site instead, run:

```bash
mkdocs build
```

The generated site is written to `site/`.
