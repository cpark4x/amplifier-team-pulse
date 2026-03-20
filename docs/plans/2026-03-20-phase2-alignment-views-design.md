# Team Pulse Phase 2: Alignment Confirmation & Views

## Goal

Shift Team Pulse from "what did people do" to "is this work driving the outcomes we agreed on." Phase 1 captures raw activity. Phase 2 adds the alignment layer — lightweight human confirmation that links activity to outcomes — and generates three views over that data.

## Background

Phase 1 (already built) provides:
- `pull-activity` recipe capturing daily GitHub activity per person
- Activity files at `people/<name>/activity/<DATE>.md`
- `outcomes.md` per person (currently placeholder, needs real outcomes)
- `commitments.md` per person per week (planned work)

The vision doc (`docs/plans/2026-03-19-team-pulse-vision.md`) defines three layers: Outcomes (top-down), Activity (bottom-up), Alignment (the bridge). Phase 2 builds the bridge.

## Approach: Weekly Summary with Alignment Tags

Week-level alignment, not commit-level. The system clusters a week's activity by repo/theme and asks the person (or manager) to link each cluster to outcomes. This keeps confirmation lightweight (~30 seconds) while producing meaningful signal.

A new file: `people/<name>/weeks/<YYYY-WNN>/summary.md`.

### Summary File Format

```markdown
# <Name> — Week of <YYYY-MM-DD>

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

- The system generates clusters and one-line summaries from activity data
- `drives:` fields start empty (or with best-guess proposal if outcomes are defined)
- The person fills in or confirms outcome IDs
- Clusters with no `drives:` value are "unlinked" — visible as drift in the manager view
- Raw activity files in `activity/` are untouched — `summary.md` is a derived artifact alongside `commitments.md` in the same week folder

## Architecture

Two recipe changes, one new file type (`summary.md`), three views. The data flows:

```
pull-activity (daily)
  → people/<name>/activity/<DATE>.md (raw activity, unchanged)

confirm-alignment (weekly, manager-driven)
  → reads activity files + outcomes.md
  → writes people/<name>/weeks/<YYYY-WNN>/summary.md

prep-audit (weekly, Friday)
  → reads summary.md files (or falls back to raw activity)
  → writes views/audit-<YYYY-WNN>.md        (manager view)
  → writes people/<name>/weeks/.../review.md (IC view)
  → writes views/leadership-<YYYY-WNN>.md   (leader view)
```

## Components

### New Recipe: `confirm-alignment.yaml`

Single mode for now: manager reviews one person at a time. No batch mode, no IC self-service yet. YAGNI.

**Input:** `member_name` (required), `week` (optional, defaults to current)

**Flow:**
1. Read all activity files from `people/<name>/activity/` for that week's date range
2. Cluster activity by repo, generate one-line summaries from commit messages
3. Read `people/<name>/outcomes.md`
   - If outcomes exist: present them as linkable options alongside each cluster
   - If no outcomes defined: generate summary without `drives:` fields, flag "no outcomes defined" — still useful as a weekly recap, naturally motivates setting outcomes
4. Present clusters conversationally — "Here's what \<name\> worked on this week. Which outcomes did these drive?"
5. Write `people/<name>/weeks/<YYYY-WNN>/summary.md`
6. Commit

The confirmation flow is one data operation (linking activity to outcomes) that can eventually be triggered from multiple entry points (recipe, 1:1, self-service). Phase 2 starts with just the manager-reviews-one-person flow.

### Modified Recipe: `prep-audit.yaml` — Three Views

The existing `prep-audit` recipe is upgraded from activity-first to outcome-first. It now reads `summary.md` files (produced by `confirm-alignment`) and generates three outputs instead of one.

**Fallback:** If no `summary.md` files exist yet, fall back to current activity-first behavior. This ensures the recipe doesn't break while Phase 2 rolls out.

#### Manager View (`views/audit-<YYYY-WNN>.md`)

*"Where do I intervene?"*

Outcome-first structure:
- Each defined outcome with its contributors and confirmed activity
- Progress signal per outcome (who's contributing, what's been done)
- Unlinked Activity section — activity clusters where no outcome was linked (the drift detector)
- Outcomes with no contributors flagged as stalled

#### IC View (`people/<name>/weeks/<YYYY-WNN>/review.md`)

*"Where do I fit?"*

Personal view per person:
- Your activity clusters and what they drove
- Which outcomes you contributed to
- What teammates are working on for the same outcomes (cross-team awareness)
- Any unlinked activity (nudge to link or flag as experimentation)

#### Leader View (`views/leadership-<YYYY-WNN>.md`)

*"Where is this going?"*

Narrative trajectory for Sam:
- Outcomes across the org with progress summaries
- Narrative context explaining what each outcome's contributors are doing and why it matters
- Designed for a VP who doesn't know the details to understand the state in 30 seconds
- Feeds into (or replaces) the existing `draft-showcase` recipe

All three views generated in one `prep-audit` run. Same underlying data, three lenses.

## What Doesn't Change

- `pull-activity.yaml` — keeps capturing raw activity as-is
- `log-commitments.yaml` — still works for planned commitments; `summary.md` is the "actuals" counterpart
- Activity files in `people/<name>/activity/` — untouched, `summary.md` is derived
- `set-outcomes.yaml` — still the way outcomes get defined (needs to be run before alignment is meaningful)

## Testing Strategy

- Run `confirm-alignment` on one team member's current week data to validate clustering and summary output
- Run `prep-audit` with and without `summary.md` files to validate fallback behavior
- Verify all three views generate correctly from the same summary data
- Confirm raw activity files are never modified by either recipe

## Open Questions

1. Should `confirm-alignment` propose `drives:` tags using keyword matching against outcome descriptions, or always start blank?
2. When outcomes change mid-quarter, should existing summaries be re-evaluated, or only future weeks?
3. Should the leader view completely replace `draft-showcase`, or remain a separate artifact?