#!/usr/bin/env python3
"""Consistency lint for the microservice-investigation playbook.

Checks the invariants that are easy to break when editing the playbook,
prompts, policies, and templates independently:

1. Template `phase:` front-matter matches the phases that list the artifact
   in their **Outputs** line in PLAYBOOK.md.
2. Template front-matter carries `playbook_version` (matching PLAYBOOK.md and
   the latest CHANGELOG entry) and the full `confidence_summary` key set.
3. Templates use only known tier markers and contain an Amendments section.
4. Prompts use only known {{VARIABLES}}, contain the full context variable
   set, and reference the `artifacts/` output folder (not `templates/`).
5. The completeness policy has a per-artifact section for every template.
6. The orchestrator rule defers to PLAYBOOK.md.

Exit code 0 = clean, 1 = violations found.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PB_DIR = ROOT / "playbooks" / "microservice-investigation"
PLAYBOOK = PB_DIR / "PLAYBOOK.md"
CHANGELOG = PB_DIR / "CHANGELOG.md"
TEMPLATES = PB_DIR / "templates"
PROMPTS = PB_DIR / "prompts"
POLICIES = PB_DIR / "policies"
RULE = ROOT / ".cursor" / "rules" / "microservice-investigation.mdc"

KNOWN_VARIABLES = {"REPO_PATH", "SERVICE_NAME", "OUTPUT_DIR", "DOC_LINKS", "SCOPE_CONSTRAINTS"}
TIER_MARKERS = {"REQUIRED", "STANDARD", "EXTENDED"}
CONFIDENCE_KEYS = ["verified", "inferred", "uncertain", "unknown", "not_applicable", "conflict"]

errors: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def parse_front_matter(text: str, path: Path) -> str:
    m = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    if not m:
        err(f"{rel(path)}: missing YAML front-matter")
        return ""
    return m.group(1)


def check_playbook_outputs() -> dict[str, set[int]]:
    """artifact filename -> set of phase numbers whose Outputs line lists it."""
    text = PLAYBOOK.read_text()
    outputs: dict[str, set[int]] = {}
    for m in re.finditer(r"### Phase (\d+):.*?\n(.*?)(?=\n### Phase |\n## )", text, re.S):
        num = int(m.group(1))
        om = re.search(r"\*\*Outputs\*\*: (.+)", m.group(2))
        if not om:
            err(f"{rel(PLAYBOOK)}: Phase {num} has no **Outputs** line")
            continue
        for art in re.findall(r"`([a-z0-9-]+\.md)`", om.group(1)):
            outputs.setdefault(art, set()).add(num)
    if not outputs:
        err(f"{rel(PLAYBOOK)}: could not parse any phase Outputs lines")
    return outputs


def get_playbook_version() -> str:
    m = re.search(r"\*\*Version\*\*: (\d+\.\d+\.\d+)", PLAYBOOK.read_text())
    if not m:
        err(f"{rel(PLAYBOOK)}: missing '**Version**: X.Y.Z' line")
        return ""
    return m.group(1)


def get_changelog_version() -> str:
    m = re.search(r"^## (\d+\.\d+\.\d+)", CHANGELOG.read_text(), re.M)
    if not m:
        err(f"{rel(CHANGELOG)}: no '## X.Y.Z' version heading found")
        return ""
    return m.group(1)


def check_templates(outputs: dict[str, set[int]], version: str) -> None:
    template_files = sorted(TEMPLATES.glob("*.md"))
    if not template_files:
        err(f"{rel(TEMPLATES)}: no templates found")

    for path in template_files:
        text = path.read_text()
        fm = parse_front_matter(text, path)
        if not fm:
            continue

        vm = re.search(r'playbook_version: "([^"]*)"', fm)
        if not vm:
            err(f"{rel(path)}: front-matter missing playbook_version")
        elif version and vm.group(1) != version:
            err(f"{rel(path)}: playbook_version {vm.group(1)!r} != PLAYBOOK version {version!r}")

        pm = re.search(r'phase: "([^"]*)"', fm)
        if not pm:
            err(f"{rel(path)}: front-matter missing phase")
        else:
            declared = {int(p) for p in re.findall(r"\d+", pm.group(1))}
            expected = outputs.get(path.name)
            if expected is None:
                err(f"{rel(path)}: not listed in any phase Outputs line in PLAYBOOK.md")
            elif declared != expected:
                err(
                    f"{rel(path)}: phase front-matter {sorted(declared)} != "
                    f"PLAYBOOK outputs {sorted(expected)}"
                )

        for key in CONFIDENCE_KEYS:
            if not re.search(rf"^  {key}: \d+$", fm, re.M):
                err(f"{rel(path)}: confidence_summary missing key '{key}'")

        for marker in re.findall(r"`\[([A-Z][A-Z-]+)\]`", text):
            if marker not in TIER_MARKERS:
                err(f"{rel(path)}: unknown tier marker `[{marker}]`")

        if "## Amendments" not in text:
            err(f"{rel(path)}: missing '## Amendments' section")


def check_prompts() -> None:
    prompt_files = sorted(PROMPTS.glob("*.md"))
    if len(prompt_files) != 11:
        err(f"{rel(PROMPTS)}: expected 11 prompts, found {len(prompt_files)}")

    for path in prompt_files:
        text = path.read_text()

        for var in set(re.findall(r"\{\{([A-Z_]+)\}\}", text)):
            if var not in KNOWN_VARIABLES:
                err(f"{rel(path)}: unknown template variable {{{{{var}}}}}")

        for var in KNOWN_VARIABLES:
            if f"{{{{{var}}}}}" not in text:
                err(f"{rel(path)}: missing context variable {{{{{var}}}}}")

        if "{{OUTPUT_DIR}}/templates/" in text:
            err(f"{rel(path)}: stale output path '{{{{OUTPUT_DIR}}}}/templates/' (use artifacts/)")


def check_completeness_policy() -> None:
    policy = POLICIES / "completeness-policy.md"
    text = policy.read_text()
    for path in sorted(TEMPLATES.glob("*.md")):
        if f"### {path.name}" not in text:
            err(f"{rel(policy)}: missing per-artifact section for {path.name}")


def check_rule() -> None:
    if not RULE.exists():
        err(f"{rel(RULE)}: orchestrator rule not found")
        return
    text = RULE.read_text()
    if "PLAYBOOK.md" not in text:
        err(f"{rel(RULE)}: rule does not reference PLAYBOOK.md")
    if "/templates/`" in text.replace("playbooks/microservice-investigation/templates/", ""):
        err(f"{rel(RULE)}: rule references a stale output templates/ folder")


def main() -> int:
    outputs = check_playbook_outputs()
    pb_version = get_playbook_version()
    cl_version = get_changelog_version()
    if pb_version and cl_version and pb_version != cl_version:
        err(f"PLAYBOOK version {pb_version} != latest CHANGELOG version {cl_version}")

    check_templates(outputs, pb_version)
    check_prompts()
    check_completeness_policy()
    check_rule()

    if errors:
        print(f"FAIL: {len(errors)} violation(s)\n")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("OK: playbook is internally consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
