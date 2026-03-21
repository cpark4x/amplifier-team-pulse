# Changelog

| Week | Must-Ship | Shipped | Rate | Carried Forward | Alignment |
|------|-----------|---------|------|-----------------|-----------|\n| 2026-W12 | 1 | 1 | 100% | 0 | 0% |

---

## Phase 2: Outcome-Driven Weekly Alignment (2026-03-20)

### Added
- **Recipe: `confirm-alignment` (v0.1.0)** — Weekly alignment confirmation workflow. Clusters member activity by repository, links contributions to defined outcomes via `drives:` field, generates weekly summary of alignment, writes `summary.md` for audit pipeline consumption.

- **File type: `summary.md`** — Weekly activity summary clusters with outcome links. Used as input for audit views and leadership narrative generation. Located at `people/<name>/weeks/<WEEK>/summary.md`.

### Changed
- **Recipe: `prep-audit` (v0.3.0)** — Now reads `summary.md` as primary input. Generates three distinct views:
  - Manager audit (`views/audit-<WEEK>.md`) — Outcome tracking, alignment gaps, activity categorization
  - IC review (`people/<name>/weeks/<WEEK>/review.md`) — Personal weekly recap with outcome linkage
  - Leader narrative (`views/leadership-<WEEK>.md`) — Strategic narrative for leadership stakeholders
  - Changed output paths from structured subdirectories to flat view paths for easier integration

- **File: `context/team-pulse-instructions.md`** — Updated routing logic to trigger `confirm-alignment` before `prep-audit` for weekly alignment workflow

### Fixed
- **`confirm-alignment` immediate write** — Recipe now writes `summary.md` immediately without gating on interactive confirmation step, enabling pipeline integration and faster iteration
