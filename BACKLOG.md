# Product Backlog

**Purpose:** Outcome-driven weekly accountability for multi-team orgs — outcomes, commitments, activity pull, audit, showcase.
**Owner:** Chris Park
**Last Updated:** 2026-03-20

---

## Current Status Summary

**4 epics tracked:** 3 complete, 1 planned

- V1 core loop (commitments, audit, showcase) — shipped
- V2 outcome-driven multi-team (migration, daily pull, outcomes, narrative showcase) — shipped
- V2 Phase 2: weekly alignment (confirm-alignment recipe, three audit views, outcome linking) — shipped
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
| Phase 2: Weekly alignment confirmation | Chris | 2026-03-20 | confirm-alignment recipe v0.1.0, clusters activity by repo |
| Phase 2: Summary-driven audit pipeline | Chris | 2026-03-20 | prep-audit v0.3.0 reads summary.md, generates manager/IC/leader views |
| Phase 2: Team pulse instructions integration | Chris | 2026-03-20 | Routing triggers confirm-alignment before audit |

---

## Prioritized Future Work

### Immediate Next

| # | Item | Effort | Impact | Why Now |
|---|------|--------|--------|---------|
| 1 | IC reviews self-service gating | S | M | IC reviews only generated for members with summary.md; others need to run confirm-alignment first (deferred) |
| 2 | Draft-showcase + leader view integration | M | M | Leadership narrative + showcase cross-linking (deferred) |
| 3 | Batch confirmation mode (team-wide) | M | M | Run confirm-alignment for entire team at once instead of per-member (deferred) |
| 4 | CLI identity filtering (V2) | M | H | Different views per person based on git config → org.yaml lookup |
| 5 | Define real outcomes for all 7 ICs | S | H | Placeholder outcomes need to be replaced with real Q1 goals |
| 6 | Collect GitHub handles for Salil, Samuel, Alex | S | H | Activity pull can't run for them until configured |

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
