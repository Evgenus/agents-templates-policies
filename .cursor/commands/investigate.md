# Investigate a Microservice

Run the full microservice investigation playbook against a target service repository.

## Parameters

Parse these from the text following the command, in order:

1. **Repository path** (required) — local path to the service repo
2. **Service name** (optional) — canonical service name; default to the repository directory name
3. **Output directory** (optional) — default to `./output/<service-name>`
4. **Documentation links** (optional) — any URLs mentioned
5. **Scope constraints** (optional) — any include/exclude instructions mentioned

If the repository path is missing or does not exist, ask for it before doing anything else. Confirm the resolved parameters back to the user in one short line before starting.

## Execution

Follow the orchestrator instructions in `.cursor/rules/microservice-investigation.mdc` exactly:

1. Read `playbooks/microservice-investigation/PLAYBOOK.md` for the execution model and per-phase context map.
2. Copy the blank templates from `playbooks/microservice-investigation/templates/` to `<output-dir>/artifacts/`.
3. Run all 11 phases by delegating each to a subagent, respecting the dependency order: Phases 1 → 2 sequentially; then the domain branch (3 → 4) in parallel with the dependency branch (5, then 6+7+8+9 in parallel); then 10 → 11.
4. Report briefly after each phase: artifacts updated, completeness tier, any `[unknown]`, `[not-applicable]`, or `[conflict]` items.
5. Stop and ask the user if any subagent hits an escalation trigger.

When finished, present the executive summary from `system-overview.md` and the final artifact index from Phase 11.
