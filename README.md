
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