# amplifier-team-pulse

Amplifier bundle for weekly commitment tracking, outcome auditing, and showcase generation.

## What It Does

Team Pulse drives outcome-oriented accountability through a fixed weekly rhythm:

1. **Monday:** Each team member runs `log-commitments` to declare what they'll ship this week
2. **Friday:** `prep-audit` scans repos and matches activity against commitments
3. **Monday:** Manager runs `draft-showcase` to review the audit and post updates to Teams

## Quick Start

### Prerequisites

- [Amplifier](https://github.com/microsoft/amplifier) installed
- [GitHub CLI](https://cli.github.com/) authenticated (`gh auth status`)
- Git configured (`git config user.name` / `git config user.email`)

### Install the Bundle

Add to your Amplifier settings:

```yaml
includes:
  - bundle: git+https://github.com/cpark4x/amplifier-team-pulse@main
```

### First-Time Setup (Manager)

1. Clone this repo
2. Copy `.env.example` to `.env` and fill in your Teams webhook URLs
3. Run the setup recipe: tell Amplifier "set up team pulse"
4. Or manually edit `team.yaml` with your team's info

### Team Member Onboarding

1. Get contributor access to this repo
2. Install the bundle in your Amplifier settings
3. Run "log my commitments" when prompted each Monday

## Recipes

| Recipe | Who | When | What |
|--------|-----|------|------|
| `log-commitments` | Each member | Monday | Log weekly commitments with outcomes |
| `prep-audit` | Automated/Manager | Friday | Scan repos, generate audit |
| `draft-showcase` | Manager | Monday | Generate and post showcases |
| `setup` | Manager | Once | Configure team and rhythm |

## Repo Structure

```
amplifier-team-pulse/
  bundle.md              # Amplifier bundle definition
  team.yaml              # Team config: members, repos, rhythm
  .env.example           # Webhook URL template
  CHANGELOG.md           # Weekly scorecard table
  README.md              # This file
  recipes/
    log-commitments.yaml # Weekly commitment entry
    prep-audit.yaml      # Repo scan + audit generation
    draft-showcase.yaml  # Showcase drafting + Teams posting
    setup.yaml           # One-time team setup
  context/
    team-pulse-instructions.md  # Shared agent context
  weeks/
    2026-W12/
      commitments/
        chris.md         # One file per person per week
        ken.md
      audit.md           # Generated audit
      showcase/
        team.md          # Team channel update
        leadership.md    # Leadership update
```

## Commitment Format

Each commitment includes:
- **Description** -- what you're doing
- **Outcome** -- what "done" looks like (specific and measurable)
- **Repo** -- which repo it's tied to (for audit matching)
- **Priority** -- `must-ship` or `stretch`

Carry-over from previous weeks is surfaced automatically.

## Design

See `docs/plans/2026-03-16-amplifier-team-pulse-design.md` for the full design document.
