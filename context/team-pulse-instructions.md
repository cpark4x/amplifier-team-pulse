# Team Pulse — Available Workflows

You are operating as part of the Team Pulse bundle. When a user triggers one of these workflows, use the `recipes` tool to execute the recipe. Do NOT attempt to perform the workflow yourself — the recipes handle multi-step orchestration.

**Catch-all rule:** If the user mentions commitments, audits, showcases, or weekly updates in a way that matches any workflow below, default to running the appropriate recipe.

## Log Commitments (Weekly, each team member)

Captures weekly commitments with outcomes, repos, and priorities. Surfaces carry-over from the previous week automatically.

**Run with the recipes tool:**
```
recipes(operation="execute", recipe_path="@team-pulse:recipes/log-commitments.yaml")
```

**With a specific member name:**
```
recipes(operation="execute", recipe_path="@team-pulse:recipes/log-commitments.yaml", context={"member_name": "Ken"})
```

**When the user says:** "log my commitments", "log commitments", "what am I committing to this week", "weekly commitments"

## Prep Audit (Weekly, automated or manager-triggered)

Scans tracked repos for activity via `gh` CLI, matches against commitments, generates the audit and scorecard.

**Run with the recipes tool:**
```
recipes(operation="execute", recipe_path="@team-pulse:recipes/prep-audit.yaml")
```

**For a specific week:**
```
recipes(operation="execute", recipe_path="@team-pulse:recipes/prep-audit.yaml", context={"week": "2026-W12"})
```

**When the user says:** "prep the audit", "run the audit", "generate audit", "prep audit"

## Draft Showcase (Weekly, manager)

Generates team and leadership showcases from the finalized audit. Posts to Teams on manager approval. This is a staged recipe — the manager reviews drafts before they are posted.

**Run with the recipes tool:**
```
recipes(operation="execute", recipe_path="@team-pulse:recipes/draft-showcase.yaml")
```

**When the user says:** "draft the showcase", "generate showcases", "send the update", "post to Teams"

## Setup (One-time, manager)

Interactive setup for new teams. Creates team.yaml, initial folder structure, and configuration.

**Run with the recipes tool:**
```
recipes(operation="execute", recipe_path="@team-pulse:recipes/setup.yaml")
```

**When the user says:** "set up team pulse", "configure team pulse", "initial setup"
