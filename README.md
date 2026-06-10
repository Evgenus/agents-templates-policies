# Templates and Policies

Structured playbooks for AI-agent-driven engineering processes, with the templates and policies they rely on.

## Contents

| Path | Purpose |
|---|---|
| `playbooks/microservice-investigation/` | An 11-phase playbook for investigating a brownfield/legacy microservice and producing evidence-backed artifacts (system overview, business logic, glossary, dependencies, API surface, data model, deployment, observability, risks, runbook) |
| `.cursor/rules/microservice-investigation.mdc` | Cursor rule that turns the agent into an orchestrator for the playbook, delegating each phase to a subagent |
| `scripts/lint-playbook.py` | Consistency lint: phase numbers, template/policy alignment, prompt variables |

## Playbook layout

Each playbook follows the same structure:

- `PLAYBOOK.md` — the process: phases, execution model (DAG with parallel branches), subagent context map, escalation rules. The single source of truth for orchestration.
- `prompts/` — one self-contained prompt per phase, with `{{VARIABLES}}` filled in by the orchestrator.
- `policies/` — cross-cutting rules inlined into every subagent prompt: how to gather evidence, what "complete" means, how to verify claims.
- `templates/` — blank artifact templates with YAML front-matter, completeness tiers (`[REQUIRED]`/`[STANDARD]`/`[EXTENDED]`), and instructions per section. Filled copies are written to the investigation's output directory under `artifacts/`.
- `examples/` — golden filled artifacts showing the expected granularity, citation style, and confidence tags.
- `CHANGELOG.md` — playbook versions. Filled artifacts record the producing version in `playbook_version` front-matter.

## Usage

In Cursor, run the slash command:

```
/investigate /path/to/repo [service-name] [output-dir]
```

Or just ask the agent to investigate a microservice (e.g. "Investigate the service at /path/to/repo"). Either way, the `microservice-investigation` rule activates, collects parameters (repository path, service name, output directory, optional doc links and scope constraints), and runs the 11 phases via subagents, reporting after each.

## Validation

Run the consistency lint before committing playbook changes:

```bash
python3 scripts/lint-playbook.py
```

It verifies that template `phase:` front-matter matches the PLAYBOOK's per-phase outputs, prompts use only known variables and current paths, every template has a per-artifact section in the completeness policy, and front-matter carries the required fields.
