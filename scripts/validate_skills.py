#!/usr/bin/env python3
"""Validate SKILL.md files across the slimstack repository.

Each top-level directory containing a SKILL.md is treated as a skill.
The frontmatter must be a YAML mapping with non-empty `name` and
`description` fields. The `name` must match the folder name (the root
SKILL.md is exempt because it is the router).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
REQUIRED_FIELDS = ("name", "description")
SKIP_DIRS = {".git", ".github", "node_modules", "references", "scripts"}


def parse_frontmatter(text: str):
    if not text.startswith("---\n"):
        return None, "missing leading '---' frontmatter delimiter"
    end = text.find("\n---", 4)
    if end == -1:
        return None, "missing closing '---' frontmatter delimiter"
    raw = text[4:end]
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        return None, f"YAML parse error: {exc}"
    if not isinstance(data, dict):
        return None, "frontmatter is not a YAML mapping"
    return data, None


def validate(skill_md: Path, expected_name: str | None) -> list[str]:
    rel = skill_md.relative_to(REPO_ROOT)
    errors: list[str] = []
    text = skill_md.read_text(encoding="utf-8")
    fm, err = parse_frontmatter(text)
    if err:
        return [f"{rel}: {err}"]
    for field in REQUIRED_FIELDS:
        value = fm.get(field)
        if value is None or (isinstance(value, str) and not value.strip()):
            errors.append(f"{rel}: missing or empty field '{field}'")
    name = fm.get("name")
    if expected_name and isinstance(name, str) and name != expected_name:
        errors.append(
            f"{rel}: name '{name}' does not match folder '{expected_name}'"
        )
    return errors


def check_router_consistency() -> list[str]:
    errors: list[str] = []
    root_skill = REPO_ROOT / "SKILL.md"
    if not root_skill.exists():
        return errors

    text = root_skill.read_text(encoding="utf-8")

    section_match = re.search(r"## 路由規則\n(.*?)(?=\n## |\Z)", text, re.DOTALL)
    if not section_match:
        return errors

    router_section = section_match.group(1)
    ref_pattern = re.compile(r"`(\w[\w-]*)\/SKILL\.md`")
    router_dirs = set(ref_pattern.findall(router_section))

    # Forward check: each referenced dir must exist with SKILL.md
    for dir_name in sorted(router_dirs):
        skill_path = REPO_ROOT / dir_name / "SKILL.md"
        if not skill_path.exists():
            errors.append(
                f"router references '{dir_name}/SKILL.md' but directory does not exist"
            )

    # Reverse check: each sub-dir with SKILL.md must appear in router table
    for child in sorted(REPO_ROOT.iterdir()):
        if not child.is_dir() or child.name in SKIP_DIRS or child.name.startswith("."):
            continue
        if (child / "SKILL.md").exists() and child.name not in router_dirs:
            errors.append(
                f"directory '{child.name}' has SKILL.md but is not in router table"
            )

    return errors


def main() -> int:
    all_errors: list[str] = []
    checked = 0

    root_skill = REPO_ROOT / "SKILL.md"
    if root_skill.exists():
        all_errors.extend(validate(root_skill, expected_name=None))
        checked += 1

    for child in sorted(REPO_ROOT.iterdir()):
        if not child.is_dir() or child.name in SKIP_DIRS or child.name.startswith("."):
            continue
        skill_md = child / "SKILL.md"
        if not skill_md.exists():
            all_errors.append(f"{child.name}/: missing SKILL.md")
            continue
        all_errors.extend(validate(skill_md, expected_name=child.name))
        checked += 1

    all_errors.extend(check_router_consistency())

    if all_errors:
        print(f"Validated {checked} skill(s); found {len(all_errors)} issue(s):")
        for line in all_errors:
            print(f"  - {line}")
        return 1
    print(f"All {checked} skill(s) passed validation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
