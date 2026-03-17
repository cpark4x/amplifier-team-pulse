---
bundle:
  name: team-pulse
  version: 0.1.0
  description: >
    Weekly commitment tracking, outcome auditing, and showcase generation for teams.
    Drive outcome-oriented accountability through a fixed weekly rhythm.

includes:
  - bundle: git+https://github.com/microsoft/amplifier-foundation@main
  - bundle: git+https://github.com/microsoft/amplifier-bundle-recipes@main#subdirectory=behaviors/recipes.yaml
---

# Team Pulse

**Outcome-driven weekly commitment tracking for teams.**

Track what your team commits to each week, audit delivery against actual repo activity, and auto-generate showcases for multiple audiences.

## What This Bundle Provides

### Weekly Rhythm
- **Monday:** Team members log commitments with concrete outcomes
- **Friday:** Tool audits delivery against repo activity
- **Monday:** Manager reviews audit, sends showcases to team and leadership

### Workflows (4 Recipes)
- **log-commitments** — Each member logs weekly commitments with outcomes, repos, and priorities
- **prep-audit** — Scans repos for activity, matches against commitments, generates audit
- **draft-showcase** — Generates audience-appropriate showcases, posts to Teams on approval
- **setup** — One-time team configuration

---

@team-pulse:context/team-pulse-instructions.md

---

@foundation:context/shared/common-system-base.md
