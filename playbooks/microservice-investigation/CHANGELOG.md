# Changelog

All notable changes to the Microservice Investigation Playbook. Filled artifacts record the version that produced them in their `playbook_version` front-matter field.

## 1.1.0 — 2026-06-11

### Fixed
- Corrected stale `phase:` front-matter values in 8 templates left over from the 9-phase → 11-phase expansion (e.g. `risk-register.md` claimed phase 8, actual phase is 10; `dependency-inventory.md` and `business-logic.md` both claimed phase 3).
- Fixed stale phase cross-references in the Phase 1 prompt (CI/CD analysis is Phase 8, not 6; dependency/API analysis is Phases 5-6, not 4-5).
- Resolved the Phase 5 input contradiction: the playbook claimed Phase 5 depends on Phases 3-4 while the prompt only used Phase 2 artifacts. Phase 5 now depends only on Phase 2 and runs in parallel with the domain branch.
- Resolved the Phase 3/4 parallelism contradiction: the playbook claimed Phases 3-4 are independent while the Phase 4 prompt requires `business-logic.md`. Phase 4 now explicitly depends on Phase 3.
- Fixed prompt 11 pointer to a nonexistent "local database setup" section in data-model.md.

### Changed
- Execution model reworked into two parallel branches after Phase 2: domain (3 → 4) and dependency (5 → 6+7+8+9).
- Filled artifacts are now written to `{{OUTPUT_DIR}}/artifacts/` instead of `{{OUTPUT_DIR}}/templates/`.
- Phase 9 no longer reads Phase 8 output (they run in parallel); probe-vs-health-endpoint reconciliation moved to the Phase 11 consistency check.
- The orchestrator rule now defers to PLAYBOOK.md for the execution model and per-phase context map instead of duplicating them; the severity rubric lives only in the risk-register template.
- All phase prompts (not just Phase 1) now receive `{{DOC_LINKS}}` and `{{SCOPE_CONSTRAINTS}}`.

### Added
- `[not-applicable]` confidence tag for confirmed absences, distinct from `[unknown]`.
- Clarification that `[stale-source]` is an annotation supplementing a confidence tag, not a tag itself.
- Artifact-level `completeness_tier` semantics (`minimum-viable` / `standard` / `extended`).
- Interface Inventory section (`[REQUIRED]`) in codebase-structure.md, produced in Phase 2, mapped to use cases in Phase 3, deepened in Phase 6.
- Per-artifact completeness tables synced with actual template sections (Impact, Relationships, Caching, CLI commands, Orchestration, Networking, On-call, Emergency contacts, etc.).
- `playbook_version` front-matter field and `not_applicable` confidence-summary counter in all templates.
- Consistency lint script (`scripts/lint-playbook.py`) and CI workflow.
- Golden example artifact in `examples/`.

## 1.0.0

- Initial 11-phase playbook: prompts, policies (gathering, completeness, verification), templates, and orchestrator rule.
