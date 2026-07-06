
# Tengkong World Archive

A fully automated bilingual digital archive system.

---

## Architecture

Source Repository → Build System → Deployment Repository → GitHub Pages

Fully automated CI/CD pipeline.

---

## Repositories

- tengkong-archive → Source code & data processing
- tengkongworld.github.io → Public website (GitHub Pages)

---

## Workflow

1. Fetch data (Blogger / feed)
2. Generate structured JSON
3. Build static HTML pages
4. Sync build/ to deployment repo
5. Commit & push changes
6. GitHub Pages updates automatically

Run the complete deployment from this repository only:

```bash
python3 deploy.py
```

Deployment rules:

- `tengkong-archive` is the only source of truth.
- `tengkongworld.github.io` is a pure deployment target.
- Do not manually edit, merge, or rebase inside `tengkongworld.github.io`.
- Each deploy resets the deployment repo to `origin/main`, replaces its contents with `build/`, commits, and pushes.

---

## Output Structure

build/
├── articles/
├── labels/
├── tc/
├── assets/
└── data/

---

## Features

- Bilingual (Simplified / Traditional Chinese)
- Fully automated deployment
- Static site generation
- Image extraction & management
- Label & archive system

---

## Status

v4.0 Stable CI/CD system completed.
