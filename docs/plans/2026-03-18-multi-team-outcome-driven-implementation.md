# Team Pulse V2: Multi-Team Outcome-Driven Implementation Plan

> **Execution:** Use the subagent-driven-development workflow to implement this plan.

**Goal:** Restructure Team Pulse from a single-team activity tracker into a multi-team, outcome-driven accountability tool with person-centric data, daily activity pulls, outcome linking, and narrative showcases for leadership.

**Architecture:** The repo moves from a flat `team.yaml` + `weeks/` structure to a person-centric `org.yaml` + `people/<name>/` structure. Each person gets their own directory with profile config, outcomes, activity logs, and weekly commitments. Recipes read `org.yaml` for org structure and `people/<name>/profile.yaml` for GitHub config. Views and showcases are generated artifacts grouped by outcome, not by person.

**Tech Stack:** Amplifier bundle (YAML recipes, markdown templates, YAML config). No traditional code — all files are recipe YAML, config YAML, or markdown. Validation via `amplifier tool invoke recipes operation=validate`.

---

## What Is This Project?

Team Pulse is an Amplifier bundle — a set of YAML recipe files that orchestrate an AI agent to do weekly team accountability work. Think of it like a bot that:

1. **Pulls activity** from GitHub repos (commits, PRs) for each team member
2. **Logs commitments** — what each person says they'll do this week
3. **Audits delivery** — matches what people said vs. what actually shipped
4. **Generates showcases** — formatted updates for the team channel and leadership

The bundle currently tracks one team (4 people) with a flat file structure. We're upgrading it to support a multi-team org (7+ people, 2 managers, 1 program leader) with an **outcome-driven** model where every commitment links to a quarterly outcome.

### Key Files You'll Be Working With

- **Recipe YAML files** (`recipes/*.yaml`) — These contain instructions for an AI agent. The `prompt:` field is a long markdown string telling the agent what to do step by step. Recipes can use Jinja2 templating (`{% if %}`, `{{variable}}`).
- **Config YAML files** (`org.yaml`, `people/*/profile.yaml`) — Plain YAML configuration.
- **Markdown files** (`people/*/outcomes.md`, commitment files) — Structured markdown that recipes read and write.
- **Context files** (`context/team-pulse-instructions.md`) — Instructions loaded into the bundle that tell the agent which recipe to run for which user command.
- **`bundle.md`** — The bundle manifest. Declares the bundle name, version, includes, and loads context files.

### How to Validate Recipe Files

After creating or modifying any recipe YAML file, validate it:
```
amplifier tool invoke recipes operation=validate recipe_path=@team-pulse:recipes/<name>.yaml
```
This checks YAML syntax and recipe schema (required fields, valid step structure, etc.). Config and markdown files don't have a validator — you verify them by reading them back.

### Commit Message Convention

All commits use `type: description` format:
- `feat: ...` for new features
- `chore: ...` for restructuring, cleanup
- `docs: ...` for documentation changes

---

## Phase 1: Foundation (Migration + Data Structure)

This phase creates the new directory structure, config files, and migrates existing data. It's mostly mechanical file creation. After this phase, the repo has the right shape for all the recipes in Phases 2 and 3.

---

### Task 1: Create `org.yaml`

**Files:**
- Create: `org.yaml`

**What this file does:** Defines the org hierarchy — who reports to whom, what teams exist, showcase webhook config, and weekly rhythm settings. It does NOT contain GitHub handles or repos (those go in per-person `profile.yaml` files). Think of it as the "org chart + settings" file.

**Step 1: Create the file**

Create `org.yaml` with this exact content:

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

  - name: Chris P
    role: manager
    reports_to: Sam S

  - name: Brian K
    role: manager
    reports_to: Sam S

  - name: Gurkaran
    role: ic
    reports_to: Chris P

  - name: Manoj
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

teams:
  - name: workspaces
    manager: Chris P
    members: [Gurkaran, Manoj, Ken, Salil Das]

grants: []
```

**Step 2: Verify the file**

Read back `org.yaml` and confirm it has 10 members (Sam, Chris, Brian, + 7 ICs), one team (workspaces with 4 members), and the rhythm/showcase config.

---

### Task 2: Create `profile.yaml` for Chris, Gurkaran, Manoj, Ken

**Files:**
- Create: `people/chris/profile.yaml`
- Create: `people/gurkaran/profile.yaml`
- Create: `people/manoj/profile.yaml`
- Create: `people/ken/profile.yaml`

**What these files do:** Each person's GitHub handles, tracked repos, and auto-discover setting. Recipes read these to know which GitHub accounts to scan and which repos to pull activity from. These four people have known GitHub handles from the existing `team.yaml`.

**Step 1: Create directory structure and files**

Create all four files. The directory `people/<name>/` will be created automatically when writing the file.

`people/chris/profile.yaml`:
```yaml
github:
  - cpark4x
  - cspark_microsoft
auto_discover: true
repos:
  - cpark4x/canvas-specialists
  - cpark4x/ridecast
  - cpark4x/canvas-app
  - technology-and-research/workspaces2
```

`people/gurkaran/profile.yaml`:
```yaml
github:
  - singh2
  - gurksing_microsoft
auto_discover: false
repos:
  - cpark4x/canvas-specialists
```

`people/manoj/profile.yaml`:
```yaml
github:
  - manojp99
  - mpaidiparthy_microsoft
auto_discover: false
repos:
  - microsoft/amplifier-app-cli
```

`people/ken/profile.yaml`:
```yaml
github:
  - kenotron-ms
  - kchau_microsoft
auto_discover: true
repos:
  - kenotron-ms/lifeos
  - kenotron-ms/agent-daemon
  - kenotron-ms/nano-foundation
```

**Step 2: Verify**

Read back each file and confirm the GitHub handles and repos match the values above.

---

### Task 3: Create `profile.yaml` for Salil, Samuel, Alex (placeholders)

**Files:**
- Create: `people/salil/profile.yaml`
- Create: `people/samuel/profile.yaml`
- Create: `people/alex/profile.yaml`

**What's different:** These three team members don't have known GitHub handles yet. Create placeholder profiles so the directory structure exists and recipes don't break when iterating over members.

**Step 1: Create the files**

`people/salil/profile.yaml`:
```yaml
github: []
auto_discover: false
repos: []
```

`people/samuel/profile.yaml`:
```yaml
github: []
auto_discover: false
repos: []
```

`people/alex/profile.yaml`:
```yaml
github: []
auto_discover: false
repos: []
```

**Step 2: Verify**

Read back each file and confirm all three have empty `github` and `repos` lists.

---

### Task 4: Create placeholder `outcomes.md` for all 7 ICs and Chris

**Files:**
- Create: `people/chris/outcomes.md`
- Create: `people/gurkaran/outcomes.md`
- Create: `people/manoj/outcomes.md`
- Create: `people/ken/outcomes.md`
- Create: `people/salil/outcomes.md`
- Create: `people/samuel/outcomes.md`
- Create: `people/alex/outcomes.md`

**Why placeholders:** Every recipe in Phases 2 and 3 assumes `outcomes.md` exists for each person. By creating placeholders now, no recipe needs defensive "file might not exist" handling. When real outcomes are defined later via the `set-outcomes` recipe, it just replaces the placeholder content.

**Step 1: Create all 7 files**

Each file follows the same pattern — only the name changes.

`people/chris/outcomes.md`:
```markdown
# Chris -- Q1 2026 Outcomes

## general
Outcomes not yet defined. Use "set outcomes for Chris" to define.
```

`people/gurkaran/outcomes.md`:
```markdown
# Gurkaran -- Q1 2026 Outcomes

## general
Outcomes not yet defined. Use "set outcomes for Gurkaran" to define.
```

`people/manoj/outcomes.md`:
```markdown
# Manoj -- Q1 2026 Outcomes

## general
Outcomes not yet defined. Use "set outcomes for Manoj" to define.
```

`people/ken/outcomes.md`:
```markdown
# Ken -- Q1 2026 Outcomes

## general
Outcomes not yet defined. Use "set outcomes for Ken" to define.
```

`people/salil/outcomes.md`:
```markdown
# Salil -- Q1 2026 Outcomes

## general
Outcomes not yet defined. Use "set outcomes for Salil" to define.
```

`people/samuel/outcomes.md`:
```markdown
# Samuel -- Q1 2026 Outcomes

## general
Outcomes not yet defined. Use "set outcomes for Samuel" to define.
```

`people/alex/outcomes.md`:
```markdown
# Alex -- Q1 2026 Outcomes

## general
Outcomes not yet defined. Use "set outcomes for Alex" to define.
```

**Step 2: Verify**

Spot-check 2-3 files to confirm the name in the header matches the directory name.

---

### Task 5: Create empty `activity/` and `weeks/` directories, migrate existing data

**Files:**
- Create: `people/<name>/activity/.gitkeep` for all 7 ICs + Chris (8 total)
- Create: `people/<name>/weeks/.gitkeep` for all 7 ICs + Chris (8 total)
- Move: `weeks/2026-W12/commitments/chris.md` → `people/chris/weeks/2026-W12/commitments.md`

**Why `.gitkeep`:** Git doesn't track empty directories. A `.gitkeep` file is a convention to force git to track the directory. Recipes will later write real files here.

**Step 1: Create `.gitkeep` files for all activity directories**

Run:
```bash
for name in chris gurkaran manoj ken salil samuel alex; do
  mkdir -p people/$name/activity
  touch people/$name/activity/.gitkeep
  mkdir -p people/$name/weeks
  touch people/$name/weeks/.gitkeep
done
```

**Step 2: Migrate Chris's existing commitment file**

```bash
mkdir -p people/chris/weeks/2026-W12
cp weeks/2026-W12/commitments/chris.md people/chris/weeks/2026-W12/commitments.md
```

**Step 3: Verify**

```bash
# Confirm directory structure exists for all people
ls people/*/activity/.gitkeep
ls people/*/weeks/.gitkeep

# Confirm migrated commitment file exists and has content
cat people/chris/weeks/2026-W12/commitments.md
```

The commitment file should contain:
```
# Chris -- Week of 2026-03-16
Logged: 2026-03-17
...
```

---

### Task 6: Create view and showcase directories

**Files:**
- Create: `views/teams/workspaces/.gitkeep`
- Create: `views/managers/chris/.gitkeep`
- Create: `views/leadership/sam/.gitkeep`
- Create: `showcases/workspaces/.gitkeep`
- Create: `showcases/org-wide/.gitkeep`

**What these are for:** Recipes in Phase 3 will generate audit views and showcases into these directories. Creating them now so the structure is ready.

**Step 1: Create all directories with `.gitkeep` files**

```bash
mkdir -p views/teams/workspaces && touch views/teams/workspaces/.gitkeep
mkdir -p views/managers/chris && touch views/managers/chris/.gitkeep
mkdir -p views/leadership/sam && touch views/leadership/sam/.gitkeep
mkdir -p showcases/workspaces && touch showcases/workspaces/.gitkeep
mkdir -p showcases/org-wide && touch showcases/org-wide/.gitkeep
```

**Step 2: Verify**

```bash
find views showcases -name .gitkeep
```

Should show 5 `.gitkeep` files.

---

### Task 7: Delete old structure

**Files:**
- Delete: `team.yaml`
- Delete: `team.yaml.example`
- Delete: `weeks/` (entire directory)
- Delete: `recipes/setup.yaml`

**Why delete these:**
- `team.yaml` is replaced by `org.yaml` + per-person `profile.yaml` files
- `team.yaml.example` is no longer relevant
- `weeks/` is replaced by `people/<name>/weeks/` (data already migrated in Task 5)
- `recipes/setup.yaml` is replaced by direct `org.yaml` management (no more interactive setup recipe)

**Step 1: Delete the files**

```bash
rm team.yaml
rm team.yaml.example
rm -rf weeks/
rm recipes/setup.yaml
```

**Step 2: Verify**

```bash
# These should all fail with "No such file or directory"
ls team.yaml
ls team.yaml.example
ls weeks/
ls recipes/setup.yaml
```

---

### Task 8: Commit Phase 1

**Step 1: Review what's staged**

```bash
git add -A
git status
```

You should see:
- **New files:** `org.yaml`, `people/*/profile.yaml`, `people/*/outcomes.md`, `people/*/activity/.gitkeep`, `people/*/weeks/.gitkeep`, `people/chris/weeks/2026-W12/commitments.md`, `views/**/.gitkeep`, `showcases/**/.gitkeep`
- **Deleted files:** `team.yaml`, `team.yaml.example`, `weeks/2026-W12/commitments/chris.md`, `recipes/setup.yaml`

**Step 2: Commit**

```bash
git commit -m "feat: migrate to person-centric data structure with org.yaml

- Create org.yaml with full org hierarchy (Sam, Chris, Brian, 7 ICs)
- Create people/<name>/profile.yaml for each member (GitHub handles, repos)
- Create placeholder outcomes.md for each member
- Create activity/ and weeks/ directories per person
- Migrate chris W12 commitments to people/chris/weeks/2026-W12/
- Create views/ and showcases/ directory structure
- Delete team.yaml, weeks/, and setup.yaml (replaced by new structure)"
```

```bash
git push
```

---

## Phase 2: Core Operations (New and Updated Recipes)

This phase creates the recipes that write data into the new structure: daily activity pulling, commitment logging with outcome linking, and outcome setting. After this phase, the three-layer model (outcomes → commitments → activity) is operational.

---

### Task 9: Create `recipes/pull-activity.yaml`

**Files:**
- Create: `recipes/pull-activity.yaml`

**What this recipe does:** This is the daily workhorse. It scans every team member's tracked GitHub repos for commits and PRs, and writes the results to `people/<name>/activity/YYYY-MM-DD.md`. It's meant to run once per morning (~2 min) to collect what happened since the last pull.

**Step 1: Create the recipe file**

Create `recipes/pull-activity.yaml` with this exact content:

```yaml
name: pull-activity
description: >
  Daily activity pull from GitHub. Scans each team member's tracked repos
  for commits and PRs, writes per-person daily activity files. Supports
  multi-account GitHub handles and auto-discover for untracked repos.
version: "0.1.0"
tags: ["activity", "daily", "automation", "github"]

# Usage:
#   "Pull activity"
#   amplifier tool invoke recipes operation=execute recipe_path=@team-pulse:recipes/pull-activity.yaml
#   amplifier tool invoke recipes operation=execute recipe_path=@team-pulse:recipes/pull-activity.yaml context='{"date": "2026-03-18"}'

context:
  date: ""  # Optional: defaults to today. Format: YYYY-MM-DD

steps:
  - id: pull-activity
    agent: self
    timeout: 600
    output: activity_result
    prompt: |
      You are pulling daily GitHub activity for all team members in Team Pulse.
      This is an automated process — no user interaction needed.

      ## Step 1: Determine the Date

      {% if date != "" %}
      Use date: {{date}}
      {% else %}
      Run `date +%Y-%m-%d` to get today's date.
      {% endif %}

      Also determine yesterday's date for the "since" filter — we want activity
      from the last 24 hours (or since the date specified).

      ## Step 2: Read Org Structure

      1. **Read `org.yaml`** to get the full member list.
         - Collect all members with `role: ic` or `role: manager` (skip `program-leader`
           unless they have a profile.yaml with repos).
         - Note the lowercase directory name for each member:
           - "Chris P" → `chris`
           - "Gurkaran" → `gurkaran`
           - "Manoj" → `manoj`
           - "Ken" → `ken`
           - "Salil Das" → `salil`
           - "Samuel Lee" → `samuel`
           - "Alex Lopez" → `alex`

      2. **For each member, read `people/<name>/profile.yaml`** to get:
         - `github:` — list of GitHub handles (may be empty)
         - `repos:` — list of tracked repositories (may be empty)
         - `auto_discover:` — whether to scan for untracked repos

         If `github:` is empty or `repos:` is empty, skip that member and note
         it in the summary (e.g., "Salil: skipped — no GitHub handles configured").

      ## Step 3: Scan Repos for Each Member

      For each member who has GitHub handles and repos configured:

      **Account switching:** The `gh` CLI may have multiple accounts authenticated.
      Before scanning a repo, check which account is active with `gh auth status`.
      If the repo belongs to an org the active account can't access, switch:
      `gh auth switch --user <appropriate_handle>`
      If a scan fails with 404, try switching to the member's other handle and retry.

      For each repo in their `profile.yaml`, try **all** of the member's GitHub
      handles as the `--author` filter:

      **Merged PRs (since yesterday):**
      ```
      gh pr list --repo <owner/repo> --state merged --search "merged:>=<DATE>" --author <handle> --json number,title,mergedAt,headRefName --limit 50
      ```

      **Open PRs by this member:**
      ```
      gh pr list --repo <owner/repo> --state open --author <handle> --json number,title,createdAt,headRefName --limit 50
      ```

      **Recent commits on default branch:**
      ```
      gh api "repos/<owner/repo>/commits?since=<YESTERDAY>T00:00:00Z&until=<DATE>T23:59:59Z&author=<handle>" --jq '.[] | .sha[:7] + " " + .commit.message'
      ```

      Run for each handle. Merge results and deduplicate by PR number or commit SHA.

      If a command fails (repo not found, no permissions), note the error and
      continue — don't stop the entire pull.

      ## Step 4: Auto-Discover Untracked Repos

      **Only for members with `auto_discover: true` in their profile.yaml.**

      For each eligible member, check for activity in repos NOT in their `repos:` list:

      ```
      gh api "users/<handle>/events?per_page=100" --jq '[.[] | select(.created_at >= "<DATE>T00:00:00Z") | .repo.name] | unique | .[]'
      ```

      Run for each handle. Compare against their `repos:` list. Flag any untracked
      repos with a commit count:

      ```
      gh api "repos/<owner/repo>/commits?since=<YESTERDAY>T00:00:00Z&until=<DATE>T23:59:59Z&author=<handle>" --jq 'length'
      ```

      ## Step 5: Write Activity Files

      For each member who had any activity, write to:
      `people/<name>/activity/<DATE>.md`

      Use this exact format:

      ```
      # <Name> — Activity for <DATE>

      ## <owner/repo>

      ### Merged PRs
      - PR #<N> "<title>" (merged <date>)

      ### Open PRs
      - PR #<N> "<title>" (opened <date>, branch: <branch>)

      ### Commits
      - <sha> <message>

      ## <next repo>
      ...

      ## Untracked Repos
      Activity found in repos not in profile.yaml:
      - <owner/repo>: <N> commits
      ```

      Omit any section that has no data (e.g., if no merged PRs, skip that heading).
      Omit the "Untracked Repos" section entirely if auto_discover is false or no
      untracked repos were found.

      If a member had zero activity across all repos, do NOT create a file for them.

      ## Step 6: Commit and Push

      ```
      git add people/*/activity/
      git commit -m "activity: pull <DATE>"
      git push
      ```

      ## Step 7: Summary

      Report:
      - How many members were scanned
      - How many had activity (files written)
      - How many were skipped (no GitHub handles)
      - Any errors encountered
      - Any untracked repos flagged

      After all scanning, switch `gh auth` back to the originally active account.
```

**Step 2: Validate the recipe**

```bash
amplifier tool invoke recipes operation=validate recipe_path=@team-pulse:recipes/pull-activity.yaml
```

Expected: Validation passes with no errors.

---

### Task 10: Rewrite `recipes/log-commitments.yaml`

**Files:**
- Modify: `recipes/log-commitments.yaml` (full rewrite)

**What changes:** The V1 recipe reads `team.yaml` and writes to `weeks/<WEEK>/commitments/<name>.md`. The V2 recipe reads `org.yaml` + `people/<name>/profile.yaml` + `people/<name>/outcomes.md`, asks for a `drives:` field on each commitment, and writes to `people/<name>/weeks/<WEEK>/commitments.md`. It also updates `profile.yaml` (not `team.yaml`) when new repos are mentioned.

**Step 1: Replace the entire file**

Replace the contents of `recipes/log-commitments.yaml` with:

```yaml
name: log-commitments
description: >
  Weekly commitment entry for team members. Reads outcomes to prompt for
  drives: linking, surfaces carry-over from last week, captures commitments
  with outcomes, repos, and priorities, and writes to the person-centric
  data structure.
version: "0.2.0"
tags: ["commitments", "weekly", "team", "outcomes"]

# Usage:
#   "Log my commitments"
#   amplifier tool invoke recipes operation=execute recipe_path=@team-pulse:recipes/log-commitments.yaml
#   amplifier tool invoke recipes operation=execute recipe_path=@team-pulse:recipes/log-commitments.yaml context='{"member_name": "Ken"}'

context:
  member_name: ""  # Optional: auto-detected from git config if empty

steps:
  - id: log-commitments
    agent: self
    timeout: 600
    output: commitment_result
    prompt: |
      You are helping a team member log their weekly commitments for Team Pulse.

      ## Setup

      1. **Determine the current week:**
         - Run `date +%Y-W%V` to get the ISO week identifier (e.g., 2026-W12)
         - Run `date +%Y-%m-%d` to get today's date
         - Determine the Monday of this week for the file header

      2. **Identify the team member:**
         {% if member_name != "" %}
         - The member is: {{member_name}}
         {% else %}
         - Run `git config user.name` and `git config user.email` to detect the user
         {% endif %}
         - Read `org.yaml` and match the user to a member entry by name
         - Determine the lowercase directory name for this member:
           - "Chris P" → `chris`
           - "Gurkaran" → `gurkaran`
           - "Manoj" → `manoj`
           - "Ken" → `ken`
           - "Salil Das" → `salil`
           - "Samuel Lee" → `samuel`
           - "Alex Lopez" → `alex`
         - If no match found, show the member list from `org.yaml` and ask who they are

      3. **Read the member's profile and outcomes:**
         - Read `people/<name>/profile.yaml` to get their tracked repos
         - Read `people/<name>/outcomes.md` to get their current outcomes

      4. **Create the week folder** if it doesn't exist:
         - `mkdir -p people/<name>/weeks/<WEEK_ID>`

      ## Carry-Over Check

      5. **Find the previous week's commitment file** for this member:
         - List folders in `people/<name>/weeks/`, find the most recent one before the current week
         - Read `people/<name>/weeks/<PREV_WEEK>/commitments.md`
         - Any items still marked `- [ ]` (unchecked) are potential carry-over
         - If no previous week folder exists, this is their first week

      6. **Present carry-over to the user:**
         - If there are unchecked items from last week, show them
         - Ask which ones to carry forward this week
         - For carried items, record the originating week in the `carried-from` field
         - If this is their first week, say so

      ## Show Current Outcomes

      7. **Display the member's outcomes** from `people/<name>/outcomes.md`:
         - Show each outcome ID and description
         - Say: "These are your current outcomes. Each commitment should link
           to one of these via the `drives:` field. You can also say 'none'
           if something doesn't connect to an outcome — but I'll flag it."

      ## Gather Commitments

      8. **For each item, first ask: "Is this something you're planning to ship, or something you already shipped?"**

         **If planning to ship (future commitment):**
         - What is the commitment? (brief description)
         - What does "done" look like? (specific, measurable outcome)
         - Which outcome does this drive? (show outcomes from step 7 as options,
           or "none" — but flag unconnected work)
         - Which repo is it tied to? (show their repos from profile.yaml, or any owner/repo)
         - Is it must-ship or stretch?
         - Push for specific outcomes. If an outcome is vague (e.g., "work on feature X"),
           ask: "What would you show someone on Friday to prove this shipped?"

         **If already shipped:**
         - What did you ship? (brief description)
         - What was the outcome? (what was delivered — PR link, artifact, result)
         - Which outcome does this drive? (same as above)
         - Which repo?
         - Was it must-ship or stretch?
         - Write it as `- [x]` (already checked) with an `- evidence:` field instead of `- outcome:`

      9. **Keep prompting** until the user says they're done adding items

      ## Write the File

      10. **Write the commitment file** to:
         `people/<name>/weeks/<WEEK_ID>/commitments.md`

         Use this exact format:

         ```
         # <Name> -- Week of <MONDAY_DATE>
         Logged: <TODAY_DATE>

         ## Carried Forward

         <list carried items with "(from W<XX>)" note>
         <or "(none -- first week)" if none>

         ## Commitments

         - [ ] <future commitment description>
           - drives: <outcome_id>
           - outcome: <what done looks like>
           - repo: <owner/repo>
           - priority: must-ship
           - carried-from: <WEEK_ID>
         - [x] <already shipped item>
           - drives: <outcome_id>
           - evidence: <what was delivered — PR link, artifact, result>
           - repo: <owner/repo>
           - priority: must-ship
         - [ ] <another commitment>
           - drives: none
           - outcome: <outcome>
           - repo: <owner/repo>
           - priority: stretch
         ```

         Rules:
         - Every commitment MUST have a `drives:` field — either an outcome ID
           from their outcomes.md, or `none`
         - Only include `carried-from` on items carried from a previous week
         - `repo` and `outcome`/`evidence` are strongly encouraged but optional
         - Priority must be exactly `must-ship` or `stretch`
         - Future items use `- [ ]` with `outcome:` (what done looks like)
         - Already-shipped items use `- [x]` with `evidence:` (what was delivered)

      ## Update profile.yaml with New Repos

      11. **Check for new repos:** Compare every `repo:` value in the commitment file
         against this member's `repos:` list in `people/<name>/profile.yaml`.
         - If a repo is mentioned that's NOT already in their list, append it
           to the `repos:` array in `profile.yaml`.

      ## Commit and Push

      12. **Commit the file (and profile.yaml if updated):**
         - `git add people/<name>/weeks/<WEEK_ID>/commitments.md`
         - If `profile.yaml` was modified: `git add people/<name>/profile.yaml`
         - `git commit -m "commitments(<name>): log week <WEEK_ID>"`
         - `git push`

      ## Tone

      Be conversational and encouraging. Help the team member think about what
      "done" looks like for each commitment. When they provide a commitment
      without a `drives:` link, gently ask which outcome it supports — but
      accept "none" without making them feel bad. Celebrate carry-over honesty —
      acknowledging unfinished work is a feature, not a failure.
```

**Step 2: Validate the recipe**

```bash
amplifier tool invoke recipes operation=validate recipe_path=@team-pulse:recipes/log-commitments.yaml
```

Expected: Validation passes with no errors.

---

### Task 11: Create `recipes/set-outcomes.yaml`

**Files:**
- Create: `recipes/set-outcomes.yaml`

**What this recipe does:** A conversational recipe where a manager (or IC) defines quarterly outcomes for a person. It reads the current `outcomes.md`, chats about what the person should focus on, and writes the structured outcome file. Outcomes have a short ID (slug) and an observable, time-bounded description.

**Step 1: Create the recipe file**

Create `recipes/set-outcomes.yaml` with this exact content:

```yaml
name: set-outcomes
description: >
  Set or update quarterly outcomes for a team member. Conversationally
  gathers outcomes and writes them to the person-centric outcomes.md file.
  Each outcome gets a short ID and an observable, time-bounded description.
version: "0.1.0"
tags: ["outcomes", "quarterly", "planning"]

# Usage:
#   "Set outcomes for Ken"
#   amplifier tool invoke recipes operation=execute recipe_path=@team-pulse:recipes/set-outcomes.yaml context='{"member_name": "Ken"}'

context:
  member_name: ""  # Required: which member to set outcomes for

steps:
  - id: set-outcomes
    agent: self
    timeout: 300
    output: outcomes_result
    prompt: |
      You are helping set quarterly outcomes for a team member in Team Pulse.

      ## Step 1: Identify the Member

      {% if member_name != "" %}
      The member is: {{member_name}}
      {% else %}
      Ask the user: "Who are we setting outcomes for?"
      {% endif %}

      - Read `org.yaml` and match the name to a member entry
      - Determine the lowercase directory name:
        - "Chris P" → `chris`
        - "Gurkaran" → `gurkaran`
        - "Manoj" → `manoj`
        - "Ken" → `ken`
        - "Salil Das" → `salil`
        - "Samuel Lee" → `samuel`
        - "Alex Lopez" → `alex`

      ## Step 2: Read Current Outcomes

      Read `people/<name>/outcomes.md` if it exists. Show the user what's
      currently there:
      - If it's a placeholder ("Outcomes not yet defined"), say so
      - If it has real outcomes, list them and ask if they want to update,
        replace, or add to them

      ## Step 3: Determine the Quarter

      Run `date +%Y-%m-%d` to get today's date. Determine the current quarter
      (Q1 = Jan-Mar, Q2 = Apr-Jun, Q3 = Jul-Sep, Q4 = Oct-Dec) and year.

      ## Step 4: Gather Outcomes

      Ask the user to describe this person's focus areas. Accept natural
      language — for example:
      - "Ken's focus this quarter is LifeOS adoption and building the eval system"
      - "Manoj needs to finish the CLI migration and start on the new plugin architecture"

      For each outcome mentioned, extract or collaboratively define:

      1. **Short ID (slug):** A kebab-case identifier like `lifeos-adoption`,
         `cli-migration`, `experimentation`. Suggest one and let the user adjust.

      2. **Observable description:** What does success look like? Push for
         specificity. If they say "work on LifeOS", ask "what would tell you
         LifeOS adoption is going well — installs? retention? active users?"

         Good: "LifeOS is actively used by 5+ people beyond Ken, with retention past first week."
         Bad: "Make LifeOS better."

      3. **Experimentation is always valid.** If someone has exploratory work,
         suggest an `experimentation` outcome like:
         "Ship 2+ exploratory projects this quarter that test new ideas."

      Keep asking until the user is done. Confirm the final list before writing.

      ## Step 5: Write the File

      Write to `people/<name>/outcomes.md` using this exact format:

      ```
      # <Name> -- <Q#> <YEAR> Outcomes

      ## <outcome-slug-1>
      <Observable, time-bounded description>

      ## <outcome-slug-2>
      <Observable, time-bounded description>

      ## experimentation
      <Description if applicable>
      ```

      Rules:
      - The `##` heading IS the outcome ID — it must be kebab-case
      - The paragraph under each heading is the description
      - No bullet points, no sub-sections — just the ID heading and a description paragraph
      - This format is what other recipes parse to get outcome IDs and descriptions

      ## Step 6: Commit and Push

      ```
      git add people/<name>/outcomes.md
      git commit -m "outcomes(<name>): set <Q#> <YEAR> outcomes"
      git push
      ```

      ## Tone

      Be collaborative, not bureaucratic. This should feel like a planning
      conversation, not a form to fill out. Help the user articulate what
      success looks like in concrete terms.
```

**Step 2: Validate the recipe**

```bash
amplifier tool invoke recipes operation=validate recipe_path=@team-pulse:recipes/set-outcomes.yaml
```

Expected: Validation passes with no errors.

---

### Task 12: Update `context/team-pulse-instructions.md`

**Files:**
- Modify: `context/team-pulse-instructions.md` (full rewrite)

**What changes:** This file tells the bundle agent which recipe to run for which user command. We need to add routing for the new recipes (`pull-activity`, `set-outcomes`) and update existing ones (`log-commitments` — same path but new behavior, `prep-audit`, `draft-showcase`). We also remove the `setup` recipe routing since that recipe was deleted.

**Step 1: Replace the entire file**

Replace the contents of `context/team-pulse-instructions.md` with:

```markdown
# Team Pulse — Available Workflows

You are operating as part of the Team Pulse bundle. When a user triggers one of these workflows, use the `recipes` tool to execute the recipe. Do NOT attempt to perform the workflow yourself — the recipes handle multi-step orchestration.

**Catch-all rule:** If the user mentions commitments, audits, showcases, activity, outcomes, or weekly updates in a way that matches any workflow below, default to running the appropriate recipe.

## Pull Activity (Daily, automated or manual)

Scans each team member's tracked GitHub repos for commits and PRs. Writes per-person daily activity files to `people/<name>/activity/<date>.md`.

**Run with the recipes tool:**
```
recipes(operation="execute", recipe_path="@team-pulse:recipes/pull-activity.yaml")
```

**For a specific date:**
```
recipes(operation="execute", recipe_path="@team-pulse:recipes/pull-activity.yaml", context={"date": "2026-03-18"})
```

**When the user says:** "pull activity", "pull today's activity", "scan repos", "what happened today", "daily pull"

## Log Commitments (Weekly, each team member)

Captures weekly commitments with outcomes, repos, and priorities. Each commitment links to a quarterly outcome via the `drives:` field. Surfaces carry-over from the previous week automatically.

**Run with the recipes tool:**
```
recipes(operation="execute", recipe_path="@team-pulse:recipes/log-commitments.yaml")
```

**With a specific member name:**
```
recipes(operation="execute", recipe_path="@team-pulse:recipes/log-commitments.yaml", context={"member_name": "Ken"})
```

**When the user says:** "log my commitments", "log commitments", "what am I committing to this week", "weekly commitments", "log commitments for Ken"

## Set Outcomes (Quarterly, manager or IC)

Sets or updates quarterly outcomes for a team member. Conversational — gathers outcomes in natural language and writes structured `outcomes.md`.

**Run with the recipes tool:**
```
recipes(operation="execute", recipe_path="@team-pulse:recipes/set-outcomes.yaml", context={"member_name": "Ken"})
```

**When the user says:** "set outcomes for Ken", "update Ken's outcomes", "define outcomes", "what should Ken focus on this quarter"

## Prep Audit (Weekly, automated or manager-triggered)

Scans tracked repos for activity via `gh` CLI, matches against commitments and outcomes, generates per-person audits, team views, and manager rollups.

**Run with the recipes tool:**
```
recipes(operation="execute", recipe_path="@team-pulse:recipes/prep-audit.yaml")
```

**For a specific week:**
```
recipes(operation="execute", recipe_path="@team-pulse:recipes/prep-audit.yaml", context={"week": "2026-W12"})
```

**When the user says:** "prep the audit", "run the audit", "generate audit", "show me the audit", "prep my 1:1 with Ken"

## Draft Showcase (Weekly, manager)

Generates outcome-first team and leadership showcases. Includes narrative rollup for Sam. Posts to Teams on manager approval. This is a staged recipe — the manager reviews drafts before they are posted.

**Run with the recipes tool:**
```
recipes(operation="execute", recipe_path="@team-pulse:recipes/draft-showcase.yaml")
```

**When the user says:** "draft the showcase", "generate showcases", "send the update", "post to Teams", "prep Sam's rollup"

## Process Standup (As needed, manager)

Extracts per-person commitments, status updates, and blockers from a pasted transcript or meeting notes. Writes to each person's commitment file.

**Run with the recipes tool:**
```
recipes(operation="execute", recipe_path="@team-pulse:recipes/process-standup.yaml")
```

**When the user says:** "process this standup", "process this transcript", "extract commitments from this meeting", "parse these meeting notes"
```

**Step 2: Verify**

Read back the file and confirm:
- 6 workflows listed (pull-activity, log-commitments, set-outcomes, prep-audit, draft-showcase, process-standup)
- No reference to `setup` recipe
- No reference to `team.yaml` — all recipes now reference `org.yaml` and `people/` structure

---

### Task 13: Commit Phase 2

**Step 1: Validate all recipes**

```bash
amplifier tool invoke recipes operation=validate recipe_path=@team-pulse:recipes/pull-activity.yaml
amplifier tool invoke recipes operation=validate recipe_path=@team-pulse:recipes/log-commitments.yaml
amplifier tool invoke recipes operation=validate recipe_path=@team-pulse:recipes/set-outcomes.yaml
```

All three should pass validation.

**Step 2: Review and commit**

```bash
git add -A
git status
```

You should see:
- **New files:** `recipes/pull-activity.yaml`, `recipes/set-outcomes.yaml`
- **Modified files:** `recipes/log-commitments.yaml`, `context/team-pulse-instructions.md`

```bash
git commit -m "feat: add pull-activity and set-outcomes recipes, update log-commitments for outcomes

- Create pull-activity recipe (daily GitHub activity scan per person)
- Create set-outcomes recipe (quarterly outcome setting via natural language)
- Rewrite log-commitments to read org.yaml/profile.yaml, add drives: field
- Update context routing for all new and updated commands"
```

```bash
git push
```

---

## Phase 3: Views, Showcases, Transcript Processing

This phase rewrites the audit and showcase recipes for outcome-first framing, creates the transcript processing recipe, and updates the bundle manifest and backlog. After this phase, the full V2 system is operational.

---

### Task 14: Rewrite `recipes/prep-audit.yaml`

**Files:**
- Modify: `recipes/prep-audit.yaml` (full rewrite)

**What changes:** V1 reads `team.yaml`, scans repos, writes one flat `weeks/<WEEK>/audit.md`. V2 reads `org.yaml` + person data, groups results by **outcome** (not just by person), generates per-person audit files, team views, and a manager rollup. It also tracks an "Alignment %" metric (commitments with `drives:` / total commitments).

**Step 1: Replace the entire file**

Replace the contents of `recipes/prep-audit.yaml` with:

```yaml
name: prep-audit
description: >
  Outcome-first weekly audit. Scans repos for activity, matches against
  commitments and outcomes, generates per-person audits, team views, and
  manager rollups. Tracks alignment (% commitments tied to outcomes).
version: "0.2.0"
tags: ["audit", "weekly", "automation", "outcomes"]

# Usage:
#   "Prep the audit"
#   amplifier tool invoke recipes operation=execute recipe_path=@team-pulse:recipes/prep-audit.yaml
#   amplifier tool invoke recipes operation=execute recipe_path=@team-pulse:recipes/prep-audit.yaml context='{"week": "2026-W12"}'

context:
  week: ""  # Optional: defaults to current ISO week

steps:
  - id: prepare-audit
    agent: self
    timeout: 900
    output: audit_result
    prompt: |
      You are preparing the weekly outcome-first audit for Team Pulse. This is
      an automated process — no user interaction needed. Read data, scan repos,
      match activity against commitments and outcomes, and generate audit views.

      ## Step 1: Determine the Week

      {% if week != "" %}
      Use week: {{week}}
      {% else %}
      Run `date +%Y-W%V` to get the current ISO week identifier.
      {% endif %}

      Calculate the Monday and Sunday dates for this week.

      ## Step 2: Read Org Structure and Person Data

      1. **Read `org.yaml`** to get:
         - Full member list with roles and reporting structure
         - Team definitions (which members belong to which team)
         - Showcase config

      2. **For each IC and manager member**, determine their lowercase directory name:
         - "Chris P" → `chris`, "Gurkaran" → `gurkaran`, "Manoj" → `manoj`
         - "Ken" → `ken`, "Salil Das" → `salil`, "Samuel Lee" → `samuel`
         - "Alex Lopez" → `alex`

      3. **For each member, read:**
         - `people/<name>/profile.yaml` — GitHub handles, repos, auto_discover
         - `people/<name>/outcomes.md` — quarterly outcomes (IDs and descriptions)
         - `people/<name>/weeks/<WEEK_ID>/commitments.md` — this week's commitments
         - `people/<name>/activity/*.md` — daily activity files for this week
           (list files in the activity directory, read those whose dates fall
           within Monday-Sunday of the target week)

         If any file doesn't exist, note it and continue.

      ## Step 3: Scan Repos for Activity (if no daily activity files exist)

      If daily activity files exist for a member (from the `pull-activity` recipe),
      use that data — do NOT re-scan repos.

      If no activity files exist for a member, fall back to scanning their repos
      directly (same logic as the pull-activity recipe):

      For each member with GitHub handles and repos configured, try all handles:

      **Merged PRs this week:**
      ```
      gh pr list --repo <owner/repo> --state merged --search "merged:>=<MONDAY>" --author <handle> --json number,title,mergedAt,headRefName --limit 50
      ```

      **Open PRs:**
      ```
      gh pr list --repo <owner/repo> --state open --author <handle> --json number,title,createdAt,headRefName --limit 50
      ```

      **Recent commits:**
      ```
      gh api "repos/<owner/repo>/commits?since=<MONDAY>T00:00:00Z&until=<SUNDAY>T23:59:59Z&author=<handle>" --jq '.[] | .sha[:7] + " " + .commit.message'
      ```

      Handle account switching as needed. Merge and deduplicate results.

      **Auto-discover** for members with `auto_discover: true`:
      ```
      gh api "users/<handle>/events?per_page=100" --jq '[.[] | select(.created_at >= "<MONDAY>T00:00:00Z") | .repo.name] | unique | .[]'
      ```

      ## Step 4: Match Activity Against Commitments

      For each member's commitments:

      - **Shipped** — PR merged whose title, branch name, or commit messages relate
        to the commitment's description or outcome
      - **Partial** — Activity exists but incomplete: open PR, WIP branch, partial work
      - **No activity** — Nothing found matching this commitment
      - **Unmatched** — Commitment has no repo tag; cannot assess automatically

      Be generous with matching. Use PR titles, branch names, and commit messages.

      For members who didn't log commitments: note "no commitments logged" but
      still report any repo activity under "Unmatched Activity".

      ## Step 5: Calculate Metrics

      For each member, calculate:
      - **Must-ship total** and **shipped count**
      - **Alignment %** = (commitments with a `drives:` field that is NOT "none") / (total commitments) × 100

      For each team, aggregate:
      - Total outcomes, on-track count, at-risk count
      - Team alignment % (average of member alignment)

      ## Step 6: Write Per-Person Audit Files

      For each member, write to:
      `people/<name>/weeks/<WEEK_ID>/audit.md`

      ```
      # <Name> -- Audit for Week of <MONDAY_DATE>

      ## Outcome Progress

      ### <outcome-id>: <outcome description snippet>
      Status: <On track / At risk / No activity>
      Commitments driving this outcome:
      - <commitment> — <Shipped/Partial/No activity> — <evidence>

      ### <next outcome>
      ...

      ## Unconnected Work
      Commitments with drives: none
      - <commitment> — <status> — <evidence>

      ## Unmatched Activity
      Activity not tied to any commitment:
      - <repo>: PR #<N> "<title>" merged

      ## Untracked Repos
      Activity in repos not in profile.yaml:
      - <owner/repo>: <N> commits

      ## Scorecard
      Must-ship: <shipped>/<total> (<rate>%)
      Alignment: <alignment>%
      ```

      Omit any section with no data.

      ## Step 7: Write Team Audit View

      For each team in `org.yaml`, write to:
      `views/teams/<team>/<WEEK_ID>-audit.md`

      Group by OUTCOME, not by person:

      ```
      # <Team> Team -- Audit for Week of <MONDAY_DATE>

      ## Outcome: <outcome-id>
      Owner(s): <who has commitments driving this>
      Status: <On track / At risk / Stalled>
      This week:
      - <person>: <commitment> — <Shipped/Partial>
      - <person>: <commitment> — <No activity>

      ## Outcome: <next outcome>
      ...

      ## Unconnected Work
      - <person>: <commitment> — drives: none

      ## Team Scorecard
      | Member | Must-Ship | Shipped | Rate | Alignment |
      |--------|-----------|---------|------|-----------|
      | <name> | <N>       | <N>     | <N>% | <N>%      |
      ```

      ## Step 8: Write Manager Rollup

      For each manager in `org.yaml`, write to:
      `views/managers/<lowercase_manager_first_name>/<WEEK_ID>-rollup.md`

      ```
      # <Manager>'s Team -- Week of <MONDAY_DATE>

      ## Outcomes Summary
      | Outcome | Owner | Status | Weeks Active |
      |---------|-------|--------|-------------|
      | <outcome> | <person> | <status> | <N> |

      ## Needs Attention
      - <outcome>: <why it needs attention>

      ## Member Scorecard
      | Member | Must-Ship | Shipped | Rate | Alignment |
      |--------|-----------|---------|------|-----------|
      | <name> | <N>       | <N>     | <N>% | <N>%      |

      ## Unconnected Work
      - <person>: <commitment with drives: none>
      ```

      For "Weeks Active", count how many consecutive weeks this outcome has had
      at least one commitment — look back through previous week folders.

      ## Step 9: Update CHANGELOG.md

      Calculate the scorecard and append a new row to `CHANGELOG.md`:

      ```
      | <WEEK_SHORT> | <must_ship> | <shipped> | <rate>% | <carried> | <alignment>% |
      ```

      If the CHANGELOG table doesn't have an Alignment column yet, add it to
      the header row first:
      ```
      | Week | Must-Ship | Shipped | Rate | Carried Forward | Alignment |
      |------|-----------|---------|------|-----------------|-----------|
      ```

      ## Step 10: Commit and Push

      ```
      git add people/*/weeks/*/audit.md views/ CHANGELOG.md
      git commit -m "audit: generate week <WEEK_ID>"
      git push
      ```
```

**Step 2: Validate the recipe**

```bash
amplifier tool invoke recipes operation=validate recipe_path=@team-pulse:recipes/prep-audit.yaml
```

Expected: Validation passes with no errors.

---

### Task 15: Rewrite `recipes/draft-showcase.yaml`

**Files:**
- Modify: `recipes/draft-showcase.yaml` (full rewrite)

**What changes:** V1 generates a team celebration post and a leadership scorecard from `weeks/<WEEK>/audit.md`. V2 generates outcome-first showcases: the team showcase groups by outcome progress (not by person), and the leadership showcase for Sam leads with a **narrative paragraph** explaining what each team does, why work matters, and what needs attention — followed by structured tables.

**Step 1: Replace the entire file**

Replace the contents of `recipes/draft-showcase.yaml` with:

```yaml
name: draft-showcase
description: >
  Generates outcome-first team and leadership showcases. Team showcase
  groups by outcome progress. Leadership rollup for Sam leads with a
  narrative paragraph for context. Staged recipe: manager reviews before posting.
version: "0.2.0"
tags: ["showcase", "weekly", "teams", "staged", "outcomes"]

# Usage:
#   "Draft the showcase"
#   amplifier tool invoke recipes operation=execute recipe_path=@team-pulse:recipes/draft-showcase.yaml
#   amplifier tool invoke recipes operation=execute recipe_path=@team-pulse:recipes/draft-showcase.yaml context='{"week": "2026-W12"}'

context:
  week: ""  # Optional: defaults to current ISO week

stages:
  - name: "drafting"
    steps:
      - id: generate-showcases
        agent: self
        timeout: 600
        output: showcase_summary
        prompt: |
          Generate outcome-first showcases from the weekly audit data: a team
          showcase, and a leadership narrative rollup for Sam.

          ## Step 1: Determine the Week

          {% if week != "" %}
          Use week: {{week}}
          {% else %}
          Run `date +%Y-W%V` to get the current ISO week identifier.
          {% endif %}

          Calculate Monday date for headers.

          ## Step 2: Read Inputs

          1. **Read `org.yaml`** — for team structure, showcase config, members
          2. **For each member, read:**
             - `people/<name>/outcomes.md` — quarterly outcomes
             - `people/<name>/weeks/<WEEK_ID>/audit.md` — this week's audit
             - `people/<name>/weeks/<WEEK_ID>/commitments.md` — commitments
          3. **Read team audit view:** `views/teams/workspaces/<WEEK_ID>-audit.md`
          4. **Read manager rollup:** `views/managers/chris/<WEEK_ID>-rollup.md`
          5. **Read `CHANGELOG.md`** — for trend data (last 3+ weeks)

          If audit files don't exist yet, tell the user to run `prep-audit` first
          and stop.

          ## Step 3: Generate Team Showcase

          Write to `showcases/workspaces/<WEEK_ID>-team.md`

          This is an outcome-first showcase — group by outcome, not by person.
          Tone: celebratory and specific.

          Use this format:

          ```
          # Workspaces Team -- Week of <MONDAY_DATE>

          ## Outcome: <outcome-id>
          Status: <On track / At risk / Shipped>
          This week: <narrative of what happened — name people and what they did>

          ## Outcome: <next outcome>
          ...

          ## Experimentation Highlights
          - **<Name>** shipped <thing> — <why it's cool>
          - **<Name>** explored <thing> — <what came of it>

          ## Carried Forward
          - <item rolling to next week>

          ## Scorecard
          Must-ship: <shipped>/<total> (<rate>%)
          Alignment: <alignment>%
          ```

          ## Step 4: Generate Leadership Rollup for Sam

          Write to `views/leadership/sam/<WEEK_ID>-rollup.md`

          **This is the most important output.** Sam doesn't know what these
          projects are. The rollup MUST lead with a narrative paragraph that:
          - Explains what each team works on and why it matters
          - Highlights what's on track
          - Flags what needs attention and why
          - Calls out experimentation wins

          Sam should be able to read the first two paragraphs and understand the
          state of the org in 30 seconds.

          Use this exact format:

          ```
          # Sam's Org -- Week of <MONDAY_DATE>

          <Narrative paragraph 1: What Chris's team is focused on. What's on
          track — name the outcomes and why they matter. What's concerning —
          explain the situation, not just "at risk".>

          <Narrative paragraph 2: Experimentation highlights. What was shipped
          that shows the team is building real tools. Keep it concrete — names,
          artifacts, impact.>

          ## Outcomes Summary

          | Outcome | Owner | Status | Weeks Active |
          |---------|-------|--------|-------------|
          | <outcome> | <person> | <On track/At risk/Stalled> | <N> |

          ## Needs Attention
          - <outcome>: <explanation of why and suggested action>

          ## Team Health
          | Manager | Outcomes | On Track | At Risk | Alignment |
          |---------|----------|----------|---------|-----------| 
          | Chris   | <N>      | <N>      | <N>     | <N>%      |
          ```

          The "Needs Attention" section should have specific, actionable items —
          not just "X is at risk" but "X is at risk because Y, consider Z."

          For "Weeks Active", count consecutive weeks with at least one commitment
          for that outcome.

          ## Step 5: Create directories if needed

          ```
          mkdir -p showcases/workspaces
          mkdir -p views/leadership/sam
          ```

          ## Output

          After writing both files, summarize:
          - Path to team showcase
          - Path to leadership rollup
          - Key stats (ship rate, alignment, risk items)

    approval:
      required: true
      prompt: |
        ## Showcase Drafts Ready for Review

        {{showcase_summary}}

        **Review the generated files** and edit directly if needed.

        When you're satisfied, **approve to post to Teams**.
        Reply "approve" to post, or edit the files first and then approve.

  - name: "posting"
    steps:
      - id: post-to-teams
        agent: self
        timeout: 120
        output: posting_result
        prompt: |
          Post the finalized showcases to Teams via webhooks.

          ## Step 1: Read Config

          Read `org.yaml` to get the webhook URLs from the `showcase:` section:
          - `showcase.workspaces.channel` — team webhook URL
          - `showcase.leadership.channel` — leadership webhook URL
          - `showcase.org-wide.channel` — org-wide webhook URL (if applicable)

          Resolve environment variable names (e.g., `$TEAM_PULSE_TEAM_WEBHOOK`)
          by reading the actual env var value.

          ## Step 2: Determine the Week

          {% if week != "" %}
          Use week: {{week}}
          {% else %}
          Run `date +%Y-W%V` to get the current ISO week identifier.
          {% endif %}

          ## Step 3: Post Team Showcase

          Read `showcases/workspaces/<WEEK_ID>-team.md`.

          Convert to a Teams Adaptive Card JSON payload:
          ```json
          {
            "type": "message",
            "attachments": [
              {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                  "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                  "type": "AdaptiveCard",
                  "version": "1.4",
                  "body": [
                    {
                      "type": "TextBlock",
                      "text": "<TITLE>",
                      "weight": "Bolder",
                      "size": "Large"
                    },
                    {
                      "type": "TextBlock",
                      "text": "<BODY_CONTENT>",
                      "wrap": true
                    }
                  ]
                }
              }
            ]
          }
          ```

          Post via curl:
          ```
          curl -X POST -H "Content-Type: application/json" -d @/tmp/team-showcase.json "$TEAM_PULSE_TEAM_WEBHOOK"
          ```

          ## Step 4: Post Leadership Rollup

          Read `views/leadership/sam/<WEEK_ID>-rollup.md`.
          Same Adaptive Card process, post to `$TEAM_PULSE_LEADERSHIP_WEBHOOK`.

          ## Step 5: Commit and Push

          ```
          git add showcases/ views/
          git commit -m "showcase: post week <WEEK_ID>"
          git push
          ```

          ## Error Handling

          If a webhook URL is not set (env var empty or missing), skip that
          posting and report it. Don't fail the entire step — post what you can.

          Report what was posted successfully and any errors.
```

**Step 2: Validate the recipe**

```bash
amplifier tool invoke recipes operation=validate recipe_path=@team-pulse:recipes/draft-showcase.yaml
```

Expected: Validation passes with no errors.

---

### Task 16: Create `recipes/process-standup.yaml`

**Files:**
- Create: `recipes/process-standup.yaml`

**What this recipe does:** Takes a pasted transcript (or file path to a `.vtt`/`.txt`) from a standup or 1:1, identifies speakers, extracts per-person commitments and status updates, matches them to outcomes, and writes commitment files. The manager reviews extracted data before it's written.

**Step 1: Create the recipe file**

Create `recipes/process-standup.yaml` with this exact content:

```yaml
name: process-standup
description: >
  Extracts per-person commitments, status updates, and blockers from a
  pasted transcript or meeting notes. Matches extracted commitments to
  outcomes and writes commitment files after manager review.
version: "0.1.0"
tags: ["standup", "transcript", "commitments", "extraction"]

# Usage:
#   "Process this standup" (then paste the transcript)
#   amplifier tool invoke recipes operation=execute recipe_path=@team-pulse:recipes/process-standup.yaml

context:
  transcript_path: ""  # Optional: path to a .vtt or .txt file. If empty, asks user to paste.

steps:
  - id: process-standup
    agent: self
    timeout: 600
    output: standup_result
    prompt: |
      You are extracting per-person data from a standup or meeting transcript
      for Team Pulse.

      ## Step 1: Get the Transcript

      {% if transcript_path != "" %}
      Read the transcript from: {{transcript_path}}
      {% else %}
      Ask the user to paste the transcript or provide a file path.
      Accept: raw text, .vtt content, or a file path to read.
      {% endif %}

      ## Step 2: Read Org and Outcomes Data

      1. **Read `org.yaml`** to get the member list — you'll use names to
         identify speakers in the transcript.
      2. **For each member**, read `people/<name>/outcomes.md` to get their
         current outcomes. You'll need these to match extracted commitments
         to outcomes.

         Member directory mapping:
         - "Chris P" → `chris`
         - "Gurkaran" → `gurkaran`
         - "Manoj" → `manoj`
         - "Ken" → `ken`
         - "Salil Das" → `salil`
         - "Samuel Lee" → `samuel`
         - "Alex Lopez" → `alex`

      ## Step 3: Determine the Week

      Run `date +%Y-W%V` to get the current ISO week identifier.
      Run `date +%Y-%m-%d` to get today's date.
      Determine Monday of this week for file headers.

      ## Step 4: Extract Per-Person Data

      Parse the transcript and extract for each identified speaker:

      1. **What they're working on** → these become commitments (future, `- [ ]`)
      2. **What they shipped/completed** → these become shipped items (`- [x]`)
      3. **Blockers mentioned** → note these for the manager

      For each extracted commitment or shipped item:
      - Try to match it to an outcome from their `outcomes.md`
      - Set the `drives:` field to the matching outcome ID, or `none` if no match
      - Infer the repo if mentioned, otherwise leave repo blank
      - Default priority to `must-ship` unless context suggests otherwise

      Handle ambiguity:
      - If you can't identify a speaker, group their text under "Unknown Speaker"
      - If a statement is ambiguous (not clearly a commitment or status update),
        include it with a "?" note for the manager to resolve

      ## Step 5: Present Extracted Data for Review

      Show the manager what you extracted, organized by person:

      ```
      ## Ken
      Commitments:
      - [ ] Build eval harness for LifeOS
        - drives: lifeos-eval (matched from outcomes)
        - repo: kenotron-ms/lifeos
        - priority: must-ship
      - [x] Shipped agent-daemon v0.2.9
        - drives: experimentation (matched from outcomes)
        - evidence: mentioned SSE live log streaming
        - repo: kenotron-ms/agent-daemon
      Blockers:
      - (none mentioned)

      ## Gurkaran
      ...
      ```

      Ask the manager:
      - "Does this look right? I can adjust any item."
      - "Any items I should add, remove, or re-categorize?"
      - "Should I write these to the commitment files?"

      Wait for confirmation before writing.

      ## Step 6: Check for Existing Commitments

      Before writing, check if each member already has a commitment file for
      this week at `people/<name>/weeks/<WEEK_ID>/commitments.md`.

      - If YES: read the existing file and MERGE — add new items, update
        status of existing items if the transcript shows they shipped. Do NOT
        overwrite existing commitments.
      - If NO: create a new file.

      ## Step 7: Write Commitment Files

      For each person with extracted data, write to:
      `people/<name>/weeks/<WEEK_ID>/commitments.md`

      Use the standard commitment format:

      ```
      # <Name> -- Week of <MONDAY_DATE>
      Logged: <TODAY_DATE> (from standup transcript)

      ## Carried Forward

      <carried items if merging with existing file, or "(none)" if new>

      ## Commitments

      - [ ] <commitment description>
        - drives: <outcome_id or none>
        - outcome: <what done looks like>
        - repo: <owner/repo>
        - priority: must-ship
      - [x] <shipped item>
        - drives: <outcome_id or none>
        - evidence: <what was delivered>
        - repo: <owner/repo>
        - priority: must-ship
      ```

      ## Step 8: Update profile.yaml with New Repos

      For each person, check if any new repos were mentioned. If so, add them
      to `people/<name>/profile.yaml`.

      ## Step 9: Commit and Push

      ```
      git add people/*/weeks/*/commitments.md people/*/profile.yaml
      git commit -m "commitments: extract from standup transcript <WEEK_ID>"
      git push
      ```

      ## Step 10: Summary

      Report:
      - How many people had data extracted
      - How many commitments total (future + shipped)
      - How many were matched to outcomes vs. unconnected
      - Any blockers flagged
      - Any ambiguous items that need follow-up
```

**Step 2: Validate the recipe**

```bash
amplifier tool invoke recipes operation=validate recipe_path=@team-pulse:recipes/process-standup.yaml
```

Expected: Validation passes with no errors.

---

### Task 17: Update `context/team-pulse-instructions.md` with final routing

**Files:**
- Modify: `context/team-pulse-instructions.md`

**What changes:** The file was already rewritten in Task 12 with placeholder entries for `process-standup` and `prep-audit`. Now verify it's complete and add any additional trigger phrases. Also add a note about the `prep my 1:1 with <name>` pattern which routes to `prep-audit` with a member filter.

**Step 1: Add 1:1 prep routing**

Add the following section to the end of the Prep Audit section in `context/team-pulse-instructions.md` (right after the existing "When the user says" line for prep-audit):

Find this line in the Prep Audit section:
```
**When the user says:** "prep the audit", "run the audit", "generate audit", "show me the audit", "prep my 1:1 with Ken"
```

Add this paragraph right after it:

```markdown

**1:1 Prep shortcut:** When the user says "prep my 1:1 with <name>", run prep-audit and then show only that person's audit data from `people/<name>/weeks/<WEEK>/audit.md`. This is a filtered view of the same audit, not a separate recipe.
```

**Step 2: Verify**

Read back the file and confirm all 6 workflows are listed with correct recipe paths.

---

### Task 18: Update `bundle.md`

**Files:**
- Modify: `bundle.md`

**What changes:** Update the description and workflow list to reflect V2 (6 recipes instead of 4, outcome-driven framing).

**Step 1: Update the bundle manifest**

Replace the current content of `bundle.md` with:

```markdown
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
```

**Step 2: Verify**

Read back the file and confirm:
- Version is `0.2.0`
- 6 recipes listed
- Data model section describes the three layers
- Includes are unchanged
- Context references are unchanged

---

### Task 19: Update `BACKLOG.md`

**Files:**
- Modify: `BACKLOG.md`

**What changes:** Mark the V2 migration as completed. Add V2 and V3 items as future work.

**Step 1: Update the backlog**

Replace the contents of `BACKLOG.md` with:

```markdown
# Product Backlog

**Purpose:** Outcome-driven weekly accountability for multi-team orgs — outcomes, commitments, activity pull, audit, showcase.
**Owner:** Chris Park
**Last Updated:** 2026-03-18

---

## Current Status Summary

**3 epics tracked:** 2 complete, 1 planned

- V1 core loop (commitments, audit, showcase) — shipped
- V2 outcome-driven multi-team (migration, daily pull, outcomes, narrative showcase) — shipped
- V2 polish + V3 website — planned

### Active Work

| Item | Owner | Status | Notes |
|------|-------|--------|-------|
| (none) | | | |

### Recently Completed

| Item | Owner | Completed | Notes |
|------|-------|-----------|-------|
| V2: Person-centric data migration | Chris | 2026-03-18 | org.yaml + people/ directories |
| V2: Daily activity pull recipe | Chris | 2026-03-18 | pull-activity.yaml |
| V2: Outcome setting recipe | Chris | 2026-03-18 | set-outcomes.yaml |
| V2: Log commitments with drives: field | Chris | 2026-03-18 | Links commitments to outcomes |
| V2: Outcome-first audit | Chris | 2026-03-18 | Groups by outcome, alignment metric |
| V2: Narrative showcase for leadership | Chris | 2026-03-18 | Sam's rollup with narrative paragraph |
| V2: Standup transcript processing | Chris | 2026-03-18 | process-standup.yaml |
| Multi-handle GitHub support | Chris | 2026-03-18 | Personal + Microsoft accounts per member |
| Auto-discover flag | Chris | 2026-03-18 | Per-member opt-in for untracked repo discovery |
| Auto-populate repos from commitments | Chris | 2026-03-18 | New repos auto-added to profile.yaml |
| Doc-driven-dev setup | Chris | 2026-03-18 | Lean tier docs structure scaffolded |

---

## Prioritized Future Work

### Immediate Next

| # | Item | Effort | Impact | Why Now |
|---|------|--------|--------|---------|
| 1 | CLI identity filtering (V2) | M | H | Different views per person based on git config → org.yaml lookup |
| 2 | Define real outcomes for all 7 ICs | S | H | Placeholder outcomes need to be replaced with real Q1 goals |
| 3 | Collect GitHub handles for Salil, Samuel, Alex | S | H | Activity pull can't run for them until configured |

### Near-term

| # | Item | Effort | Impact | Rationale |
|---|------|--------|--------|-----------|
| 1 | Grant mechanism recipe | S | M | "Grant Brian access to workspaces" — adds to org.yaml grants |
| 2 | Month/quarter rollup recipe | M | H | "What did we accomplish this quarter?" — no answer today |
| 3 | Automated scheduling (GitHub Action) | M | M | Daily pull without someone's laptop |

### Long-term (V3)

- Website with authentication (Microsoft SSO or GitHub OAuth)
- Real access controls (repo is data store, website is read layer)
- Cross-org aggregation
- Integration with external project trackers

---

## Change History

| Version | Date | Person | Changes |
|---------|------|--------|---------|
| v2.0 | 2026-03-18 | Chris | V2 outcome-driven multi-team migration |
| v1.0 | 2026-03-18 | Chris | Initial backlog from first working session |
```

**Step 2: Verify**

Read back the file and confirm V2 items appear in "Recently Completed" and V2/V3 items appear in "Future Work".

---

### Task 20: Update `CHANGELOG.md` and add Alignment column

**Files:**
- Modify: `CHANGELOG.md`

**What changes:** Add the Alignment column to the scorecard table header, since the V2 audit now tracks alignment percentage.

**Step 1: Update the table header**

Replace the contents of `CHANGELOG.md` with:

```markdown
# Changelog

| Week | Must-Ship | Shipped | Rate | Carried Forward | Alignment |
|------|-----------|---------|------|-----------------|-----------|
```

**Step 2: Verify**

Read back the file and confirm the table header now includes the Alignment column.

---

### Task 21: Update `.env.example` with new webhook

**Files:**
- Modify: `.env.example`

**What changes:** Add the org-wide webhook from `org.yaml`'s showcase config.

**Step 1: Update the file**

Replace the contents of `.env.example` with:

```
# Teams Webhook URLs for showcase posting
# Get these from Teams channel > Connectors > Incoming Webhook
TEAM_PULSE_TEAM_WEBHOOK=https://outlook.office.com/webhook/YOUR_TEAM_WEBHOOK_URL
TEAM_PULSE_LEADERSHIP_WEBHOOK=https://outlook.office.com/webhook/YOUR_LEADERSHIP_WEBHOOK_URL
TEAM_PULSE_ORG_WEBHOOK=https://outlook.office.com/webhook/YOUR_ORG_WEBHOOK_URL
```

**Step 2: Verify**

Read back the file and confirm all three webhook env vars are listed.

---

### Task 22: Final commit for Phase 3

**Step 1: Validate all recipes**

```bash
amplifier tool invoke recipes operation=validate recipe_path=@team-pulse:recipes/pull-activity.yaml
amplifier tool invoke recipes operation=validate recipe_path=@team-pulse:recipes/log-commitments.yaml
amplifier tool invoke recipes operation=validate recipe_path=@team-pulse:recipes/set-outcomes.yaml
amplifier tool invoke recipes operation=validate recipe_path=@team-pulse:recipes/prep-audit.yaml
amplifier tool invoke recipes operation=validate recipe_path=@team-pulse:recipes/draft-showcase.yaml
amplifier tool invoke recipes operation=validate recipe_path=@team-pulse:recipes/process-standup.yaml
```

All 6 should pass validation.

**Step 2: Review and commit**

```bash
git add -A
git status
```

You should see:
- **New files:** `recipes/process-standup.yaml`
- **Modified files:** `recipes/prep-audit.yaml`, `recipes/draft-showcase.yaml`, `context/team-pulse-instructions.md`, `bundle.md`, `BACKLOG.md`, `CHANGELOG.md`, `.env.example`

```bash
git commit -m "feat: outcome-first audit, narrative showcase, standup processing

- Rewrite prep-audit for outcome-first grouping with alignment metric
- Rewrite draft-showcase with narrative leadership rollup for Sam
- Create process-standup recipe for transcript extraction
- Update bundle.md to v0.2.0 with 6 recipes
- Update BACKLOG.md with V2 completion and future work
- Add Alignment column to CHANGELOG.md"
```

```bash
git push
```

---

## Post-Implementation Verification

After all 22 tasks are complete, verify the final state:

**Directory structure should look like:**
```
amplifier-team-pulse/
├── org.yaml
├── people/
│   ├── chris/
│   │   ├── profile.yaml
│   │   ├── outcomes.md
│   │   ├── activity/.gitkeep
│   │   └── weeks/
│   │       ├── .gitkeep
│   │       └── 2026-W12/
│   │           └── commitments.md
│   ├── gurkaran/
│   │   ├── profile.yaml
│   │   ├── outcomes.md
│   │   ├── activity/.gitkeep
│   │   └── weeks/.gitkeep
│   ├── manoj/ (same structure)
│   ├── ken/ (same structure)
│   ├── salil/ (same structure)
│   ├── samuel/ (same structure)
│   └── alex/ (same structure)
├── views/
│   ├── teams/workspaces/.gitkeep
│   ├── managers/chris/.gitkeep
│   └── leadership/sam/.gitkeep
├── showcases/
│   ├── workspaces/.gitkeep
│   └── org-wide/.gitkeep
├── recipes/
│   ├── pull-activity.yaml
│   ├── log-commitments.yaml
│   ├── set-outcomes.yaml
│   ├── prep-audit.yaml
│   ├── draft-showcase.yaml
│   └── process-standup.yaml
├── context/
│   └── team-pulse-instructions.md
├── docs/
├── bundle.md
├── BACKLOG.md
├── CHANGELOG.md
├── .env.example
├── .gitignore
└── README.md
```

**Deleted files (should NOT exist):**
- `team.yaml`
- `team.yaml.example`
- `weeks/` directory
- `recipes/setup.yaml`

**Quick smoke test:** Run each recipe validation:
```bash
for recipe in pull-activity log-commitments set-outcomes prep-audit draft-showcase process-standup; do
  echo "Validating $recipe..."
  amplifier tool invoke recipes operation=validate recipe_path=@team-pulse:recipes/$recipe.yaml
done
```

All 6 should pass. The repo is now fully migrated to V2.