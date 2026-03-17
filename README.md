# amplifier-team-pulse

Your skip-level asks "what did your team deliver this week?" You spend 30 minutes digging through PRs, Slack threads, and hazy Monday memories to reconstruct it. Meanwhile, half the commitments from last Monday quietly disappeared -- nobody mentioned them, nobody carried them forward.

Team Pulse makes commitments visible and outcomes verifiable. Each person declares what they'll ship on Monday with concrete outcomes. On Friday, the tool scans their repos and matches activity against those commitments. Monday morning, you have a pre-built audit and a showcase draft ready for leadership. The commits don't lie, and nothing quietly disappears.

## What It Looks Like

**Monday -- each team member declares commitments:**

```markdown
- [ ] Ship Eval system for LifeOS
  - outcome: Eval harness passing 3+ test cases in CI
  - repo: kenotron-ms/lifeos
  - priority: must-ship
- [ ] Create a demo for LifeOS
  - outcome: 5-minute walkthrough ready for Thursday demo
  - repo: kenotron-ms/lifeos
  - priority: stretch
```

**Friday -- the tool scans repos and generates an audit:**

```markdown
| Commitment | Status | Evidence |
|------------|--------|----------|
| Ship Eval system | Shipped | PR #14 "Eval harness scaffold" merged 2026-03-19 |
| Create demo | Partial | PR #18 "Demo walkthrough" open, 4 commits |
```

**Monday morning -- you get two showcase drafts:**
- Team channel: names people, celebrates wins, surfaces carry-over
- Leadership brief: must-ship scorecard (6/8 shipped, 75%), trend line, next week focus

Review in 2 minutes, approve, posted to Teams.

## Quick Start

**~5 minutes to install. First result: your commitment file, committed to the repo.**

```yaml
# Add to your Amplifier settings
includes:
  - bundle: git+https://github.com/cpark4x/amplifier-team-pulse@main
```

Clone this repo, then tell Amplifier:

> "log my commitments"

The recipe walks you through entering commitments with outcomes and priorities. That's it -- you're tracking.

For team setup (members, repos, webhooks, rhythm), run "set up team pulse" or edit `team.yaml` directly. See the [usage guide](docs/plans/2026-03-16-amplifier-team-pulse-design.md) for full configuration.

## How It Works

Four recipes. Configurable rhythm -- default is Monday/Friday/Monday.

| Recipe | Who | When | What |
|--------|-----|------|------|
| `log-commitments` | Each member | Start of week | Declare commitments with outcomes, repos, priorities |
| `prep-audit` | Auto/Manager | End of week | Scan repos via `gh` CLI, match activity against commitments |
| `draft-showcase` | Manager | Before meeting | Generate showcases, post to Teams on approval |
| `setup` | Manager | Once | Configure team members, repos, rhythm, webhooks |

Each commitment tags a repo. The audit matches PRs, commits, and branch names against commitment descriptions. Unshipped commitments carry forward automatically -- they show up next Monday with a trail back to when they were first committed.

## What It Won't Do (Yet)

- No automated reminders (you tell people to run it)
- No quarterly rollups (data model supports it, recipe isn't built yet)
- No privacy controls for large teams (transparent by default, appropriate for teams with trust)

## Built By

Chris Park -- because Monday mornings should be about planning what's next, not reconstructing what happened.
