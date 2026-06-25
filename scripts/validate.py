#!/usr/bin/env python3
"""Validate the Software Design Philosophy Codex plugin without third-party packages."""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path
from typing import Any

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = PLUGIN_ROOT / "skills" / "software-design-philosophy"
REPOSITORY_URL = "https://github.com/Tazkus/software-design-philosophy-skill"
EXPECTED_RESOURCES = [
    SKILL_ROOT / "references" / "principles.md",
    SKILL_ROOT / "references" / "review-rubric.md",
    SKILL_ROOT / "references" / "examples.md",
    SKILL_ROOT / "assets" / "design-review-template.md",
]


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def load_json(path: Path, errors: list[str]) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing JSON file: {path.relative_to(PLUGIN_ROOT)}", errors)
        return {}
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path.relative_to(PLUGIN_ROOT)}: {exc}", errors)
        return {}

    if not isinstance(value, dict):
        fail(f"expected a JSON object in {path.relative_to(PLUGIN_ROOT)}", errors)
        return {}
    return value


def parse_frontmatter(text: str, path: Path, errors: list[str]) -> dict[str, str]:
    if not text.startswith("---\n"):
        fail(f"{path.relative_to(PLUGIN_ROOT)} must start with YAML front matter", errors)
        return {}

    parts = text.split("---", 2)
    if len(parts) != 3:
        fail(f"{path.relative_to(PLUGIN_ROOT)} has unterminated YAML front matter", errors)
        return {}

    metadata: dict[str, str] = {}
    for raw_line in parts[1].strip().splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if ":" not in raw_line:
            fail(
                f"unsupported front matter line in {path.relative_to(PLUGIN_ROOT)}: {raw_line!r}",
                errors,
            )
            continue
        key, value = raw_line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"').strip("'")
    return metadata


def validate_manifest(errors: list[str]) -> None:
    manifest_path = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
    manifest = load_json(manifest_path, errors)
    if not manifest:
        return

    for key in ["name", "version", "description", "skills"]:
        if not manifest.get(key):
            fail(f"plugin manifest is missing {key!r}", errors)

    if manifest.get("name") != "software-design-philosophy":
        fail("plugin name must be software-design-philosophy", errors)

    version = str(manifest.get("version", ""))
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        fail(f"plugin version is not simple semver: {version!r}", errors)

    for key in ["homepage", "repository"]:
        if manifest.get(key) != REPOSITORY_URL:
            fail(f"plugin {key} must be {REPOSITORY_URL}", errors)

    skills_path = manifest.get("skills")
    if not isinstance(skills_path, str) or not skills_path.startswith("./"):
        fail("plugin skills path must be a ./-relative string", errors)
    elif not (PLUGIN_ROOT / skills_path).is_dir():
        fail(f"plugin skills directory does not exist: {skills_path}", errors)

    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        fail("plugin manifest must include an interface object", errors)
    else:
        for key in ["displayName", "shortDescription", "longDescription", "defaultPrompt"]:
            if not interface.get(key):
                fail(f"plugin interface is missing {key!r}", errors)
        prompts = interface.get("defaultPrompt")
        if not isinstance(prompts, list) or not all(isinstance(item, str) and item for item in prompts):
            fail("plugin interface.defaultPrompt must be a non-empty string array", errors)


def validate_marketplace(errors: list[str]) -> None:
    marketplace_path = PLUGIN_ROOT / ".agents" / "plugins" / "marketplace.json"
    marketplace = load_json(marketplace_path, errors)
    if not marketplace:
        return

    if marketplace.get("name") != "software-design-philosophy-skill":
        fail("marketplace name must be software-design-philosophy-skill", errors)

    interface = marketplace.get("interface")
    if not isinstance(interface, dict) or not interface.get("displayName"):
        fail("marketplace must include interface.displayName", errors)

    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list):
        fail("marketplace plugins must be a list", errors)
        return

    matching = [
        item
        for item in plugins
        if isinstance(item, dict) and item.get("name") == "software-design-philosophy"
    ]
    if len(matching) != 1:
        fail("marketplace must contain exactly one software-design-philosophy entry", errors)
        return

    entry = matching[0]
    source = entry.get("source")
    if not isinstance(source, dict):
        fail("marketplace plugin source must be an object", errors)
    elif source.get("source") != "local" or source.get("path") != "./":
        fail("marketplace source must point at the repository root with local path ./", errors)

    policy = entry.get("policy")
    if not isinstance(policy, dict):
        fail("marketplace plugin must include a policy object", errors)
    else:
        if policy.get("installation") != "AVAILABLE":
            fail("marketplace policy.installation must be AVAILABLE", errors)
        if policy.get("authentication") != "ON_INSTALL":
            fail("marketplace policy.authentication must be ON_INSTALL", errors)

    if not entry.get("category"):
        fail("marketplace plugin must include a category", errors)


def validate_skill(errors: list[str]) -> None:
    skill_path = SKILL_ROOT / "SKILL.md"
    try:
        text = skill_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        fail(f"missing skill manifest: {skill_path.relative_to(PLUGIN_ROOT)}", errors)
        return

    metadata = parse_frontmatter(text, skill_path, errors)
    if metadata.get("name") != "software-design-philosophy":
        fail("SKILL.md name must be software-design-philosophy", errors)

    description = metadata.get("description", "")
    if len(description) < 80:
        fail("SKILL.md description is too short to trigger reliably", errors)
    if len(description) > 600:
        fail("SKILL.md description is too long for efficient discovery", errors)

    for heading in [
        "# Software Design Philosophy",
        "## Core objective",
        "## Workflow",
        "## Output contract",
    ]:
        if heading not in text:
            fail(f"SKILL.md is missing required heading: {heading}", errors)

    for resource in EXPECTED_RESOURCES:
        if not resource.is_file():
            fail(f"missing supporting resource: {resource.relative_to(PLUGIN_ROOT)}", errors)

    metadata_path = SKILL_ROOT / "agents" / "openai.yaml"
    try:
        metadata_text = metadata_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        fail(f"missing skill UI metadata: {metadata_path.relative_to(PLUGIN_ROOT)}", errors)
    else:
        for token in [
            "display_name:",
            "short_description:",
            "default_prompt:",
            "allow_implicit_invocation:",
        ]:
            if token not in metadata_text:
                fail(f"openai.yaml is missing {token}", errors)


def validate_evals(errors: list[str]) -> None:
    prompts_path = PLUGIN_ROOT / "evals" / "prompts.csv"
    try:
        with prompts_path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            fieldnames = set(reader.fieldnames or [])
    except FileNotFoundError:
        fail(f"missing eval prompt set: {prompts_path.relative_to(PLUGIN_ROOT)}", errors)
        return

    required_fields = {"id", "should_trigger", "prompt"}
    if fieldnames != required_fields:
        fail(
            f"eval CSV fields must be exactly {sorted(required_fields)}, got {sorted(fieldnames)}",
            errors,
        )
    if not rows:
        fail("eval prompt set is empty", errors)
        return

    ids: set[str] = set()
    positive = 0
    negative = 0
    for index, row in enumerate(rows, start=2):
        case_id = (row.get("id") or "").strip()
        if not case_id:
            fail(f"eval row {index} has no id", errors)
        elif case_id in ids:
            fail(f"duplicate eval id: {case_id}", errors)
        ids.add(case_id)

        trigger = (row.get("should_trigger") or "").strip().lower()
        if trigger == "true":
            positive += 1
        elif trigger == "false":
            negative += 1
        else:
            fail(f"eval row {index} has invalid should_trigger value: {trigger!r}", errors)

        if not (row.get("prompt") or "").strip():
            fail(f"eval row {index} has an empty prompt", errors)

    if positive < 8:
        fail(f"expected at least 8 positive trigger cases, found {positive}", errors)
    if negative < 4:
        fail(f"expected at least 4 negative trigger cases, found {negative}", errors)

    if not (PLUGIN_ROOT / "evals" / "rubric.md").is_file():
        fail("missing eval behavior rubric", errors)


def main() -> int:
    errors: list[str] = []
    validate_manifest(errors)
    validate_marketplace(errors)
    validate_skill(errors)
    validate_evals(errors)

    if errors:
        print("validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("software-design-philosophy plugin validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
