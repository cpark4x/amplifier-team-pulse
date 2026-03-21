"""
Tests for recipes/prep-audit.yaml — Tasks 4-7 upgrades.

Covers:
  - Task 4: summary.md reading with graceful fallback
  - Task 5: IC review.md output
  - Task 6: leadership view at views/leadership-<WEEK>.md
  - Task 7: flat manager view at views/audit-<WEEK>.md (no nested team/manager paths)
  - Version bump to 0.3.0
  - Updated git commit paths

Run with: python3 -m pytest tests/test_prep_audit_recipe.py -v
"""

import os
import yaml
import pytest


RECIPE_PATH = os.path.join(
    os.path.dirname(__file__), "..", "recipes", "prep-audit.yaml"
)


@pytest.fixture
def recipe():
    """Load and parse the prep-audit.yaml recipe."""
    with open(RECIPE_PATH, "r") as f:
        return yaml.safe_load(f)


@pytest.fixture
def prompt(recipe):
    """Extract the main step prompt text."""
    return recipe["steps"][0]["prompt"]


# ---------------------------------------------------------------------------
# Metadata
# ---------------------------------------------------------------------------


class TestPrepAuditMetadata:
    """Top-level recipe metadata."""

    def test_recipe_name(self, recipe):
        """Recipe name must be 'prep-audit'."""
        assert recipe.get("name") == "prep-audit", (
            f"Expected name='prep-audit', got {recipe.get('name')!r}"
        )

    def test_recipe_version_bumped_to_0_3_0(self, recipe):
        """Version must be bumped to '0.3.0' for this feature set."""
        assert str(recipe.get("version")) == "0.3.0", (
            f"Expected version='0.3.0', got {recipe.get('version')!r}"
        )

    def test_recipe_timeout_unchanged(self, recipe):
        """Step timeout must remain 900."""
        step = recipe["steps"][0]
        assert step.get("timeout") == 900, (
            f"Expected timeout=900, got {step.get('timeout')!r}"
        )


# ---------------------------------------------------------------------------
# Task 4 — summary.md reading with graceful fallback
# ---------------------------------------------------------------------------


class TestTask4SummaryReading:
    """Prompt must instruct reading summary.md before falling back to raw activity."""

    def test_prompt_references_summary_md_read(self, prompt):
        """Prompt must instruct reading summary.md for each member."""
        assert "summary.md" in prompt, (
            "Prompt missing reference to summary.md (Task 4: read summaries)"
        )

    def test_prompt_references_summary_path(self, prompt):
        """Prompt must reference the summary path pattern people/<name>/weeks/<WEEK_ID>/summary.md."""
        assert "weeks/" in prompt and "summary.md" in prompt, (
            "Prompt missing weeks/<WEEK_ID>/summary.md path pattern"
        )

    def test_prompt_has_graceful_fallback_language(self, prompt):
        """Prompt must describe falling back to raw activity files when no summary exists."""
        lower = prompt.lower()
        assert "fall back" in lower or "fallback" in lower or "if it doesn't exist" in lower or "if no summary" in lower, (
            "Prompt missing graceful fallback language for missing summary.md"
        )

    def test_prompt_references_drives_tag(self, prompt):
        """Prompt must reference drives: tags from summaries as primary data source."""
        assert "drives:" in prompt, (
            "Prompt missing 'drives:' tag reference (activity clusters → outcomes)"
        )

    def test_prompt_references_activity_clusters(self, prompt):
        """Prompt must reference activity clusters from summary as data source."""
        lower = prompt.lower()
        assert "cluster" in lower, (
            "Prompt missing cluster reference for summary-based data source"
        )


# ---------------------------------------------------------------------------
# Task 5 — IC review.md view
# ---------------------------------------------------------------------------


class TestTask5ICView:
    """Prompt must generate per-person review.md files."""

    def test_prompt_references_review_md_output(self, prompt):
        """Prompt must instruct writing review.md for each member."""
        assert "review.md" in prompt, (
            "Prompt missing 'review.md' output instruction (Task 5: IC view)"
        )

    def test_prompt_references_ic_review_path(self, prompt):
        """Prompt must reference the IC review path pattern people/<name>/weeks/<WEEK_ID>/review.md."""
        assert "people/" in prompt and "review.md" in prompt, (
            "Prompt missing people/<name>/weeks/<WEEK_ID>/review.md path"
        )

    def test_ic_review_contains_your_activity_section(self, prompt):
        """IC review format must include 'Your Activity' section."""
        assert "Your Activity" in prompt, (
            "Prompt missing 'Your Activity' section in IC review format"
        )

    def test_ic_review_contains_outcomes_contributed_section(self, prompt):
        """IC review format must include 'Outcomes You Contributed To' section."""
        assert "Outcomes You Contributed To" in prompt, (
            "Prompt missing 'Outcomes You Contributed To' in IC review format"
        )

    def test_ic_review_contains_unlinked_activity_section(self, prompt):
        """IC review format must include 'Unlinked Activity' section."""
        assert "Unlinked Activity" in prompt, (
            "Prompt missing 'Unlinked Activity' section in IC review format"
        )

    def test_ic_review_references_teammates(self, prompt):
        """IC review must show cross-team awareness — teammates driving same outcomes."""
        lower = prompt.lower()
        assert "teammate" in lower or "teammates" in lower, (
            "Prompt missing teammate cross-team awareness in IC review"
        )


# ---------------------------------------------------------------------------
# Task 6 — Leadership view
# ---------------------------------------------------------------------------


class TestTask6LeadershipView:
    """Prompt must generate views/leadership-<WEEK>.md."""

    def test_prompt_references_leadership_view_path(self, prompt):
        """Prompt must reference views/leadership- output path."""
        assert "views/leadership-" in prompt, (
            "Prompt missing 'views/leadership-' output path (Task 6)"
        )

    def test_leadership_view_contains_outcome_progress_section(self, prompt):
        """Leadership view format must include 'Outcome Progress' section."""
        assert "Outcome Progress" in prompt, (
            "Prompt missing 'Outcome Progress' section in leadership view format"
        )

    def test_leadership_view_contains_team_health_section(self, prompt):
        """Leadership view format must include 'Team Health' section."""
        assert "Team Health" in prompt, (
            "Prompt missing 'Team Health' section in leadership view format"
        )

    def test_leadership_view_contains_alignment_rate(self, prompt):
        """Leadership view must include alignment rate metric."""
        lower = prompt.lower()
        assert "alignment rate" in lower or "alignment:" in lower, (
            "Prompt missing alignment rate metric in leadership view"
        )

    def test_leadership_view_contains_status_labels(self, prompt):
        """Leadership view must include outcome status labels (On track / At risk / Stalled)."""
        assert "On track" in prompt or "At risk" in prompt or "Stalled" in prompt, (
            "Prompt missing outcome status labels in leadership view"
        )

    def test_leadership_view_contains_unlinked_activity(self, prompt):
        """Leadership view must include unlinked activity section."""
        assert "Unlinked Activity" in prompt, (
            "Prompt missing 'Unlinked Activity' in leadership view"
        )


# ---------------------------------------------------------------------------
# Task 7 — Flat manager view paths
# ---------------------------------------------------------------------------


class TestTask7FlatManagerView:
    """Manager view must be consolidated to views/audit-<WEEK>.md."""

    def test_prompt_references_flat_audit_path(self, prompt):
        """Prompt must reference flat views/audit- output path."""
        assert "views/audit-" in prompt, (
            "Prompt missing 'views/audit-' flat path (Task 7)"
        )

    def test_prompt_does_not_reference_nested_teams_path(self, prompt):
        """Prompt must NOT reference old views/teams/ nested path."""
        assert "views/teams/" not in prompt, (
            "Prompt still references deprecated 'views/teams/' path (should be flat)"
        )

    def test_prompt_does_not_reference_nested_managers_path(self, prompt):
        """Prompt must NOT reference old views/managers/ nested path."""
        assert "views/managers/" not in prompt, (
            "Prompt still references deprecated 'views/managers/' path (should be flat)"
        )

    def test_audit_view_is_outcome_first(self, prompt):
        """Manager audit view must group by outcome (outcome-first layout)."""
        # The audit view should mention outcome grouping
        lower = prompt.lower()
        assert "outcome" in lower and (
            "group" in lower or "outcome-first" in lower or "grouped by outcome" in lower
        ), "Prompt missing outcome-first grouping instruction for audit view"

    def test_audit_view_has_unlinked_activity_section(self, prompt):
        """Manager audit view must have an 'Unlinked Activity' section for drift detection."""
        assert "Unlinked Activity" in prompt, (
            "Prompt missing 'Unlinked Activity' section in audit view"
        )


# ---------------------------------------------------------------------------
# Git commit step — updated paths
# ---------------------------------------------------------------------------


class TestGitCommitPaths:
    """Git commit must include all new output paths."""

    def test_git_commit_includes_review_md(self, prompt):
        """Git commit must include people/*/weeks/*/review.md."""
        assert "people/*/weeks/*/review.md" in prompt, (
            "Git commit missing 'people/*/weeks/*/review.md' glob"
        )

    def test_git_commit_includes_audit_view(self, prompt):
        """Git commit must include views/audit-*.md glob."""
        assert "views/audit-*.md" in prompt, (
            "Git commit missing 'views/audit-*.md' glob"
        )

    def test_git_commit_includes_leadership_view(self, prompt):
        """Git commit must include views/leadership-*.md glob."""
        assert "views/leadership-*.md" in prompt, (
            "Git commit missing 'views/leadership-*.md' glob"
        )
