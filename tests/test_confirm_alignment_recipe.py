"""
Tests for recipes/confirm-alignment.yaml

Follows TDD: these tests are written BEFORE the recipe file exists.
Run with: python -m pytest tests/test_confirm_alignment_recipe.py -v
"""

import os
import yaml
import pytest


RECIPE_PATH = os.path.join(
    os.path.dirname(__file__), "..", "recipes", "confirm-alignment.yaml"
)


@pytest.fixture
def recipe():
    """Load and parse the confirm-alignment.yaml recipe."""
    with open(RECIPE_PATH, "r") as f:
        return yaml.safe_load(f)


class TestConfirmAlignmentRecipeExists:
    """Test that the recipe file exists and is valid YAML."""

    def test_recipe_file_exists(self):
        """File recipes/confirm-alignment.yaml must exist."""
        assert os.path.exists(RECIPE_PATH), (
            f"Recipe file not found at {RECIPE_PATH}"
        )

    def test_recipe_is_valid_yaml(self):
        """Recipe must be valid YAML (parseable with yaml.safe_load)."""
        with open(RECIPE_PATH, "r") as f:
            content = f.read()
        result = yaml.safe_load(content)
        assert result is not None, "Recipe YAML parsed to None"
        assert isinstance(result, dict), "Recipe YAML must parse to a dict"


class TestConfirmAlignmentRecipeMetadata:
    """Test recipe top-level metadata fields."""

    def test_recipe_name(self, recipe):
        """Recipe name must be 'confirm-alignment'."""
        assert recipe.get("name") == "confirm-alignment", (
            f"Expected name='confirm-alignment', got {recipe.get('name')!r}"
        )

    def test_recipe_version(self, recipe):
        """Recipe version must be '0.1.0'."""
        assert str(recipe.get("version")) == "0.1.0", (
            f"Expected version='0.1.0', got {recipe.get('version')!r}"
        )

    def test_recipe_has_tags(self, recipe):
        """Recipe must have tags field."""
        assert "tags" in recipe, "Recipe missing 'tags' field"
        assert isinstance(recipe["tags"], list), "Tags must be a list"

    def test_recipe_tags_contain_required_values(self, recipe):
        """Tags must include alignment, weekly, outcomes, summary."""
        tags = recipe.get("tags", [])
        for required_tag in ["alignment", "weekly", "outcomes", "summary"]:
            assert required_tag in tags, (
                f"Missing required tag '{required_tag}' in tags: {tags}"
            )


class TestConfirmAlignmentRecipeContext:
    """Test recipe context fields."""

    def test_context_exists(self, recipe):
        """Recipe must have a context section."""
        assert "context" in recipe, "Recipe missing 'context' field"
        assert isinstance(recipe["context"], dict), "Context must be a dict"

    def test_context_has_member_name(self, recipe):
        """Context must have 'member_name' field."""
        context = recipe.get("context", {})
        assert "member_name" in context, (
            "Context missing 'member_name' field"
        )

    def test_context_member_name_default_empty_string(self, recipe):
        """Context 'member_name' must default to empty string."""
        context = recipe.get("context", {})
        assert context.get("member_name") == "", (
            f"Expected member_name='', got {context.get('member_name')!r}"
        )

    def test_context_has_week(self, recipe):
        """Context must have 'week' field."""
        context = recipe.get("context", {})
        assert "week" in context, "Context missing 'week' field"

    def test_context_week_default_empty_string(self, recipe):
        """Context 'week' must default to empty string."""
        context = recipe.get("context", {})
        assert context.get("week") == "", (
            f"Expected week='', got {context.get('week')!r}"
        )


class TestConfirmAlignmentRecipeSteps:
    """Test recipe steps configuration."""

    def test_steps_exists(self, recipe):
        """Recipe must have a steps section."""
        assert "steps" in recipe, "Recipe missing 'steps' field"
        assert isinstance(recipe["steps"], list), "Steps must be a list"

    def test_exactly_one_step(self, recipe):
        """Recipe must have exactly 1 step."""
        steps = recipe.get("steps", [])
        assert len(steps) == 1, (
            f"Expected exactly 1 step, got {len(steps)}"
        )

    def test_step_id(self, recipe):
        """Step must have id='confirm-alignment'."""
        step = recipe["steps"][0]
        assert step.get("id") == "confirm-alignment", (
            f"Expected step id='confirm-alignment', got {step.get('id')!r}"
        )

    def test_step_agent_is_self(self, recipe):
        """Step must have agent='self'."""
        step = recipe["steps"][0]
        assert step.get("agent") == "self", (
            f"Expected agent='self', got {step.get('agent')!r}"
        )

    def test_step_timeout(self, recipe):
        """Step must have timeout=600."""
        step = recipe["steps"][0]
        assert step.get("timeout") == 600, (
            f"Expected timeout=600, got {step.get('timeout')!r}"
        )

    def test_step_output(self, recipe):
        """Step must have output='alignment_result'."""
        step = recipe["steps"][0]
        assert step.get("output") == "alignment_result", (
            f"Expected output='alignment_result', got {step.get('output')!r}"
        )

    def test_step_has_prompt(self, recipe):
        """Step must have a prompt field."""
        step = recipe["steps"][0]
        assert "prompt" in step, "Step missing 'prompt' field"
        assert isinstance(step["prompt"], str), "Prompt must be a string"
        assert len(step["prompt"].strip()) > 0, "Prompt must not be empty"


class TestConfirmAlignmentRecipePromptContent:
    """Test that the prompt contains required content for all 8 steps."""

    def get_prompt(self, recipe):
        return recipe["steps"][0]["prompt"]

    def test_prompt_contains_week_jinja_conditional(self, recipe):
        """Prompt must use Jinja2 conditional for 'week' context variable."""
        prompt = self.get_prompt(recipe)
        assert "{% if week" in prompt, (
            "Prompt missing Jinja2 conditional for 'week'"
        )

    def test_prompt_contains_date_command(self, recipe):
        """Prompt must reference `date +%Y-W%V` command."""
        prompt = self.get_prompt(recipe)
        assert "date +%Y-W%V" in prompt, (
            "Prompt missing `date +%Y-W%V` command for week determination"
        )

    def test_prompt_contains_member_name_jinja_conditional(self, recipe):
        """Prompt must use Jinja2 conditional for 'member_name'."""
        prompt = self.get_prompt(recipe)
        assert "{% if member_name" in prompt, (
            "Prompt missing Jinja2 conditional for 'member_name'"
        )

    def test_prompt_contains_name_mapping(self, recipe):
        """Prompt must contain org name-to-directory mapping."""
        prompt = self.get_prompt(recipe)
        # Check key mappings are present
        assert "Chris P" in prompt and "chris" in prompt, "Missing Chris P → chris mapping"
        assert "Gurkaran" in prompt and "gurkaran" in prompt, "Missing Gurkaran → gurkaran mapping"
        assert "Manoj" in prompt and "manoj" in prompt, "Missing Manoj → manoj mapping"
        assert "Ken" in prompt and "ken" in prompt, "Missing Ken → ken mapping"
        assert "Salil Das" in prompt and "salil" in prompt, "Missing Salil Das → salil mapping"
        assert "Samuel Lee" in prompt and "samuel" in prompt, "Missing Samuel Lee → samuel mapping"
        assert "Alex Lopez" in prompt and "alex" in prompt, "Missing Alex Lopez → alex mapping"

    def test_prompt_contains_activity_directory_reference(self, recipe):
        """Prompt must reference activity directory."""
        prompt = self.get_prompt(recipe)
        assert "activity" in prompt, "Prompt missing reference to activity directory"

    def test_prompt_contains_outcomes_md_reference(self, recipe):
        """Prompt must reference outcomes.md."""
        prompt = self.get_prompt(recipe)
        assert "outcomes.md" in prompt, "Prompt missing reference to outcomes.md"

    def test_prompt_contains_summary_md_write_instruction(self, recipe):
        """Prompt must instruct writing summary.md."""
        prompt = self.get_prompt(recipe)
        assert "summary.md" in prompt, "Prompt missing reference to summary.md"

    def test_prompt_contains_git_commit_instruction(self, recipe):
        """Prompt must contain git commit instruction with correct message format."""
        prompt = self.get_prompt(recipe)
        assert "git commit" in prompt, "Prompt missing git commit instruction"
        assert "alignment(" in prompt, "Prompt missing alignment commit message format"

    def test_prompt_contains_git_push_instruction(self, recipe):
        """Prompt must contain git push instruction."""
        prompt = self.get_prompt(recipe)
        assert "git push" in prompt, "Prompt missing git push instruction"

    def test_prompt_contains_cluster_by_repo(self, recipe):
        """Prompt must instruct clustering activity by repo."""
        prompt = self.get_prompt(recipe)
        assert "cluster" in prompt.lower() or "repo" in prompt.lower(), (
            "Prompt missing repo clustering instruction"
        )

    def test_prompt_contains_drives_field(self, recipe):
        """Prompt must reference 'drives:' field for outcome linking."""
        prompt = self.get_prompt(recipe)
        assert "drives:" in prompt, "Prompt missing 'drives:' field reference"

    def test_prompt_contains_weeks_directory_structure(self, recipe):
        """Prompt must reference weeks/<WEEK_ID> directory structure."""
        prompt = self.get_prompt(recipe)
        assert "weeks/" in prompt, "Prompt missing weeks/ directory reference"
