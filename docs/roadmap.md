# 腾空世界观数字档案馆

# Version 2 Development Roadmap

> Status: In Progress
>
> Goal:
>
> Build a configuration-driven digital archive system.

---

# Overall Progress

Milestone A

██████████ 100%

Configuration Driven

✓ Completed

Milestone B  ░░░░░░░░░░  0%
Engineering Refactoring

20%

Milestone C  ░░░░░░░░░░  0%

Milestone D  ░░░░░░░░░░  0%

Milestone E  ░░░░░░░░░░  0%

---

# Milestone A

## Configuration Driven

Objective

Move archive behavior from hard-coded logic into configuration.

Status

🚧 In Progress

Tasks

| ID | Task | Status | Priority |
|----|------|--------|----------|
| V2-001 | Collection API | ✅ | High |
| V2-002 | Local Image System | ✅ | High |
| V2-003 | Collection Default Behavior | 🚧 | High |
| V2-004 | Homepage Configuration | 📋 | High |
| V2-005 | Configuration Validation | 📋 | Medium |

Deliverables

- Collection API
- archive.config.json
- default_view
- default_sort
- Homepage configuration
- Configuration validation

---

# Milestone B

## Collection Driven

Objective

Collections become the primary organizational object of the archive.

Status

📋 Planned

Tasks

| ID | Task | Status |
|----|------|--------|
| V2-006 | Collection Page | 📋 |
| V2-007 | Collection Metadata | 📋 |
| V2-008 | Collection Statistics | 📋 |
| V2-009 | Collection Navigation | 📋 |
| V2-010 | Collection Cover | 📋 |

Deliverables

- Collection homepage
- Collection metadata
- Collection statistics
- Navigation
- Cover system

---

# Milestone C

## Archive Engine

Objective

Turn sync.py into a reusable archive generation engine.

Status

📋 Planned

Tasks

- Metadata engine
- Search index
- Validation
- Incremental build
- Build report

---

# Milestone D

## User Experience

Objective

Improve archive usability.

Status

📋 Planned

Tasks

- Reading history
- Bookmarks
- Theme system
- Responsive layout
- Timeline
- Favorites

---

# Milestone E

## Publishing Platform

Objective

Expand the archive into a publishing platform.

Status

📋 Planned

Tasks

- EPUB export
- PDF export
- RSS
- Metadata API
- Search API

---

# Design Principles

Version 2 follows these principles:

1. Configuration defines default behavior.

2. sync.py interprets configuration.

3. Generated HTML carries configuration to the frontend.

4. JavaScript handles interaction only.

5. User preferences override configuration and are stored locally.

6. Collection is the primary organizational object.

7. Documentation is maintained before implementation.