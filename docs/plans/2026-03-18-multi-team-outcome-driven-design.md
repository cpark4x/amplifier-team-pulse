# Team Pulse V2: Multi-Team, Outcome-Driven Accountability

## Goal

Evolve Team Pulse from a single-team activity tracker into a multi-team, outcome-driven accountability tool. The core shift: from "what did people do" to "are people spending their time on things that matter."

## Background

Team Pulse V1 exists as a working Amplifier bundle with 4 recipes (`log-commitments`, `prep-audit`, `draft-showcase`, `setup`) and a single `team.yaml` for one team. Chris Park manages 7 direct reports under Sam S (program leader):

```
Sam S (program leader)
├── Chris P (manager)
│   ├── Gurkaran (IC, Workspaces team)
│   ├── Manoj (IC, Workspaces team)
│   ├── Ken (IC, Workspaces team)
│   ├── Salil Das (IC, Workspaces team)
│   ├── Samuel Lee (IC, reports to Chris)
│   ├── Alex Lopez (IC, reports to Chris)
│   └── Johanna (on leave)
├── Brian K (manager)
│   └── [his team]
└── [possibly other managers]
```

The close team (Gurkaran, Manoj, Ken, Salil) works on a shared project. Samuel and Alex work independently. Chris captures data for all 7 from 1:1s and standups. The team is a research team focused on becoming the best AI builders -- experimentation alongside core work is by design, not distraction.

## Approach

### The Three-Layer Model

Activity is evidence, not the goal. The tool tracks three layers:

| Layer | Cadence | Who sets it | Question it answers |
|-------|---------|-------------|---------------------|
| Outcomes | Quarterly (edit in place, git is history) | Manager + individual agree | "What are we trying to achieve?" |
| Commitments | Weekly | Individual declares (or manager captures from 1:1/standup) | "What am I doing THIS WEEK to drive those outcomes?" |
| Activity | Daily pull from GitHub | Automated | "What actually happened?" |

Each commitment explicitly links to an outcome via a `drives:` field. This is the intentionality mechanism -- it forces the question "is what I'm about to spend my time on connected to an outcome that matters?"

Experimentation is a valid outcome category, not distraction. A commitment tagged `drives: experimentation` is intentional. A commitment with no `drives:` field is directionless.

### Key Signals

| Signal | What it tells you |
|--------|------------------|
| Commitment has no `drives:` field | Work disconnected from outcomes |
| Outcome has no commitments for 2+ weeks | Nobody working toward this outcome |
| Activity doesn't match commitments | Person got distracted |
| Lots of activity, outcome not progressing | Busy but not effective |
| Commitment shipped, outcome still not progressing | Wrong lever |

## Architecture

### Person-Centric Data Model

Data is organized by person, not by team. Teams change; person data doesn't move.

```
amplifier-team-pulse/
├── org.yaml                          # Org hierarchy, teams, grants
├── people/
│   ├── ken/
│   │   ├── profile.yaml              # GitHub handles, repos, auto_discover
│   │   ├── outcomes.md               # Quarterly outcomes agreed with manager
│   │   ├── activity/
│   │   │   ├── 2026-03-17.md         # Daily GitHub activity
│   │   │   └── 2026-03-18.md
│   │   └── weeks/
│   │       └── 2026-W12/
│   │           └── commitments.md    # Weekly, each has "drives:" field
│   ├── gurkaran/
│   │   ├── profile.yaml
│   │   ├── outcomes.md
│   │   ├── activity/
│   │   └── weeks/
│   └── ... (one directory per person)
├── views/                            # Generated artifacts, not source of truth
│   ├── teams/
│   │   └── workspaces/
│   │       ├── 2026-W12-audit.md
│   │       └── 2026-W12-showcase.md
│   ├── managers/
│   │   └── chris/
│   │       └── 2026-W12-rollup.md
│   └── leadership/
│       └── sam/
│           └── 2026-W12-rollup.md
├── showcases/
│   ├── workspaces/
│   └── org-wide/
├── recipes/
├── context/
├── docs/
├── BACKLOG.md
├── CHANGELOG.md
└── bundle.md
```

Why person-centric: When Samuel moves teams, only `org.yaml` changes. His data stays in `people/samuel/`. A query for "what did Samuel ship this year?" always looks in one place. After 6 months, no data migration needed for reorgs.

## Components

### org.yaml -- The Relationship and Permission Layer

Defines who reports to whom, what teams exist, and what access grants have been made. Separate from per-person config (which lives in `profile.yaml`).

```yaml
org:
  name: "Sam's Org"

rhythm:
  commitment_day: monday
  audit_prep_day: friday
  meeting_day: monday

showcase:
  org-wide:
    channel: $TEAM_PULSE_ORG_WEBHOOK
    tone: outcomes
  workspaces:
    channel: $TEAM_PULSE_TEAM_WEBHOOK
    tone: celebratory
  leadership:
    channel: $TEAM_PULSE_LEADERSHIP_WEBHOOK
    recipient: Sam
    tone: outcomes

members:
  - name: Sam S
    role: program-leader
    github: [sam-github-handle]

  - name: Chris P
    role: manager
    reports_to: Sam S
    github: [cpark4x, cspark_microsoft]

  - name: Brian K
    role: manager
    reports_to: Sam S
    github: [brian-github-handle]

  - name: Gurkaran
    role: ic
    reports_to: Chris P

  - name: Ken
    role: ic
    reports_to: Chris P

  - name: Salil Das
    role: ic
    reports_to: Chris P

  - name: Samuel Lee
    role: ic
    reports_to: Chris P

  - name: Alex Lopez
    role: ic
    reports_to: Chris P

  - name: Manoj
    role: ic
    reports_to: Chris P

teams:
  - name: workspaces
    manager: Chris P
    members: [Gurkaran, Manoj, Ken, Salil Das]

grants: []
```

Per-person config (GitHub handles, repos, `auto_discover`) lives in `people/<name>/profile.yaml`, not in `org.yaml`. This keeps `org.yaml` focused on structure and avoids merge conflicts when repos are added.

### profile.yaml -- Per-Person Configuration

```yaml
# people/ken/profile.yaml
github:
  - kenotron-ms
  - kchau_microsoft
auto_discover: true
repos:
  - kenotron-ms/lifeos
  - kenotron-ms/agent-daemon
  - kenotron-ms/nano-foundation
```

New repos are auto-added when mentioned in commitments (existing behavior from V1).

### outcomes.md -- Per-Person Outcomes

```markdown
# Ken -- Q1 2026 Outcomes

## lifeos-adoption
LifeOS is actively used by 5+ people beyond Ken, with retention past first week.

## lifeos-eval
LifeOS has a repeatable eval framework that measures vault quality.

## experimentation
Ship 2+ exploratory projects this quarter that test new ideas.
```

Outcomes are:
- **Observable:** you can tell whether progress is happening without a debate
- **Time-bounded:** creates urgency
- **Edited in place:** git history tracks changes
- **Set via natural language prompts:** "Ken's focus this quarter is LifeOS adoption and building the eval system"

### Commitment Format

```markdown
# Ken -- Week of 2026-03-16
Logged: 2026-03-16

## Commitments

- [ ] Build eval harness for LifeOS
  - drives: lifeos-eval
  - outcome: Eval framework scoring 31 scenarios
  - repo: kenotron-ms/lifeos
  - priority: must-ship

- [x] Ship agent-daemon v0.2.9
  - drives: experimentation
  - evidence: SSE live log streaming, run card v2, executor fixes
  - repo: kenotron-ms/agent-daemon
  - priority: must-ship
```

The `drives:` field links each commitment to an outcome. Commitments without `drives:` are flagged as unconnected work.

### Views -- Generated, Not Source of Truth

Views are generated on demand from person data + `org.yaml`. They are cached in the `views/` directory but can always be regenerated.

| User asks | What happens |
|-----------|-------------|
| "What happened today?" | Reads today's activity files for your scope |
| "Show me the weekly audit" | Reads Mon-Fri activity + commitments, matches against outcomes |
| "What did we ship this month?" | Reads all activity for the month, groups by outcome |
| "Prep my 1:1 with Salil" | Reads Salil's recent activity since last 1:1 |
| "Sam wants the org status" | Reads all activity across all teams, generates leadership rollup |

## Data Flow

### Daily Activity Pull

One core write operation. Runs every morning (~2 min). Scans each person's tracked repos for commits and PRs since the last pull. Writes to `people/<name>/activity/<date>.md`.

The daily pull is the only data collection operation. Everything else (weekly audit, monthly rollup, 1:1 prep, showcase) is a read/view operation over accumulated daily data.

### GitHub Multi-Account Support

Each person can have multiple GitHub handles (personal + Microsoft). The daily pull:
1. Switches gh accounts as needed (`gh auth switch --user`)
2. Tries all handles per person as `--author` filter
3. Deduplicates by commit SHA or PR number

Auto-discover (opt-in per person via `profile.yaml`) uses the GitHub Events API to flag repos with activity not tracked in `profile.yaml`.

### Transcript Processing

A `process-standup` recipe takes a pasted transcript or `.vtt` file and extracts per-person data:
1. Identifies speakers
2. Extracts commitments, status updates, blockers per person
3. Writes to appropriate `people/<name>/weeks/<week>/commitments.md` files
4. Manager reviews and approves before commit

This is critical because Chris captures data for 7 people from 1:1s and standups -- manual entry is unsustainable.

### Showcase Generation -- Outcome-First with Narrative

Team showcase is framed around outcome progress, not activity lists:

```markdown
# Workspaces Team -- Week of 2026-03-16

## Outcome: LifeOS Adoption
Status: At risk -- installed but retention failing
This week: Ken committed onboarding docs, 3 installs completed,
           but no one used it past day 1

## Outcome: Canvas CLI
Status: On track
This week: Manoj cleaned up tech debt, session analyzer PR open

## Outcome: Experimentation
This week: Ken shipped agent-daemon v0.2.9 (21 commits),
           Chris shipped PR-FAQ and Team Pulse bundles
```

### Leadership Rollup -- Narrative + Risk Flags

Sam's view leads with a narrative paragraph providing context on what each team does and why it matters, followed by structured data:

```markdown
# Sam's Org -- Week of 2026-03-16

Chris's team is focused on building AI-powered developer tools
(Amplifier bundles). Core product work is on track -- the Canvas
CLI cleanup landed and the presentation builder is in final review.
Two concerns worth flagging: LifeOS (Ken's internal knowledge
management tool) has adoption friction -- it's been installed by
the team but nobody retained it past day one, suggesting a UX gap
worth investigating. And Salil's API migration hasn't had any
commitments in two weeks -- needs a check-in on whether this is
still a priority or should be deprioritized.

Experimentation output is strong this week -- Chris shipped 3 new
bundles (Team Pulse, PR-FAQ skill, README skill) and Ken shipped
a major update to agent-daemon. The team is building real tools
that others can use.

## Outcomes Summary

| Outcome | Owner | Status | Weeks Active |
|---------|-------|--------|-------------|
| Canvas CLI | Manoj | On track | 4 |
| Presenter Builder | Gurkaran | On track | 3 |
| LifeOS Adoption | Ken | At risk | 5 |
| API Migration | Salil | Stalled | 2 weeks no activity |
| Experimentation | Team-wide | Healthy | Ongoing |

## Needs Attention
- LifeOS Adoption: installed but not retained. Consider whether
  this needs a UX research spike or a scope reduction.
- API Migration: no commitments from Salil in 2 weeks. Is this
  still a priority?

## Team Health
| Manager | Outcomes | On Track | At Risk | Alignment |
|---------|----------|----------|---------|-----------|
| Chris   | 8        | 6        | 2       | 75%       |
| Brian   | 5        | 4        | 1       | 80%       |
```

Alignment = percentage of commitments tied to agreed outcomes vs. unconnected work.

## Visibility and Access

### Access Rules

- **Program leader (Sam):** sees everything
- **Manager (Chris, Brian):** sees own direct reports. Can request access to other managers' teams via grants in `org.yaml`.
- **IC on a team (Ken):** sees own data + team shared data
- **IC standalone (Salil):** sees own data only
- **Everyone:** can see data marked public to their group (org-wide showcases)

### Phased Enforcement

| Phase | Enforcement |
|-------|-------------|
| MVP | Repo access = see everything. CLI works for collaborators only. Non-collaborators (Samuel, Sam) get info relayed by Chris or via shared artifacts. |
| V2 | CLI filters by identity (`git config` -> `org.yaml` lookup). Honest but not enforced -- raw files still on disk. |
| V3 | Website with authentication (Microsoft SSO or GitHub OAuth). Real access controls. The repo is the data store, the website is the read layer. |

Grant mechanism: "Grant Brian access to workspaces" adds an entry to `org.yaml` grants section.

### CLI Identity and Scoped Queries

The CLI detects identity from git config and matches against `org.yaml`:
- Ken runs "show me the audit" -> sees Workspaces team data only
- Chris runs "show me the audit" -> sees all 7 directs
- Sam runs "show me the audit" -> sees everything
- Brian runs "show me the audit" -> sees his team + granted access

This is V2 behavior. MVP has no filtering.

## Operations

| Command | What it does |
|---------|-------------|
| "Pull activity" | Daily. Scans repos per person, writes `people/<name>/activity/<date>.md` |
| "Log commitments" | Weekly. Interactive, each commitment links to outcome via `drives:`. Auto-adds new repos to `profile.yaml` |
| "Process this standup" | Extracts per-person data from pasted transcript |
| "Set outcomes for Ken" | Quarterly. Natural language, writes `people/ken/outcomes.md` |
| "Show me the audit" | Generates view scoped to your identity -- outcomes status with activity evidence |
| "Draft the showcase" | Team and leadership narratives framed around outcome progress |
| "Grant Brian access to workspaces" | Adds entry to `org.yaml` grants |
| "Prep my 1:1 with Salil" | Reads Salil's recent activity and outcome progress |

## Migration from V1

One-shot migration (repo has minimal data):
1. Create `org.yaml` from existing `team.yaml`
2. Create `people/` directories for each member
3. Extract `profile.yaml` per person from `team.yaml`
4. Move existing `weeks/2026-W12/commitments/chris.md` to `people/chris/weeks/2026-W12/commitments.md`
5. Update recipes to read from new structure
6. Delete `team.yaml` and old `weeks/` directory
7. One commit

## Testing Strategy

- Validate `org.yaml` parsing with the full org hierarchy
- Test daily pull writes to correct person directories and deduplicates across multi-account handles
- Test commitment logging links to outcomes via `drives:` field
- Test view generation scopes correctly per identity (MVP: unscoped; V2: filtered)
- Test transcript processing extracts per-person data and writes to correct paths
- Test migration moves existing V1 data to new structure without data loss

## Open Questions

1. **Sam's and Brian's GitHub handles** -- need to collect these
2. **Salil, Samuel, Alex's GitHub handles** -- need to collect these
3. **Johanna's status** -- on leave, excluded for now, add when she returns
4. **Microsoft GitHub Enterprise access** -- `_microsoft` handles 404 from personal gh token. Each person's Microsoft account events may not be visible depending on org permissions. Need to verify.
5. **Daily activity file accumulation** -- keeping daily files as-is for now. Will revisit consolidation if it becomes a performance problem.
