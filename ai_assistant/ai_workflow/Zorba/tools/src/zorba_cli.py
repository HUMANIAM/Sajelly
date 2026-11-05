#!/usr/bin/env python3
"""Set up and verify Zorba integrations from vendor-neutral definitions."""

import argparse
import json
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Set, TextIO, Tuple

from review_execution import LEVELS, REVIEWERS, SETTINGS_PATH, load_settings, review_plan


VENDORS = ("codex", "claude")
MANIFEST_PATH = Path("ai_assistant/ai_workflow/Zorba/specialists.json")
ROLES_PATH = Path("ai_assistant/ai_workflow/Zorba/roles")
CODEX_AGENTS_PATH = Path(".codex/agents")
CLI_PATH = Path("ai_assistant/ai_workflow/Zorba/tools/src/zorba_cli.py")
CANONICAL_GUIDE = "ai_assistant/ai_workflow/Zorba/roles/zorba.md"


def _plural(count: int, singular: str) -> str:
    """Return the singular or plural noun to agree with a dynamic count."""
    return singular if count == 1 else singular + "s"


# ===========================================================================
# 1. Data models & manifest validation
# ===========================================================================


class ZorbaConfigurationError(ValueError):
    """Raised when vendor-neutral Zorba configuration is invalid."""


@dataclass(frozen=True)
class Specialist:
    """Identity and canonical role mapping for one Zorba specialist."""

    identifier: str
    display_name: str
    role: str
    model: Optional[str] = None
    model_reasoning_effort: Optional[str] = None


@dataclass(frozen=True)
class ZorbaWorkspace:
    """Repository paths and transformations owned by the setup tool."""

    root: Path

    @property
    def manifest_file(self) -> Path:
        """Return the vendor-neutral specialist manifest path."""
        return self.root / MANIFEST_PATH

    @property
    def roles_directory(self) -> Path:
        """Return the canonical role directory."""
        return self.root / ROLES_PATH

    @property
    def codex_agents_directory(self) -> Path:
        """Return the generated project-scoped Codex directory."""
        return self.root / CODEX_AGENTS_PATH

    def load_specialists(self) -> Tuple[Specialist, ...]:
        """Load and validate the manifest and its canonical role documents."""
        try:
            data = json.loads(self.manifest_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise ZorbaConfigurationError(
                "Could not read {}: {}".format(self.manifest_file, error)
            ) from error

        if not isinstance(data, dict):
            raise ZorbaConfigurationError(
                "{} must contain a JSON object".format(self.manifest_file)
            )
        records = data.get("specialists")
        if not isinstance(records, list) or not records:
            raise ZorbaConfigurationError(
                "{} must define a non-empty list of specialists".format(
                    self.manifest_file
                )
            )

        specialists: List[Specialist] = []
        identifiers: Set[str] = set()
        roles: Set[str] = set()
        execution = None
        if any(isinstance(record, dict) and record.get("id") in REVIEWERS for record in records):
            try:
                execution = load_settings(self.root / SETTINGS_PATH)
            except (OSError, ValueError, ImportError) as error:
                raise ZorbaConfigurationError("Invalid review execution settings: {}".format(error)) from error
        for position, record in enumerate(records, start=1):
            specialist = self._validate_specialist(record, position, execution)
            if specialist.identifier in identifiers:
                raise ZorbaConfigurationError(
                    "Duplicate specialist id: {}".format(specialist.identifier)
                )
            if specialist.role in roles:
                raise ZorbaConfigurationError(
                    "Duplicate specialist role: {}".format(specialist.role)
                )
            identifiers.add(specialist.identifier)
            roles.add(specialist.role)
            self.role_description(specialist)
            specialists.append(specialist)

        guide = self.roles_directory / "zorba.md"
        if not guide.is_file():
            raise ZorbaConfigurationError(
                "Canonical Zorba Guide is missing: {}".format(guide)
            )
        return tuple(specialists)

    def _validate_specialist(
        self, record: object, position: int, execution: Optional[Dict[str, Any]] = None
    ) -> Specialist:
        """Validate one untrusted manifest record."""
        if not isinstance(record, dict):
            raise ZorbaConfigurationError(
                "Specialist {} must be an object".format(position)
            )

        values: Dict[str, str] = {}
        for field in ("id", "display_name", "role"):
            value = record.get(field)
            if not isinstance(value, str) or not value.strip():
                raise ZorbaConfigurationError(
                    "Specialist {} field {} must be a non-empty string".format(
                        position, field
                    )
                )
            values[field] = value

        identifier = values["id"]
        display_name = values["display_name"]
        role = values["role"]
        if re.fullmatch(r"[a-z][a-z0-9_]*", identifier) is None:
            raise ZorbaConfigurationError(
                "Invalid specialist id: {}".format(identifier)
            )
        if '"""' in display_name:
            raise ZorbaConfigurationError(
                "Specialist display name cannot contain triple quotes: {}".format(
                    display_name
                )
            )
        if Path(role).name != role or not role.endswith(".md"):
            raise ZorbaConfigurationError(
                "Specialist role must be a Markdown filename: {}".format(role)
            )
        role_path = self.roles_directory / role
        if not role_path.is_file():
            raise ZorbaConfigurationError(
                "Canonical role document is missing: {}".format(role_path)
            )
        profile = {}
        if identifier in REVIEWERS and execution is not None:
            profile = execution["profiles"][execution["lead_profile"]]
        return Specialist(
            identifier, display_name, role,
            profile.get("model"), profile.get("model_reasoning_effort"),
        )

    def role_description(self, specialist: Specialist) -> str:
        """Derive a concise description from the canonical role document."""
        role_path = self.roles_directory / specialist.role
        try:
            lines = role_path.read_text(encoding="utf-8").splitlines()
        except OSError as error:
            raise ZorbaConfigurationError(
                "Could not read canonical role {}: {}".format(role_path, error)
            ) from error

        # Match the "Why I exist" heading tolerantly: ignore surrounding
        # whitespace and heading casing so minor edits to a role file do not
        # break description extraction.
        heading_index: Optional[int] = None
        for index, line in enumerate(lines):
            if line.strip().lower() == "## why i exist":
                heading_index = index
                break
        if heading_index is None:
            raise ZorbaConfigurationError(
                "Canonical role lacks a 'Why I exist' section: {}".format(
                    role_path
                )
            )

        paragraph: List[str] = []
        for line in lines[heading_index + 1 :]:
            stripped = line.strip()
            if not stripped:
                if paragraph:
                    break
                continue
            if stripped.startswith("#"):
                break
            paragraph.append(stripped)

        if not paragraph:
            raise ZorbaConfigurationError(
                "Canonical role lacks a description after 'Why I exist': {}".format(
                    role_path
                )
            )
        description = " ".join(paragraph)
        description = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", description)
        return re.sub(r"[*_`]", "", description)

    # -----------------------------------------------------------------------
    # 2. Codex adapter rendering & drift detection
    # -----------------------------------------------------------------------

    def expected_codex_files(
        self,
        specialists: Sequence[Specialist],
    ) -> Dict[str, str]:
        """Render all expected Codex files from canonical Zorba sources."""
        return {
            self._codex_filename(specialist): self._render_codex_agent(specialist)
            for specialist in specialists
        }

    def orphaned_codex_files(self, expected_files: Dict[str, str]) -> List[str]:
        """Return sorted .toml files present but not defined by the manifest."""
        directory = self.codex_agents_directory
        if not directory.is_dir():
            return []
        return sorted(
            path.name
            for path in directory.glob("*.toml")
            if path.is_file() and path.name not in expected_files
        )

    def codex_drift(self, specialists: Sequence[Specialist]) -> List[str]:
        """Return missing, stale, or orphaned generated Codex files."""
        expected_files = self.expected_codex_files(specialists)
        problems: List[str] = []
        for filename, expected in expected_files.items():
            installed = self.codex_agents_directory / filename
            if not installed.is_file():
                problems.append("{} is missing".format(filename))
                continue
            try:
                actual = installed.read_text(encoding="utf-8")
            except OSError as error:
                problems.append("{} cannot be read: {}".format(filename, error))
                continue
            if actual != expected:
                problems.append(
                    "{} differs from vendor-neutral Zorba".format(filename)
                )
        for orphan in self.orphaned_codex_files(expected_files):
            problems.append(
                "{} is unexpected (not in vendor-neutral Zorba)".format(orphan)
            )
        return problems

    def write_codex_setup(
        self,
        specialists: Sequence[Specialist],
        output: TextIO,
    ) -> bool:
        """Generate Codex files, returning whether every write succeeded."""
        expected_files = self.expected_codex_files(specialists)
        try:
            self.codex_agents_directory.mkdir(parents=True, exist_ok=True)
            for filename, content in expected_files.items():
                destination = self.codex_agents_directory / filename
                destination.write_text(content, encoding="utf-8")
        except OSError as error:
            print("[FAIL] Could not write Codex setup: {}".format(error), file=output)
            return False

        count = len(specialists)
        print(
            "[SYNC] Generated {} Codex {} from vendor-neutral Zorba at {}".format(
                count, _plural(count, "specialist"), self.codex_agents_directory
            ),
            file=output,
        )
        return True

    def remove_orphaned_codex_files(
        self,
        names: Sequence[str],
        output: TextIO,
    ) -> bool:
        """Delete confirmed orphan files, returning whether all deletions worked."""
        try:
            for name in names:
                (self.codex_agents_directory / name).unlink()
                print(
                    "[SYNC] Deleted Codex agent no longer in "
                    "specialists.json: {}".format(name),
                    file=output,
                )
        except OSError as error:
            print("[FAIL] Could not delete Codex agent: {}".format(error), file=output)
            return False
        return True

    @staticmethod
    def _codex_filename(specialist: Specialist) -> str:
        """Return the project-scoped Codex filename for a specialist."""
        return specialist.identifier.replace("_", "-") + ".toml"

    def _render_codex_agent(self, specialist: Specialist) -> str:
        """Render one thin Codex adapter from a canonical role."""
        canonical_role = "ai_assistant/ai_workflow/Zorba/roles/{}".format(
            specialist.role
        )
        instructions = "\n\n".join(
            (
                "Act as Zorba's {display_name} for the assigned work.",
                (
                    "Before doing substantive work, read {canonical_role} in "
                    "full. That file is the canonical definition of your "
                    "purpose, inputs, responsibilities, ownership boundary, "
                    "output contract, and completion criteria. Follow it "
                    "without copying or redefining it here."
                ),
                (
                    "Consult ai_assistant/ai_workflow/Zorba/manifesto.md, "
                    "ai_assistant/ai_workflow/Zorba/requirements.md, existing "
                    "feature artifacts, and project context when they are "
                    "relevant. Preserve Zorba's non-linear workflow: perform "
                    "only this role's needed contribution, do not silently take "
                    "over another role, and do not require every role to "
                    "participate. If work owned by another role is needed, "
                    "return a concise handoff request naming the role, "
                    "objective, relevant context, existing decisions, and open "
                    "questions."
                ),
                (
                    "Follow all applicable repository instructions. Treat the "
                    "repository's tracked Zorba documents as the source of "
                    "truth; do not rely on a vendor-specific copy of the "
                    "workflow."
                ),
            )
        ).format(
            display_name=specialist.display_name,
            canonical_role=canonical_role,
        )
        description = "Zorba {}. {}".format(
            specialist.display_name,
            self.role_description(specialist),
        )
        # json.dumps emits a JSON string literal, which is also a valid TOML
        # single-line basic string. Using it for every field keeps rendering
        # safe no matter what a display name or role description contains
        # (quotes, triple quotes, or backslashes) without fragile escaping of
        # a triple-quoted block.
        return (
            "name = {}\n".format(json.dumps(specialist.identifier))
            + "description = {}\n".format(json.dumps(description))
            + ("model = {}\n".format(json.dumps(specialist.model)) if specialist.model else "")
            + ("model_reasoning_effort = {}\n".format(json.dumps(specialist.model_reasoning_effort)) if specialist.model_reasoning_effort else "")
            + "developer_instructions = {}\n".format(json.dumps(instructions))
        )


# ===========================================================================
# 3. CLI actions (check, setup, sync)
# ===========================================================================


def find_repository_root(start: Path) -> Path:
    """Return the nearest parent containing repository metadata."""
    for candidate in (start,) + tuple(start.parents):
        if (candidate / ".git").exists():
            return candidate
    raise RuntimeError("Could not locate the Sajelly repository root")


def ask_confirmation(prompt: str, input_fn: Callable[[str], str]) -> bool:
    """Return whether the contributor explicitly answered yes."""
    try:
        answer = input_fn("{} [y/N] ".format(prompt))
    except EOFError:
        return False
    return answer.strip().lower() in {"y", "yes"}


def synchronize_codex_files(
    workspace: ZorbaWorkspace,
    specialists: Sequence[Specialist],
    input_fn: Callable[[str], str],
    output: TextIO,
) -> None:
    """Refresh generated files and ask before deleting orphaned agents."""
    expected_files = workspace.expected_codex_files(specialists)
    orphaned = workspace.orphaned_codex_files(expected_files)
    delete_orphaned: List[str] = []
    if orphaned:
        print(
            "[SYNC] Codex agents no longer present in specialists.json:",
            file=output,
        )
        for name in orphaned:
            print("       - {}".format(name), file=output)
        for name in orphaned:
            if ask_confirmation(
                "Delete orphaned Codex agent {}?".format(name),
                input_fn,
            ):
                delete_orphaned.append(name)

    if not workspace.write_codex_setup(specialists, output):
        return
    if delete_orphaned:
        workspace.remove_orphaned_codex_files(delete_orphaned, output)
    preserved = [name for name in orphaned if name not in delete_orphaned]
    if preserved:
        print(
            "[UNCHANGED] Orphaned Codex agents preserved by user choice: {}".format(
                ", ".join(preserved)
            ),
            file=output,
        )


def setup_codex(
    workspace: ZorbaWorkspace,
    specialists: Sequence[Specialist],
    input_fn: Callable[[str], str],
    output: TextIO,
) -> None:
    """Offer creation for a missing setup or sync for an existing setup."""
    target = workspace.codex_agents_directory
    if target.exists():
        if not target.is_dir():
            print(
                "[FAIL] Codex setup path is not a directory: {}".format(target),
                file=output,
            )
            return
        if not workspace.codex_drift(specialists):
            print(
                "[UNCHANGED] Codex already matches vendor-neutral Zorba.",
                file=output,
            )
            return
        if ask_confirmation(
            "Codex setup already exists. Would you like to sync it from "
            "vendor-neutral Zorba?",
            input_fn,
        ):
            synchronize_codex_files(workspace, specialists, input_fn, output)
        else:
            print("[UNCHANGED] Existing Codex setup was not synced.", file=output)
        return

    if ask_confirmation(
        "Codex setup does not exist at {}. Would you like to create it?".format(
            target
        ),
        input_fn,
    ):
        workspace.write_codex_setup(specialists, output)
    else:
        print("[UNCHANGED] Codex setup was not created.", file=output)


def sync_codex(
    workspace: ZorbaWorkspace,
    specialists: Sequence[Specialist],
    input_fn: Callable[[str], str],
    output: TextIO,
) -> None:
    """Sync Codex, offering setup once when its folder is missing."""
    target = workspace.codex_agents_directory
    if not target.exists():
        if ask_confirmation(
            "Codex setup is missing. Would you like to set it up now?",
            input_fn,
        ):
            workspace.write_codex_setup(specialists, output)
        else:
            print("[UNCHANGED] Codex setup was not created.", file=output)
        return
    if not target.is_dir():
        print(
            "[FAIL] Codex setup path is not a directory: {}".format(target),
            file=output,
        )
        return

    if workspace.codex_drift(specialists):
        synchronize_codex_files(workspace, specialists, input_fn, output)
    else:
        print(
            "[UNCHANGED] Codex already matches vendor-neutral Zorba.",
            file=output,
        )


def check_entry_file(
    workspace: ZorbaWorkspace,
    filename: str,
    output: TextIO,
) -> bool:
    """Check that a client entry file points at the canonical Zorba Guide."""
    path = workspace.root / filename
    if not path.is_file():
        print("[FAIL] {} is missing".format(filename), file=output)
        return False
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as error:
        print("[FAIL] Could not read {}: {}".format(filename, error), file=output)
        return False
    if CANONICAL_GUIDE not in content:
        print(
            "[FAIL] {} does not reference the canonical Zorba Guide".format(
                filename
            ),
            file=output,
        )
        return False
    print(
        "[PASS] {} routes Zorba to the canonical Guide".format(filename),
        file=output,
    )
    return True


def report_executable(name: str, label: str, output: TextIO) -> None:
    """Report a detectable CLI without treating extensions as absent."""
    executable = shutil.which(name)
    if executable:
        print("[PASS] {} CLI detected at {}".format(label, executable), file=output)
        return
    print(
        "[WARN] {} CLI not detected; an IDE extension cannot be detected here".format(
            label
        ),
        file=output,
    )


def check_all(workspace: ZorbaWorkspace, output: TextIO) -> bool:
    """Report vendor-neutral, Codex, and Claude readiness without mutation."""
    print("Zorba — AI assistant setup\n", file=output)
    try:
        specialists = workspace.load_specialists()
    except ZorbaConfigurationError as error:
        print("[FAIL] Vendor-neutral Zorba: {}".format(error), file=output)
        return False

    count = len(specialists)
    print(
        "[PASS] Vendor-neutral Zorba defines the Guide and {} canonical {}".format(
            count, _plural(count, "specialist")
        ),
        file=output,
    )

    print("\nCodex", file=output)
    report_executable("codex", "Codex", output)
    entry_ready = check_entry_file(workspace, "AGENTS.md", output)
    target = workspace.codex_agents_directory
    if not target.exists():
        print("[NOT SET UP] Codex specialists: {} is missing".format(target), file=output)
        print("             Run: python3 {} --setup codex".format(CLI_PATH), file=output)
        codex_ready = False
    elif not target.is_dir():
        print(
            "[FAIL] Codex setup path is not a directory: {}".format(target),
            file=output,
        )
        codex_ready = False
    else:
        problems = workspace.codex_drift(specialists)
        if problems:
            print(
                "[FAIL] Codex specialists do not match vendor-neutral Zorba",
                file=output,
            )
            for problem in problems:
                print("       - {}".format(problem), file=output)
            print("       Run: python3 {} --sync codex".format(CLI_PATH), file=output)
            codex_ready = False
        else:
            print(
                "[PASS] Codex matches vendor-neutral Zorba ({} {})".format(
                    count, _plural(count, "specialist")
                ),
                file=output,
            )
            codex_ready = True

    print("\nClaude", file=output)
    report_executable("claude", "Claude", output)
    check_entry_file(workspace, "CLAUDE.md", output)
    print("[WIP] Claude specialist setup and sync are not implemented yet", file=output)

    print(
        "\n[NOT VERIFIED] Client loading and specialist invocation require a "
        "fresh live session",
        file=output,
    )
    print(
        "Next after setup: open a fresh client and say: "
        "Zorba, help me get started with Sajelly.",
        file=output,
    )
    return entry_ready and codex_ready


def build_parser() -> argparse.ArgumentParser:
    """Build the contributor setup and read-only review planning interface."""
    parser = argparse.ArgumentParser(
        prog="zorba_cli.py",
        description=(
            "Zorba helps technical and non-technical contributors set up an AI "
            "assistant for Sajelly. Codex setup is available; Claude specialist "
            "setup is work in progress."
        ),
        epilog=(
            "Start with: python3 {} --check\n".format(CLI_PATH)
            + "Then set up a supported client, for example: "
            + "python3 {} --setup codex".format(CLI_PATH)
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument(
        "--review-plan",
        action="store_true",
        help="print a JSON model/effort plan for selected review subjects; do not launch agents",
    )
    parser.add_argument("--subjects", nargs="+", help="review subject IDs from review_execution.json")
    parser.add_argument("--risk", choices=LEVELS, help="assessed change risk; absent means configured default")
    parser.add_argument("--system-criticality", choices=LEVELS, help="impact of failure for the reviewed system")
    actions.add_argument(
        "--check",
        action="store_true",
        help="report vendor-neutral, Codex, and Claude setup status",
    )
    actions.add_argument(
        "--setup",
        choices=VENDORS,
        metavar="{codex,claude}",
        help="set up one client, asking before files are created or synced",
    )
    actions.add_argument(
        "--sync",
        choices=VENDORS,
        metavar="{codex,claude}",
        help="sync one client from vendor-neutral Zorba",
    )
    return parser


def main(
    argv: Optional[Sequence[str]] = None,
    input_fn: Callable[[str], str] = input,
    output: Optional[TextIO] = None,
    repository_root: Optional[Path] = None,
) -> int:
    """Run the Zorba setup CLI and return 0, 1, or unsupported-vendor 2."""
    stream = output if output is not None else sys.stdout
    parser = build_parser()
    arguments = parser.parse_args(argv)
    root = repository_root or find_repository_root(Path(__file__).resolve().parent)
    workspace = ZorbaWorkspace(root)

    if arguments.review_plan:
        try:
            settings = load_settings(root / SETTINGS_PATH)
            plan = review_plan(settings, arguments.subjects or [], arguments.risk, arguments.system_criticality)
        except (OSError, ValueError, ImportError) as error:
            print(json.dumps({"error": str(error)}), file=stream)
            return 1
        print(json.dumps(plan, indent=2), file=stream)
        return 0
    if arguments.subjects or arguments.risk or arguments.system_criticality:
        parser.error("--subjects, --risk and --system-criticality require --review-plan")

    if not (arguments.check or arguments.setup or arguments.sync):
        print("Zorba — Sajelly AI assistant setup\n", file=stream)
        print(
            "I help contributors check and set up supported AI assistants from "
            "Sajelly's vendor-neutral Zorba definitions.",
            file=stream,
        )
        print(file=stream)
        parser.print_help(file=stream)
        return 0

    if arguments.check:
        return 0 if check_all(workspace, stream) else 1

    try:
        specialists = workspace.load_specialists()
    except ZorbaConfigurationError as error:
        print("[FAIL] Vendor-neutral Zorba: {}".format(error), file=stream)
        return 1

    vendor = arguments.setup or arguments.sync
    if vendor == "claude":
        print(
            "[WIP] Claude specialist setup and sync are not implemented yet. "
            "No files were changed.",
            file=stream,
        )
        return 2

    if arguments.setup:
        setup_codex(workspace, specialists, input_fn, stream)
    else:
        sync_codex(workspace, specialists, input_fn, stream)
    return 0 if check_all(workspace, stream) else 1


if __name__ == "__main__":
    raise SystemExit(main())
