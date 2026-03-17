# amplifier-team-pulse

Your team had a great week. Three features shipped, a demo landed, and the intern fixed that auth bug everyone forgot about. But when your skip-level asks "what did your team deliver?" you spend 30 minutes digging through PRs, Slack threads, and hazy Monday memories to reconstruct it.

Meanwhile, half the commitments from last Monday quietly disappeared. Nobody mentioned them. Nobody carried them forward. They just... stopped existing.

Team Pulse fixes both problems. Each person declares what they'll ship on Monday -- with concrete outcomes, not vague intentions. On Friday, the tool scans their repos and matches activity against those commitments. On Monday morning, you have a pre-built audit and a showcase draft ready to send to leadership. The commits don't lie, and nothing quietly disappears.

## What It Looks Like

**Monday -- each team member runs `log-commitments`:**

```markdown
# Ken -- Week of 2026-03-16
Logged: 2026-03-16

## Carried Forward

- Implement Eval system for LifeOS (from W11 -- partial, PR #14 open)

## Commitments

- [ ] Ship Eval system for LifeOS
  - outcome: Eval harness passing 3+ test cases in CI
  - repo: kenotron-ms/lifeos
  - priority: must-ship
  - carried-from: W11
- [ ] Create a demo for LifeOS
  - outcome: 5-minute walkthrough ready for Thursday demo
  - repo: kenotron-ms/lifeos
  - priority: must-ship
```

**Friday -- `prep-audit` scans repos automatically:**

```markdown
## Ken

### Must-Ship

| Commitment | Status | Evidence |
|------------|--------|----------|
| Ship Eval system | Shipped | PR #14 "Eval harness scaffold" merged 2026-03-19 |
| Create demo for LifeOS | Partial | PR #18 "Demo walkthrough" open, 4 commits |
```

**Monday morning -- `draft-showcase` generates two outputs:**
- A team showcase that names people and celebrates wins
- A leadership brief with a must-ship scorecard (6/8 shipped, 75%) and trend line

You review both in 2 minutes, tweak if needed, approve, and they post to Teams.

## Quick Start

**Install time:** ~5 minutes. **First result:** Your first commitment file, committed to the repo.

### Prerequisites

- [Amplifier](https://github.com/microsoft/amplifier) installed
- [GitHub CLI](https://cli.github.com/) authenticated (`gh auth status`)

### Install the Bundle

```yaml
# In your Amplifier settings
includes:
  - bundle: git+https://github.com/cpark4x/amplifier-team-pulse@main
```

### First Commitments

Clone this repo, then tell Amplifier:

> "log my commitments"

That's it. The recipe walks you through entering your commitments with outcomes and priorities.

For full setup (team config, webhooks, rhythm settings), run "set up team pulse" or edit `team.yaml` directly.

## How It Works

Four recipes drive the weekly cycle. Configurable rhythm -- default is Monday/Friday/Monday.

| Recipe | Who | When | What |
|--------|-----|------|------|
| `log-commitments` | Each member | Start of week | Declare commitments with outcomes, repos, priorities |
| `prep-audit` | Auto/Manager | End of week | Scan repos via `gh` CLI, match activity against commitments |
| `draft-showcase` | Manager | Before meeting | Generate team + leadership showcases, post to Teams on approval |
| `setup` | Manager | Once | Configure team members, repos, rhythm, webhooks |

Each commitment tags a repo. The audit pulls PRs and commits from that repo and matches them against the commitment using titles, branch names, and commit messages. Commitments that don't ship carry forward automatically -- they don't quietly disappear.

## What It Won't Do (Yet)

- No automated reminders (you tell people to run it)
- No quarterly rollups (the data model supports it, the recipe isn't built yet)
- No privacy controls for large teams (transparent by default, appropriate for small teams with trust)

## Built By

Chris Park -- built to solve the "what did we ship this week?" problem for the Workspaces team at Microsoft.
