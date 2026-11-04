"""Behavioral tests for the Zorba contributor setup tool."""

import io
import json
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import pytest

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

from zorba_cli import ZorbaConfigurationError, ZorbaWorkspace, main


SpecialistSeed = Tuple[str, str]


def default_specialists(count: int) -> List[SpecialistSeed]:
    """Return distinct specialist identities for an isolated repository."""
    names = [
        ("architect", "Architect"),
        ("builder", "Builder"),
        ("reviewer", "Reviewer"),
        ("planner", "Planner"),
        ("tester", "Tester"),
        ("scribe", "Scribe"),
        ("deployer", "Deployment Engineer"),
        ("researcher", "Researcher"),
    ]
    assert count <= len(names)
    return names[:count]


def build_repo(
    root: Path,
    specialists: Sequence[SpecialistSeed],
    guide: bool = True,
    why_heading: str = "## Why I exist",
) -> Path:
    """Create a minimal vendor-neutral Zorba repository fixture."""
    (root / ".git").mkdir(parents=True, exist_ok=True)
    roles = root / "ai_assistant/ai_workflow/Zorba/roles"
    roles.mkdir(parents=True, exist_ok=True)
    if guide:
        (roles / "zorba.md").write_text("# Zorba Guide\n", encoding="utf-8")

    records = []
    for identifier, display_name in specialists:
        role_file = identifier.replace("_", "-") + ".md"
        (roles / role_file).write_text(
            "# {name}\n\n{heading}\n\nI own the {identifier} responsibilities "
            "for the team and keep them moving.\n".format(
                name=display_name,
                heading=why_heading,
                identifier=identifier,
            ),
            encoding="utf-8",
        )
        records.append(
            {"id": identifier, "display_name": display_name, "role": role_file}
        )

    manifest = root / "ai_assistant/ai_workflow/Zorba/specialists.json"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps({"specialists": records}), encoding="utf-8")

    pointer = "See ai_assistant/ai_workflow/Zorba/roles/zorba.md\n"
    (root / "AGENTS.md").write_text(pointer, encoding="utf-8")
    (root / "CLAUDE.md").write_text(pointer, encoding="utf-8")
    return root


def run_cli(
    root: Path,
    arguments: Sequence[str],
    answers: Sequence[str] = (),
) -> Tuple[int, str, List[str]]:
    """Run the public CLI boundary with deterministic confirmation answers."""
    output = io.StringIO()
    prompts: List[str] = []
    remaining_answers = iter(answers)

    def input_fn(prompt: str) -> str:
        prompts.append(prompt)
        return next(remaining_answers, "")

    status = main(
        arguments,
        input_fn=input_fn,
        output=output,
        repository_root=root,
    )
    return status, output.getvalue(), prompts


def setup_with_orphan(root: Path) -> Tuple[ZorbaWorkspace, Path]:
    """Create a synchronized setup plus one agent absent from the manifest."""
    workspace = ZorbaWorkspace(root)
    specialists = workspace.load_specialists()
    assert workspace.write_codex_setup(specialists, io.StringIO())
    orphan = workspace.codex_agents_directory / "old-agent.toml"
    orphan.write_text('name = "old-agent"\n', encoding="utf-8")
    return workspace, orphan


def snapshot(directory: Path) -> Dict[str, bytes]:
    """Capture generated file contents for an immutability assertion."""
    return {
        path.name: path.read_bytes()
        for path in sorted(directory.glob("*.toml"))
    }


def test_no_arguments_explains_zorba_and_available_commands(tmp_path: Path) -> None:
    root = build_repo(tmp_path, default_specialists(2))

    status, output, prompts = run_cli(root, [])

    assert status == 0
    assert prompts == []
    assert "Zorba — Sajelly AI assistant setup" in output
    assert "technical and non-technical contributors" in output
    assert "--check" in output
    assert "--setup" in output
    assert "--sync" in output


@pytest.mark.parametrize("count", [6, 8])
def test_dynamic_team_sizes_load_and_sync(tmp_path: Path, count: int) -> None:
    root = build_repo(tmp_path, default_specialists(count))
    workspace = ZorbaWorkspace(root)

    specialists = workspace.load_specialists()
    assert len(specialists) == count
    assert workspace.write_codex_setup(specialists, io.StringIO())
    assert len(list(workspace.codex_agents_directory.glob("*.toml"))) == count
    assert workspace.codex_drift(specialists) == []


def test_check_reports_dynamic_count(tmp_path: Path) -> None:
    root = build_repo(tmp_path, default_specialists(6))
    workspace = ZorbaWorkspace(root)
    workspace.write_codex_setup(workspace.load_specialists(), io.StringIO())

    status, output, prompts = run_cli(root, ["--check"])

    assert status == 0
    assert prompts == []
    assert "6 canonical specialists" in output
    assert "seven" not in output.lower()


def test_empty_specialist_list_is_rejected(tmp_path: Path) -> None:
    root = build_repo(tmp_path, [])
    with pytest.raises(ZorbaConfigurationError):
        ZorbaWorkspace(root).load_specialists()


def test_singular_specialist_count_is_grammatical(tmp_path: Path) -> None:
    root = build_repo(tmp_path, default_specialists(1))
    workspace = ZorbaWorkspace(root)
    workspace.write_codex_setup(workspace.load_specialists(), io.StringIO())

    _status, output, _prompts = run_cli(root, ["--check"])

    assert "1 canonical specialist" in output
    assert "1 canonical specialists" not in output


def test_check_missing_setup_is_read_only(tmp_path: Path) -> None:
    root = build_repo(tmp_path, default_specialists(2))

    status, output, prompts = run_cli(root, ["--check"])

    assert status == 1
    assert prompts == []
    assert "[NOT SET UP]" in output
    assert not (root / ".codex").exists()


def test_check_ready_setup_is_read_only(tmp_path: Path) -> None:
    root = build_repo(tmp_path, default_specialists(2))
    workspace = ZorbaWorkspace(root)
    workspace.write_codex_setup(workspace.load_specialists(), io.StringIO())
    before = snapshot(workspace.codex_agents_directory)

    status, _output, prompts = run_cli(root, ["--check"])

    assert status == 0
    assert prompts == []
    assert snapshot(workspace.codex_agents_directory) == before


def test_setup_missing_directory_requires_confirmation(tmp_path: Path) -> None:
    root = build_repo(tmp_path, default_specialists(2))

    status, output, prompts = run_cli(
        root,
        ["--setup", "codex"],
        answers=["no"],
    )

    assert status == 1
    assert len(prompts) == 1
    assert "Would you like to create it?" in prompts[0]
    assert "[UNCHANGED]" in output
    assert not (root / ".codex").exists()


def test_setup_missing_directory_creates_after_confirmation(tmp_path: Path) -> None:
    root = build_repo(tmp_path, default_specialists(2))

    status, output, prompts = run_cli(
        root,
        ["--setup", "codex"],
        answers=["yes"],
    )

    assert status == 0, output
    assert len(prompts) == 1
    assert len(list((root / ".codex/agents").glob("*.toml"))) == 2


def test_sync_missing_directory_requires_setup_confirmation(tmp_path: Path) -> None:
    root = build_repo(tmp_path, default_specialists(2))

    status, output, prompts = run_cli(
        root,
        ["--sync", "codex"],
        answers=["no"],
    )

    assert status == 1
    assert len(prompts) == 1
    assert "Would you like to set it up now?" in prompts[0]
    assert "[UNCHANGED]" in output
    assert not (root / ".codex").exists()


def test_sync_missing_directory_sets_up_after_one_confirmation(
    tmp_path: Path,
) -> None:
    root = build_repo(tmp_path, default_specialists(2))

    status, output, prompts = run_cli(
        root,
        ["--sync", "codex"],
        answers=["yes"],
    )

    assert status == 0, output
    assert len(prompts) == 1
    assert "Would you like to set it up now?" in prompts[0]
    assert len(list((root / ".codex/agents").glob("*.toml"))) == 2


def test_check_flags_orphaned_agent(tmp_path: Path) -> None:
    root = build_repo(tmp_path, default_specialists(2))
    workspace, orphan = setup_with_orphan(root)

    problems = workspace.codex_drift(workspace.load_specialists())

    assert any(orphan.name in problem and "unexpected" in problem for problem in problems)
    status, output, _prompts = run_cli(root, ["--check"])
    assert status == 1
    assert orphan.name in output


def test_sync_preserves_orphan_when_deletion_is_declined(tmp_path: Path) -> None:
    root = build_repo(tmp_path, default_specialists(2))
    _workspace, orphan = setup_with_orphan(root)

    status, output, prompts = run_cli(
        root,
        ["--sync", "codex"],
        answers=["no"],
    )

    assert status == 1
    assert len(prompts) == 1
    assert "Delete orphaned Codex agent old-agent.toml?" in prompts[0]
    assert orphan.exists()
    assert "preserved by user choice" in output


def test_sync_deletes_orphan_after_confirmation(tmp_path: Path) -> None:
    root = build_repo(tmp_path, default_specialists(2))
    workspace, orphan = setup_with_orphan(root)

    status, output, prompts = run_cli(
        root,
        ["--sync", "codex"],
        answers=["yes"],
    )

    assert status == 0, output
    assert len(prompts) == 1
    assert "Delete orphaned Codex agent old-agent.toml?" in prompts[0]
    assert not orphan.exists()
    assert workspace.codex_drift(workspace.load_specialists()) == []


def test_sync_asks_separately_for_each_orphan(tmp_path: Path) -> None:
    root = build_repo(tmp_path, default_specialists(2))
    workspace = ZorbaWorkspace(root)
    specialists = workspace.load_specialists()
    assert workspace.write_codex_setup(specialists, io.StringIO())
    first = workspace.codex_agents_directory / "former-a.toml"
    second = workspace.codex_agents_directory / "former-b.toml"
    first.write_text('name = "former-a"\n', encoding="utf-8")
    second.write_text('name = "former-b"\n', encoding="utf-8")

    status, output, prompts = run_cli(
        root,
        ["--sync", "codex"],
        answers=["yes", "no"],
    )

    assert status == 1
    assert len(prompts) == 2
    assert first.name in prompts[0]
    assert second.name in prompts[1]
    assert not first.exists()
    assert second.exists()
    assert second.name in output


def test_setup_drift_asks_to_sync_then_to_delete_orphan(tmp_path: Path) -> None:
    root = build_repo(tmp_path, default_specialists(2))
    workspace, orphan = setup_with_orphan(root)
    victim = next(
        path
        for path in workspace.codex_agents_directory.glob("*.toml")
        if path != orphan
    )
    victim.write_text('name = "stale"\n', encoding="utf-8")

    status, output, prompts = run_cli(
        root,
        ["--setup", "codex"],
        answers=["yes", "no"],
    )

    assert status == 1
    assert len(prompts) == 2
    assert "Would you like to sync it" in prompts[0]
    assert "Delete orphaned Codex agent old-agent.toml?" in prompts[1]
    assert orphan.exists()
    assert "preserved by user choice" in output
    assert "stale" not in victim.read_text(encoding="utf-8")


def test_setup_does_not_prompt_when_already_synchronized(tmp_path: Path) -> None:
    root = build_repo(tmp_path, default_specialists(3))
    workspace = ZorbaWorkspace(root)
    workspace.write_codex_setup(workspace.load_specialists(), io.StringIO())

    status, output, prompts = run_cli(root, ["--setup", "codex"])

    assert status == 0
    assert prompts == []
    assert "already matches" in output


def test_role_heading_match_is_case_and_space_tolerant(tmp_path: Path) -> None:
    root = build_repo(
        tmp_path,
        default_specialists(1),
        why_heading="## Why I Exist   ",
    )
    workspace = ZorbaWorkspace(root)

    specialists = workspace.load_specialists()

    assert "responsibilities" in workspace.role_description(specialists[0])


def test_missing_role_heading_is_rejected(tmp_path: Path) -> None:
    root = build_repo(tmp_path, default_specialists(1))
    roles = root / "ai_assistant/ai_workflow/Zorba/roles"
    role = next(path for path in roles.glob("*.md") if path.name != "zorba.md")
    role.write_text("# Role\n\n## Something else\n\nText.\n", encoding="utf-8")

    with pytest.raises(ZorbaConfigurationError):
        ZorbaWorkspace(root).load_specialists()


def test_special_characters_render_as_valid_toml(tmp_path: Path) -> None:
    root = build_repo(tmp_path, [("architect", 'The "Lead" \\ Architect')])
    workspace = ZorbaWorkspace(root)
    specialists = workspace.load_specialists()
    content = next(iter(workspace.expected_codex_files(specialists).values()))

    parsed = tomllib.loads(content)

    assert parsed["name"] == "architect"
    assert 'The "Lead" \\ Architect' in parsed["developer_instructions"]
    assert 'The "Lead" \\ Architect' in parsed["description"]


@pytest.mark.parametrize("action", ["--setup", "--sync"])
def test_claude_actions_report_wip_without_changes(
    tmp_path: Path,
    action: str,
) -> None:
    root = build_repo(tmp_path, default_specialists(2))

    status, output, prompts = run_cli(root, [action, "claude"])

    assert status == 2
    assert prompts == []
    assert "[WIP]" in output
    assert not (root / ".claude").exists()
