# Phase 2: Alignment Confirmation & Three Views — Implementation Plan

> **Execution:** Use the subagent-driven-development workflow to implement this plan.

**Goal:** Add weekly alignment confirmation (linking activity clusters to outcomes) and generate three views (manager, IC, leader) from the same summary data.
**Architecture:** A new `confirm-alignment` recipe clusters a person's weekly activity by repo, presents clusters conversationally for outcome linking, and writes `summary.md`. The existing `prep-audit` recipe is upgraded to read summaries first (falling back to raw activity), then generate three distinct views instead of one.
**Tech Stack:** Amplifier recipe YAML, Jinja2 templating, `gh` CLI, markdown output files

**Design doc:** `docs/plans/2026-03-20-phase2-alignment-views-design.md`

---

## Phase A: Core — `confirm-alignment` Recipe

### Task 1: Create `recipes/confirm-alignment.yaml`

**Files:**
- Create: `recipes/confirm-alignment.yaml`

**Step 1: Create the recipe file**

Create `recipes/confirm-alignment.yaml` with the complete content below. This recipe follows the same single-step, `agent: self`, conversational pattern as `log-commitments.yaml`. The prompt has 8 numbered steps covering: week determination, member identification, activity file reading, clustering, outcomes reading, conversational presentation, file writing, and commit.

```yaml
name: confirm-alignment
description: >
  Weekly alignment confirmation for a team member. Reads daily activity files,
  clusters by repo, presents clusters to the manager for outcome linking, and
  writes a summary.md file with drives: tags connecting activity to outcomes.
version: "0.1.0"
tags: ["alignment", "weekly", "outcomes", "summary"]

# Usage:
#   "Confirm alignment for Ken"
#   amplifier tool invoke recipes operation=execute recipe_path=@team-pulse:recipes/confirm-alignment.yaml context='{"member_name": "Ken"}'
#   amplifier tool invoke recipes operation=execute recipe_path=@team-pulse:recipes/confirm-alignment.yaml context='{"member_name": "Ken", "week": "2026-W12"}'

context:
  member_name: ""  # Required: which member to review
  week: ""  # Optional: ISO week like 2026-W12. Defaults to current week.

steps:
  - id: confirm-alignment
    agent: self
    timeout: 600
    output: alignment_result
    prompt: |
      You are helping a manager confirm weekly alignment for a team member in
      Team Pulse. You will cluster their activity by repo, then ask the manager
      to link each cluster to an outcome.

      ## Step 1: Determine the Week

      {% if week != "" %}
      Use week: {{week}}
      {% else %}
      Run `date +%Y-W%V` to get the current ISO week identifier (e.g., 2026-W12).
      {% endif %}

      Calculate the Monday and Sunday dates for this week. You need these to
      filter activity files by date range.

      ## Step 2: Identify the Team Member

      {% if member_name != "" %}
      The member is: {{member_name}}
      {% else %}
      Ask the user: "Who are we reviewing this week?"
      {% endif %}

      - Read `org.yaml` and match the name to a member entry
      - Determine the lowercase directory name for this member:
        - "Chris P" → `chris`
        - "Gurkaran" → `gurkaran`
        - "Manoj" → `manoj`
        - "Ken" → `ken`
        - "Salil Das" → `salil`
        - "Samuel Lee" → `samuel`
        - "Alex Lopez" → `alex`
      - If no match found, show the member list from `org.yaml` and ask who
        they mean

      ## Step 3: Read Activity Files for This Week

      List all files in `people/<name>/activity/` and read those whose dates
      fall within Monday–Sunday of the target week.

      For example, if the week is 2026-W12 (Monday 2026-03-16 to Sunday
      2026-03-22), read files like `2026-03-16.md`, `2026-03-17.md`, etc.

      If NO activity files exist for this week, tell the manager:
      "No activity found for <name> in week <WEEK>. Run `pull-activity` first,
      or check that daily pulls have been running."
      Then stop.

      ## Step 4: Cluster Activity by Repo

      Parse all activity files and group by repository (`## <owner/repo>`
      headings in the activity files). For each repo, collect:
      - Number of commits
      - Number of merged PRs
      - Number of open PRs
      - All commit messages and PR titles

      Then generate a **one-line summary** for each repo cluster from the
      commit messages and PR titles. This should capture the theme of the work,
      not list individual commits. Examples:
      - "Built eval system with parallel test runner and rubric scoring"
      - "iOS UX fixes and cloud deployment pipeline"
      - "Documentation and PR-FAQ writing"

      Combine counts across all days in the week. A repo that appears in
      multiple daily files gets one merged cluster.

      For auto-discovered repos (marked with `(auto-discovered)` in activity
      files), preserve that annotation in the cluster heading.

      ## Step 5: Read Outcomes

      Read `people/<name>/outcomes.md`.

      Check whether real outcomes are defined or if it's a placeholder
      ("Outcomes not yet defined"). Outcome IDs are the `##` headings in
      kebab-case (e.g., `## lifeos-adoption` → outcome ID `lifeos-adoption`).

      - **If real outcomes exist:** You will present them as linkable options
        in Step 6.
      - **If outcomes are placeholder/undefined:** You will still generate
        the summary but without `drives:` values. Flag this to the manager:
        "No outcomes defined for <name> yet. I'll generate a weekly recap
        without alignment tags. Use 'set outcomes for <name>' to define them."

      ## Step 6: Present Clusters to Manager

      Show the manager each cluster and ask them to link it to outcomes.

      **If outcomes exist, present like this:**

      > Here's what <Name> worked on in <WEEK>:
      >
      > **kenotron-ms/lifeos** (17 commits)
      > Built eval system with parallel test runner and rubric scoring
      >
      > **kenotron-ms/agent-daemon** (35 commits)
      > macOS onboarding wizard, tray health indicator, cron schedule fix
      >
      > Their current outcomes are:
      > 1. `lifeos-adoption` — LifeOS is actively used by 5+ people...
      > 2. `eval-system` — Eval framework running nightly with...
      >
      > Which outcomes did each cluster drive? You can say things like:
      > - "lifeos drives lifeos-adoption"
      > - "agent-daemon drives eval-system"
      > - "the last one is unlinked"

      **If no outcomes exist, present like this:**

      > Here's what <Name> worked on in <WEEK>:
      >
      > **kenotron-ms/lifeos** (17 commits)
      > Built eval system with parallel test runner and rubric scoring
      >
      > No outcomes are defined for <Name> yet, so I can't link these
      > clusters. I'll save the summary as-is. Consider running
      > "set outcomes for <Name>" to make next week's alignment useful.
      >
      > Does this summary look accurate? Any corrections?

      Accept corrections to summaries. Keep the conversation lightweight —
      the goal is ~30 seconds of manager time per person, not a deep review.

      ## Step 7: Write the Summary File

      Create the week folder if it doesn't exist:
      ```
      mkdir -p people/<name>/weeks/<WEEK_ID>
      ```

      Write to `people/<name>/weeks/<WEEK_ID>/summary.md` using this exact
      format:

      ```
      # <Name> — Week of <MONDAY_DATE>

      ## Activity Clusters

      ### <owner/repo> (<N> commits)
      <One-line summary generated from commit messages>
      drives: <outcome-id>

      ### <owner/repo> (<N> commits, <M> PRs)
      <One-line summary>
      drives:

      ### <owner/repo> (auto-discovered, <N> commits)
      <One-line summary>
      drives:
      ```

      Rules:
      - Every cluster MUST have a `drives:` line — either an outcome ID or
        empty (meaning unlinked)
      - Count format: `<N> commits` alone if no PRs; add `, <M> PRs` if
        there are merged or open PRs (combine merged + open count)
      - Auto-discovered repos get `(auto-discovered, <N> commits)` format
      - The `##` heading is always `## Activity Clusters` (not per-outcome)
      - `drives:` with no value after it means unlinked — this is the drift
        signal for the manager view

      ## Step 8: Commit and Push

      ```
      git add people/<name>/weeks/<WEEK_ID>/summary.md
      git commit -m "alignment(<name>): confirm week <WEEK_ID>"
      git push
      ```

      ## Tone

      Be efficient and conversational. This is a quick alignment check, not
      a performance review. Present the data, get the links, write the file.
      If outcomes aren't defined, don't nag — just note it once and move on.
      The summary is still useful as a weekly recap even without alignment tags.
```

**Step 2: Validate the recipe file is well-formed YAML**

Run:
```
python3 -c "import yaml; yaml.safe_load(open('recipes/confirm-alignment.yaml')); print('YAML valid')"
```
Expected: `YAML valid`

**Step 3: Verify the recipe is discoverable by checking it has required fields**

Run:
```
python3 -c "
import yaml
r = yaml.safe_load(open('recipes/confirm-alignment.yaml'))
assert r['name'] == 'confirm-alignment', f'name mismatch: {r[\"name\"]}'
assert r['version'] == '0.1.0', f'version mismatch: {r[\"version\"]}'
assert len(r['steps']) == 1, f'expected 1 step, got {len(r[\"steps\"])}'
assert r['steps'][0]['agent'] == 'self', f'agent mismatch'
assert r['steps'][0]['timeout'] == 600, f'timeout mismatch: {r[\"steps\"][0][\"timeout\"]}'
assert 'member_name' in r['context'], 'missing member_name context'
assert 'week' in r['context'], 'missing week context'
print('All recipe fields validated')
"
```
Expected: `All recipe fields validated`

**Step 4: Commit**

```
git add recipes/confirm-alignment.yaml
git commit -m "feat: add confirm-alignment recipe for weekly alignment confirmation"
```

---

### Task 2: Register `confirm-alignment` in Context Instructions

**Files:**
- Modify: `context/team-pulse-instructions.md` (insert new section between "Set Outcomes" and "Prep Audit")

**Step 1: Add the Confirm Alignment section to the instructions file**

Insert a new section after the "Set Outcomes" section (after line 48) and before the "Prep Audit" section. The new section should be:

```markdown
## Confirm Alignment (Weekly, manager)

Reviews one team member's weekly activity, clusters it by repo, and asks the manager to link each cluster to an outcome. Writes `summary.md` with `drives:` tags. Run this before `prep-audit` for best results.

**Run with the recipes tool:**
```
recipes(operation="execute", recipe_path="@team-pulse:recipes/confirm-alignment.yaml", context={"member_name": "Ken"})
```

**For a specific week:**
```
recipes(operation="execute", recipe_path="@team-pulse:recipes/confirm-alignment.yaml", context={"member_name": "Ken", "week": "2026-W12"})
```

**When the user says:** "confirm alignment for Ken", "review Ken's week", "link Ken's activity to outcomes", "what did Ken work on this week", "align Ken's work"
```

**Step 2: Verify the file has the new section**

Run:
```
grep -c "Confirm Alignment" context/team-pulse-instructions.md
```
Expected: `1` (exactly one match)

**Step 3: Commit**

```
git add context/team-pulse-instructions.md
git commit -m "docs: register confirm-alignment recipe in context instructions"
```

---

### Task 3: Validate `confirm-alignment` with Chris's W12 Data

**Files:**
- No files created or modified — this is a validation-only task
- Reads: `people/chris/activity/2026-03-16.md` through `2026-03-19.md` (W12 data), `people/chris/outcomes.md`
- Writes (via recipe): `people/chris/weeks/2026-W12/summary.md`

**Step 1: Verify Chris has W12 activity data available**

Run:
```
ls -la people/chris/activity/2026-03-1[6-9].md
```
Expected: 4 files listed (2026-03-16 through 2026-03-19 — Monday through Thursday of W12)

**Step 2: Check Chris's current outcomes state**

Run:
```
cat people/chris/outcomes.md
```
Expected: Placeholder text — `Outcomes not yet defined`. This means the recipe should generate a summary WITHOUT `drives:` values and flag that no outcomes are defined.

**Step 3: Run the confirm-alignment recipe for Chris, week W12**

Run:
```
recipes(operation="execute", recipe_path="@team-pulse:recipes/confirm-alignment.yaml", context={"member_name": "Chris P", "week": "2026-W12"})
```

During execution, the recipe will:
1. Read activity files for 2026-03-16 through 2026-03-22
2. Cluster by repo — expect clusters for repos like `cpark4x/canvas-specialists`, `cpark4x/ridecast`, `cpark4x/amplifier-team-pulse`, etc.
3. Detect that outcomes are placeholder — should flag "No outcomes defined for Chris yet"
4. Present clusters for review — since outcomes are undefined, it should skip the linking conversation and just ask if the summary looks accurate
5. Write `people/chris/weeks/2026-W12/summary.md`
6. Commit

**Step 4: Verify the summary file was created with correct format**

Run:
```
cat people/chris/weeks/2026-W12/summary.md
```

Verify:
- File starts with `# Chris P — Week of 2026-03-16`
- Has `## Activity Clusters` heading
- Has `### <owner/repo> (<N> commits)` sub-headings for each repo
- Each cluster has a one-line summary
- Each cluster has a `drives:` line (all empty since no outcomes are defined)
- Auto-discovered repos are annotated with `(auto-discovered, ...)`

**Step 5: Verify raw activity files were NOT modified**

Run:
```
git diff people/chris/activity/
```
Expected: No output (activity files unchanged)

---

## Phase B: Views — Upgrade `prep-audit`

### Task 4: Add `summary.md` Reading to `prep-audit.yaml`

**Files:**
- Modify: `recipes/prep-audit.yaml` (add Step 2a after existing Step 2, bump version)

**Step 1: Bump the version from "0.2.0" to "0.3.0"**

In `recipes/prep-audit.yaml`, change:
```
version: "0.2.0"
```
to:
```
version: "0.3.0"
```

**Step 2: Add Step 2a — read summary.md files**

Insert a new section after Step 2 (after the member data reading) and before Step 3 (repo scanning). Add this new step between the end of Step 2 and the beginning of Step 3:

```markdown
      ## Step 2a: Read Summary Files (Alignment Data)

      For each member, check if a summary file exists:
      `people/<name>/weeks/<WEEK_ID>/summary.md`

      If it exists, read it. Parse the activity clusters:
      - Each `### <owner/repo> (...)` heading is a cluster
      - The line below the heading is the one-line summary
      - The `drives: <outcome-id>` line links the cluster to an outcome
        (empty `drives:` means unlinked)

      Track which members have summaries and which don't. Members WITH
      summaries get the outcome-first treatment in views. Members WITHOUT
      summaries fall back to the raw activity + commitments approach from
      Step 3 onward.

      This is the key Phase 2 behavior: if `confirm-alignment` has been run
      for a member, their data is richer. If not, everything still works
      using the Phase 1 activity-first path.
```

**Step 3: Update Step 3 heading to clarify fallback behavior**

Change Step 3's description to make it clear this is the fallback path. Replace the first line of Step 3:

From:
```
      ## Step 3: Scan Repos for Activity (if no daily activity files exist)
```

To:
```
      ## Step 3: Scan Repos for Activity (fallback — only if no activity files AND no summary)
```

**Step 4: Validate YAML is still well-formed**

Run:
```
python3 -c "import yaml; yaml.safe_load(open('recipes/prep-audit.yaml')); print('YAML valid')"
```
Expected: `YAML valid`

**Step 5: Commit**

```
git add recipes/prep-audit.yaml
git commit -m "feat(prep-audit): add summary.md reading with fallback to raw activity"
```

---

### Task 5: Add IC View Output to `prep-audit.yaml`

**Files:**
- Modify: `recipes/prep-audit.yaml` (add new step after Step 6 for IC view)

**Step 1: Add Step 6a — Write IC Review Files**

Insert a new step after Step 6 (per-person audit files) and before Step 7 (team audit view). This step generates a personal review for each IC:

```markdown
      ## Step 6a: Write IC Review Files

      For each member who has a summary.md for this week, write a personal
      review to:
      `people/<name>/weeks/<WEEK_ID>/review.md`

      This is the IC's personal view — "Where do I fit?"

      ```
      # <Name> — Week in Review (<WEEK_ID>)

      ## Your Activity This Week

      ### <owner/repo> (<N> commits)
      <One-line summary from summary.md>
      Drives: <outcome description> (or "Unlinked" if drives: is empty)

      ### <next repo cluster>
      ...

      ## Outcomes You Contributed To

      ### <outcome-id>: <outcome description>
      Your work: <which clusters drove this outcome>
      Teammates on this outcome: <other members whose summaries also
        link clusters to this same outcome-id, with their cluster summaries>

      ### <next outcome>
      ...

      ## Unlinked Activity
      <Clusters where drives: is empty — nudge to link or flag as exploration>
      - <owner/repo>: <summary> — Consider linking to an outcome or flagging
        as experimentation
      ```

      Rules:
      - Only generate review.md for members who HAVE a summary.md this week
      - The "Teammates on this outcome" section creates cross-team awareness —
        look across ALL members' summaries to find shared outcome-ids
      - If a member has no outcomes defined, skip the "Outcomes You Contributed
        To" section and just show activity clusters
      - Omit any section with no data

      For members WITHOUT summary.md, do NOT generate a review.md — the IC
      view requires alignment data to be meaningful.
```

**Step 2: Validate YAML is still well-formed**

Run:
```
python3 -c "import yaml; yaml.safe_load(open('recipes/prep-audit.yaml')); print('YAML valid')"
```
Expected: `YAML valid`

**Step 3: Commit**

```
git add recipes/prep-audit.yaml
git commit -m "feat(prep-audit): add IC review.md personal view per member"
```

---

### Task 6: Add Leader View Output to `prep-audit.yaml`

**Files:**
- Modify: `recipes/prep-audit.yaml` (add new step after the manager rollup step for leader view)

**Step 1: Add Step 8a — Write Leader View**

Insert a new step after Step 8 (manager rollup) and before Step 9 (CHANGELOG update). This step generates the leader narrative:

```markdown
      ## Step 8a: Write Leader View

      Write a leadership narrative view to:
      `views/leadership-<WEEK_ID>.md`

      This is the leader's view — "Where is this going?" — designed for Sam,
      a VP who needs to understand the state of the org in 30 seconds.

      ```
      # Leadership View — Week of <MONDAY_DATE>

      ## Outcome Trajectories

      ### <outcome-id>: <outcome description>
      **Status:** <On track / Progressing / At risk / Stalled>
      **Contributors:** <names of people whose summaries link to this outcome>

      <Narrative paragraph: 2-3 sentences explaining what happened this week
      on this outcome, why it matters, and where it's headed. Written for
      someone who doesn't know the technical details. Draw from the cluster
      summaries and commit themes to paint a picture.>

      ### <next outcome>
      ...

      ## Unlinked Activity

      <Summary of activity clusters across the org that aren't linked to any
      outcome. This is the org-level drift signal.>

      - <person>: <owner/repo> — <summary>

      ## Org Health

      - **Members with alignment confirmed:** <N> of <total>
      - **Outcomes with active contributors:** <N> of <total defined>
      - **Outcomes with no activity this week:** <list or "none">
      ```

      Rules:
      - Group ALL members' data by outcome across the whole org, not per-team
      - The narrative paragraph is the key differentiator — don't just list
        facts, tell the story of what's happening on each outcome
      - If no summaries exist for anyone, fall back to a simpler activity-only
        view: "Alignment confirmation hasn't been run yet this week.
        Here's the raw activity summary:" followed by per-person activity
        highlights
      - Status determination:
        - **On track** = multiple contributors with linked activity
        - **Progressing** = at least one contributor with linked activity
        - **At risk** = contributors exist but activity is sparse or mostly unlinked
        - **Stalled** = outcome defined but no linked activity this week
      - Create the views directory if needed: `mkdir -p views`
```

**Step 2: Validate YAML is still well-formed**

Run:
```
python3 -c "import yaml; yaml.safe_load(open('recipes/prep-audit.yaml')); print('YAML valid')"
```
Expected: `YAML valid`

**Step 3: Commit**

```
git add recipes/prep-audit.yaml
git commit -m "feat(prep-audit): add leadership narrative view"
```

---

### Task 7: Flatten Manager View Paths

**Files:**
- Modify: `recipes/prep-audit.yaml` (change Step 7 and Step 8 output paths, update Step 10 git add)

**Step 1: Change Step 7 — Team Audit View path**

In Step 7, change the output path from the nested structure to flat.

Replace:
```
      For each team in `org.yaml`, write to:
      `views/teams/<team>/<WEEK_ID>-audit.md`
```

With:
```
      Write the manager audit view to:
      `views/audit-<WEEK_ID>.md`

      This is a single consolidated file covering all teams (flat path,
      not nested by team). If multiple teams exist, include all in one file
      with team headers.
```

**Step 2: Change Step 8 — Manager Rollup path**

In Step 8, the output currently goes to `views/managers/<name>/<WEEK_ID>-rollup.md`. We're consolidating this into the same `views/audit-<WEEK_ID>.md` file from Step 7. Replace the Step 8 output path.

Replace:
```
      For each manager in `org.yaml`, write to:
      `views/managers/<lowercase_manager_first_name>/<WEEK_ID>-rollup.md`
```

With:
```
      The manager rollup content is now included in `views/audit-<WEEK_ID>.md`
      from Step 7 — append the "Needs Attention" and "Member Scorecard"
      sections there instead of writing a separate file.

      Do NOT write to `views/managers/` — that path is deprecated.
```

**Step 3: Update Step 10 — git add paths**

In Step 10, the git add command references the old nested paths. Update it.

Replace:
```
      git add people/*/weeks/*/audit.md views/ CHANGELOG.md
```

With:
```
      git add people/*/weeks/*/audit.md people/*/weeks/*/review.md views/ CHANGELOG.md
```

**Step 4: Validate YAML is still well-formed**

Run:
```
python3 -c "import yaml; yaml.safe_load(open('recipes/prep-audit.yaml')); print('YAML valid')"
```
Expected: `YAML valid`

**Step 5: Verify the version is "0.3.0"**

Run:
```
grep 'version:' recipes/prep-audit.yaml
```
Expected: `version: "0.3.0"`

**Step 6: Commit**

```
git add recipes/prep-audit.yaml
git commit -m "feat(prep-audit): flatten view paths and consolidate manager rollup"
```

---

## Phase C: Validation & Cleanup

### Task 8: End-to-End Validation

**Files:**
- No files created or modified manually — recipes write the output files
- Validates: `people/chris/weeks/2026-W12/summary.md` (from Task 3), `views/audit-2026-W12.md`, `people/chris/weeks/2026-W12/review.md`, `views/leadership-2026-W12.md`

**Prerequisites:** Task 3 must have run successfully (Chris's `summary.md` exists).

**Step 1: Verify summary.md exists from Task 3**

Run:
```
test -f people/chris/weeks/2026-W12/summary.md && echo "EXISTS" || echo "MISSING"
```
Expected: `EXISTS`

If MISSING: re-run Task 3 first.

**Step 2: Run prep-audit for W12**

Run:
```
recipes(operation="execute", recipe_path="@team-pulse:recipes/prep-audit.yaml", context={"week": "2026-W12"})
```

During execution, verify the recipe:
1. Reads `summary.md` for Chris (Step 2a) — Chris has one, others don't
2. Falls back to raw activity for members without summaries (Ken, Gurkaran have activity files; others may have none)
3. Generates per-person audit files at `people/<name>/weeks/2026-W12/audit.md`
4. Generates IC review for Chris at `people/chris/weeks/2026-W12/review.md` (only Chris has a summary)
5. Generates manager view at `views/audit-2026-W12.md` (NOT `views/teams/...`)
6. Generates leader view at `views/leadership-2026-W12.md`
7. Updates CHANGELOG.md
8. Commits

**Step 3: Verify all three views were generated**

Run:
```
echo "=== Manager View ===" && head -5 views/audit-2026-W12.md && echo "" && echo "=== IC Review ===" && head -5 people/chris/weeks/2026-W12/review.md && echo "" && echo "=== Leader View ===" && head -5 views/leadership-2026-W12.md
```

Expected: First 5 lines of each file showing correct headers:
- Manager view: heading mentioning "Audit" and "2026-03-16" (Monday of W12)
- IC review: heading mentioning "Chris" and "Week in Review"
- Leader view: heading mentioning "Leadership View" and "2026-03-16"

**Step 4: Verify old nested paths were NOT used**

Run:
```
find views/teams views/managers -name "*.md" 2>/dev/null | wc -l
```
Expected: `0` (no new files in the old nested directories)

**Step 5: Verify raw activity files were NOT modified**

Run:
```
git diff people/chris/activity/ people/ken/activity/ people/gurkaran/activity/
```
Expected: No output (activity files unchanged by prep-audit)

**Step 6: Verify CHANGELOG was updated**

Run:
```
cat CHANGELOG.md
```
Expected: A new row with W12 data appended to the table.

---

### Task 9: Update BACKLOG.md and Final Commit

**Files:**
- Modify: `BACKLOG.md`

**Step 1: Update BACKLOG.md — add Phase 2 to Recently Completed**

In `BACKLOG.md`, add these rows to the "Recently Completed" table (after the existing rows, before the `---` separator):

```markdown
| Phase 2: confirm-alignment recipe | Chris | 2026-03-20 | Weekly alignment confirmation with drives: tags |
| Phase 2: Three views (manager, IC, leader) | Chris | 2026-03-20 | prep-audit upgrade — outcome-first views |
| Phase 2: summary.md file format | Chris | 2026-03-20 | Derived weekly summary linking activity to outcomes |
```

**Step 2: Update BACKLOG.md — update Current Status Summary**

Change the status summary at the top to reflect Phase 2 completion.

Replace:
```markdown
**3 epics tracked:** 2 complete, 1 planned

- V1 core loop (commitments, audit, showcase) — shipped
- V2 outcome-driven multi-team (migration, daily pull, outcomes, narrative showcase) — shipped
- V2 polish + V3 website — planned
```

With:
```markdown
**4 epics tracked:** 3 complete, 1 planned

- V1 core loop (commitments, audit, showcase) — shipped
- V2 outcome-driven multi-team (migration, daily pull, outcomes, narrative showcase) — shipped
- V2 Phase 2: alignment confirmation + three views — shipped
- V3 polish + website — planned
```

**Step 3: Update the "Last Updated" date**

Change:
```
**Last Updated:** 2026-03-18
```
To:
```
**Last Updated:** 2026-03-20
```

**Step 4: Commit everything**

```
git add BACKLOG.md
git commit -m "docs: update backlog with Phase 2 completion"
git push
```
