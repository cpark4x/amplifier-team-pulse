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

## Quick Start: New Team

**~10 minutes to set up. One repo per team.**

### Prerequisites

- [Amplifier](https://github.com/microsoft/amplifier) installed
- [GitHub CLI](https://cli.github.com/) authenticated (`gh auth status`)

### 1. Create your team's repo

```bash
gh repo create your-org/team-pulse --private --clone
cd team-pulse
```

### 2. Install the bundle

Add to your Amplifier settings:

```yaml
includes:
  - bundle: git+https://github.com/cpark4x/amplifier-team-pulse@main
```

### 3. Run setup

Tell Amplifier:

> "set up team pulse"

The recipe walks you through adding team members, repos, rhythm, and webhook config. It generates `team.yaml` and commits it. That's it -- your team is tracking.

Or copy `team.yaml.example` to `team.yaml` and edit manually.

### 4. Onboard your team

Each team member:
1. Gets contributor access to the repo
2. Adds the bundle to their Amplifier settings
3. Says "log my commitments" on Monday

## Quick Start: Join an Existing Team

Your team lead already set up a team-pulse repo. You need:

1. Clone the repo (`git clone <your-team-pulse-repo>`)
2. Add the bundle to your Amplifier settings:
   ```yaml
   includes:
     - bundle: git+https://github.com/cpark4x/amplifier-team-pulse@main
   ```
3. Tell Amplifier: "log my commitments"

That's it -- the recipe walks you through entering commitments with outcomes and priorities.

## How It Works

Four recipes. Configurable rhythm -- default is Monday/Friday/Monday.

| Recipe | Who | When | What |
|--------|-----|------|------|
| `log-commitments` | Each member | Start of week | Declare commitments with outcomes, repos, priorities |
| `prep-audit` | Auto/Manager | End of week | Scan repos via `gh` CLI, match activity against commitments |
| `draft-showcase` | Manager | Before meeting | Generate showcases, post to Teams on approval |
| `setup` | Manager | Once | Configure team members, repos, rhythm, webhooks |

Each commitment tags a repo. The audit matches PRs, commits, and branch names against commitment descriptions. Unshipped commitments carry forward automatically -- they show up next Monday with a trail back to when they were first committed.

Already shipped something before logging it? The recipe handles that too -- say "I already shipped this" and it logs it as completed with evidence.

## What It Won't Do (Yet)

- No automated reminders (you tell people to run it)
- No quarterly rollups (data model supports it, recipe isn't built yet)
- No privacy controls for large teams (transparent by default, appropriate for teams with trust)

## Built By

Chris Park -- because Monday mornings should be about planning what's next, not reconstructing what happened.
