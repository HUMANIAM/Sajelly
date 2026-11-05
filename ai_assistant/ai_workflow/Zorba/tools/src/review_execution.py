"""Resolve editable review settings without launching models or editing Codex."""

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional, Sequence


SETTINGS_PATH = Path(
    "ai_assistant/ai_workflow/Zorba/roles/engineering_review/common/review_execution.json"
)
PROFILES = ("lightweight", "standard", "deep", "critical")
LEVELS = ("low", "medium", "high", "critical")
REVIEWERS = ("frontend_engineering_reviewer", "backend_engineering_reviewer")


def validate_settings(settings: Dict[str, Any], schema_path: Path) -> None:
    """Validate the UI schema, model/effort pairs, references and risk floors."""
    from jsonschema import Draft202012Validator

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    errors = sorted(
        Draft202012Validator(schema).iter_errors(settings),
        key=lambda error: str(list(error.absolute_path)),
    )
    if errors:
        raise ValueError("Invalid review settings: {}".format(errors[0].message))
    for name, profile in settings["profiles"].items():
        efforts = settings["models"].get(profile["model"], [])
        if profile["model_reasoning_effort"] not in efforts:
            raise ValueError("Unsupported configured model/effort pair: {}".format(name))
    floors = [PROFILES.index(settings["risk_profiles"][level]) for level in LEVELS]
    if floors != sorted(floors) or floors[2] < 2 or floors[3] < 3:
        raise ValueError("Risk floors must increase; high requires deep and critical requires critical")


def load_settings(path: Path) -> Dict[str, Any]:
    """Read and validate the canonical settings and its adjacent UI schema."""
    settings = json.loads(path.read_text(encoding="utf-8"))
    validate_settings(settings, path.with_suffix(".schema.json"))
    return settings


def save_settings(path: Path, settings: Dict[str, Any]) -> None:
    """Validate and atomically replace settings for a future local UI caller.

    The caller owns user authorization and concurrent-edit handling. This does
    not sync Codex files, launch models, or claim those models are accessible.
    """
    validate_settings(settings, path.with_suffix(".schema.json"))
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=str(path.parent), delete=False
        ) as output:
            temporary = Path(output.name)
            json.dump(settings, output, indent=2)
            output.write("\n")
        os.replace(str(temporary), str(path))
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def review_plan(
    settings: Dict[str, Any],
    subjects: Sequence[str],
    change_risk: Optional[str] = None,
    system_criticality: Optional[str] = None,
) -> Dict[str, Any]:
    """Select only requested subjects, raised to the higher impact floor.

    Risk and criticality are assessed inputs, not inferred from source by this
    resolver. The lead must revisit them if changed behavior reveals more risk.
    """
    risk = change_risk or settings["defaults"]["change_risk"]
    criticality = system_criticality or settings["defaults"]["system_criticality"]
    if risk not in LEVELS or criticality not in LEVELS:
        raise ValueError("Risk and system criticality must be low, medium, high or critical")
    if not subjects or len(subjects) != len(set(subjects)):
        raise ValueError("Select at least one distinct review subject")
    floor_level = max((risk, criticality), key=LEVELS.index)
    floor = settings["risk_profiles"][floor_level]
    assignments = []
    for name in subjects:
        subject = settings["subjects"].get(name)
        if subject is None or not subject["enabled"]:
            raise ValueError("Unknown or disabled review subject: {}".format(name))
        profile = max((subject["profile"], floor), key=PROFILES.index)
        assignments.append({
            "subject": name,
            "title": subject["title"],
            "focus": subject["focus"],
            "base_profile": subject["profile"],
            "effective_profile": profile,
            **settings["profiles"][profile],
        })
    lead_profile = settings["lead_profile"]
    return {
        "settings_version": settings["version"],
        "change_risk": risk,
        "system_criticality": criticality,
        "minimum_profile": floor,
        "lead": {"profile": lead_profile, **settings["profiles"][lead_profile]},
        "subjects": assignments,
        "max_parallel_helpers": settings["max_parallel_helpers"],
        "launch_policy": "Explicitly pass both model and reasoning effort; no silent fallback. Respect runtime slots and wait for every requested contribution.",
        "availability": "Not checked by planning. Confirm each launch; record actual runtime metadata when exposed and any unavailable model or effort.",
    }
