"""Tests for bundle.md - validates content matches spec requirements."""

import os

BUNDLE_MD_PATH = os.path.join(os.path.dirname(__file__), "..", "bundle.md")


def read_bundle_md():
    with open(BUNDLE_MD_PATH, "r") as f:
        return f.read()


def test_bundle_md_exists():
    assert os.path.exists(BUNDLE_MD_PATH), "bundle.md must exist"


def test_bundle_metadata_name():
    content = read_bundle_md()
    assert "name: team-pulse" in content, "bundle name must be 'team-pulse'"


def test_bundle_metadata_version():
    content = read_bundle_md()
    assert "version: 0.1.0" in content, "bundle version must be '0.1.0'"


def test_bundle_metadata_description():
    content = read_bundle_md()
    assert "Weekly commitment tracking" in content, (
        "description must mention weekly commitment tracking"
    )
    assert "outcome" in content.lower(), "description must mention outcomes"


def test_includes_amplifier_foundation():
    content = read_bundle_md()
    assert "git+https://github.com/microsoft/amplifier-foundation@main" in content, (
        "must include amplifier-foundation bundle"
    )


def test_includes_amplifier_bundle_recipes():
    content = read_bundle_md()
    assert (
        "git+https://github.com/microsoft/amplifier-bundle-recipes@main#subdirectory=behaviors/recipes.yaml"
        in content
    ), "must include amplifier-bundle-recipes"


def test_body_heading():
    content = read_bundle_md()
    assert "# Team Pulse" in content, "must have '# Team Pulse' heading"


def test_body_weekly_rhythm():
    content = read_bundle_md()
    assert "Monday" in content, "must describe Monday commitments"
    assert "Friday" in content, "must describe Friday audit"
    assert "Weekly Rhythm" in content, "must have Weekly Rhythm section"


def test_body_workflows_section():
    content = read_bundle_md()
    assert "log-commitments" in content, "must mention log-commitments workflow"
    assert "prep-audit" in content, "must mention prep-audit workflow"
    assert "draft-showcase" in content, "must mention draft-showcase workflow"
    assert "setup" in content, "must mention setup workflow"


def test_reference_team_pulse_instructions():
    content = read_bundle_md()
    assert "@team-pulse:context/team-pulse-instructions.md" in content, (
        "must reference @team-pulse:context/team-pulse-instructions.md"
    )


def test_reference_common_system_base():
    content = read_bundle_md()
    assert "@foundation:context/shared/common-system-base.md" in content, (
        "must reference @foundation:context/shared/common-system-base.md"
    )


def test_frontmatter_present():
    content = read_bundle_md()
    assert content.startswith("---"), "must start with YAML frontmatter delimiter"
