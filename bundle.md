---
bundle:
  name: team-pulse
  version: 0.2.0
  description: >
    Outcome-driven weekly accountability for multi-team orgs. Track outcomes,
    commitments, and activity per person. Generate audits grouped by outcome
    progress and narrative showcases for leadership.

includes:
  - bundle: git+https://github.com/microsoft/amplifier-foundation@main
  - bundle: git+https://github.com/microsoft/amplifier-bundle-recipes@main#subdirectory=behaviors/recipes.yaml
---

# Team Pulse

**Outcome-driven weekly commitment tracking for teams.**

Track what your team commits to each week, link every commitment to a quarterly outcome, audit delivery against actual repo activity, and auto-generate showcases for multiple audiences — from team celebrations to leadership narratives.

## Data Model

Three layers, each building on the last:
- **Outcomes** (quarterly) — What are we trying to achieve?
- **Commitments** (weekly) — What am I doing THIS WEEK to drive those outcomes?
- **Activity** (daily) — What actually happened in GitHub?

Data is organized per person in `people/<name>/` directories. Org structure lives in `org.yaml`.

## Workflows (6 Recipes)
- **pull-activity** — Daily GitHub activity scan per person
- **log-commitments** — Each member logs weekly commitments linked to outcomes via `drives:`
- **set-outcomes** — Quarterly outcome setting through natural language
- **prep-audit** — Outcome-first audit: matches activity against commitments and outcomes
- **draft-showcase** — Team and leadership showcases with narrative rollup for Sam
- **process-standup** — Extract per-person commitments from standup transcripts

---

@team-pulse:context/team-pulse-instructions.md

---

@foundation:context/shared/common-system-base.md
