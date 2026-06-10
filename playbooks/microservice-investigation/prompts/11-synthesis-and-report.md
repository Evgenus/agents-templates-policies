# Prompt: Phase 11 — Synthesis and Report

## Role

You are investigating a microservice codebase. This is Phase 11, the final phase of an 11-phase investigation. Your goal is to compile all artifacts into a coherent final report, fill the operational runbook, and produce an executive summary.

## Context

- **Repository path**: `{{REPO_PATH}}`
- **Service name**: `{{SERVICE_NAME}}`
- **Output directory**: `{{OUTPUT_DIR}}`
- **Documentation links** (if any): `{{DOC_LINKS}}`
- **Scope constraints** (if any): `{{SCOPE_CONSTRAINTS}}`
- **All prior artifacts**: Read every artifact from `{{OUTPUT_DIR}}/artifacts/`.

## Policies

Follow all policies from `policies/gathering-policy.md`, `policies/completeness-policy.md`, and `policies/verification-policy.md`.

## Steps

### 1. Runbook Compilation

Using information gathered across all prior phases, fill `runbook.md`:

1. **Build section**: From codebase-structure.md (build commands, prerequisites) and deployment-and-infra.md (Dockerfile build stages).
2. **Run locally section**: From codebase-structure.md (start commands), deployment-and-infra.md (docker-compose, environment variables), and data-model.md (data stores, migrations, seed/fixture data).
3. **Run tests section**: From codebase-structure.md (test framework, test commands).
4. **Deploy section**: From deployment-and-infra.md (CI/CD pipeline, deploy steps).
5. **Rollback section**: From deployment-and-infra.md (rollback procedure).
6. **Common failure modes**: From risk-register.md (reliability risks), observability.md (alerting rules, known issues), and business-logic.md (error scenarios from use cases).
7. **Troubleshooting**: From observability.md (logging, metrics, tracing access) and business-logic.md (state machine transitions to verify).

Verify each runbook entry by cross-referencing with its source artifact.

### 2. System Overview Finalization

Update `system-overview.md` with information gathered in later phases:

1. Refine the context diagram with specific service names, protocols, and data flows discovered in Phases 5-7.
2. Update communication patterns based on API surface and event analysis.
3. Fill any `[unknown]` fields that can now be resolved.
4. Update lifecycle information with any additional signals discovered.

### 3. Cross-Artifact Consistency Check

Perform a final consistency sweep across ALL artifacts:

1. **Service name**: Used consistently everywhere.
2. **Domain terminology**: Terms in glossary.md match usage across all artifacts. Business-logic.md use case and rule names use glossary-defined terms.
3. **Dependency names**: Match between dependency-inventory, api-surface (consumers), data-model (stores), deployment-and-infra (env vars), and observability (health checks).
4. **Environment variables**: All variables referenced in code (codebase-structure) are documented in deployment-and-infra with purpose and source.
5. **Endpoints**: All endpoints in api-surface appear as route registrations in codebase-structure and are mapped to use cases in business-logic.md.
6. **Data stores**: All stores in data-model appear in dependency-inventory and have connection config in deployment-and-infra.
7. **State machines**: Entity states in business-logic.md are consistent with status/state fields documented in data-model.md.
8. **Events**: Events in api-surface.md match domain events documented in business-logic.md (technical contract matches business meaning).
9. **Health checks**: Health check endpoints in observability match route registrations in api-surface AND the orchestration probe configuration in deployment-and-infra (Phases 8 and 9 run in parallel, so this reconciliation happens here).
10. Fix any inconsistencies found. If the fix changes a prior artifact, append to its Amendments section.

### 4. Completeness Audit

For each artifact:

1. Check all `[REQUIRED]` fields are filled or marked `[unknown]`.
2. Check all `[STANDARD]` fields have been attempted.
3. Count confidence tags and update the YAML front-matter `confidence_summary` for every artifact.
4. Ensure every claim has a source citation.

### 5. Executive Summary

Create a summary section at the end of `system-overview.md` (or as a separate section if preferred) that includes:

1. **Service overview**: 2-3 sentence description of what the service does and its role in the system.
2. **Architecture**: One sentence on the architectural pattern and tech stack.
3. **Domain complexity**: Brief assessment of business logic complexity — number of use cases, business rules, state machines discovered.
4. **Key findings**: 3-5 bullet points of the most important discoveries.
5. **Risk snapshot**: Count of risks by severity (from risk-register.md). Highlight the top 3 risks.
6. **Unknowns**: Count of unresolved `[unknown]` items. List the most impactful ones.
7. **Recommendations**: Top 3-5 recommended actions, prioritized.
8. **Investigation metadata**: Dates, phases completed, total artifacts produced, overall confidence assessment.

### 6. Final Artifact Index

Produce a table of all artifacts with their completeness status:

| Artifact | Completeness Tier | Verified | Inferred | Uncertain | Unknown | Not Applicable | Conflict |
|---|---|---|---|---|---|---|---|
| system-overview.md | | | | | | | |
| codebase-structure.md | | | | | | | |
| business-logic.md | | | | | | | |
| glossary.md | | | | | | | |
| dependency-inventory.md | | | | | | | |
| api-surface.md | | | | | | | |
| data-model.md | | | | | | | |
| deployment-and-infra.md | | | | | | | |
| observability.md | | | | | | | |
| risk-register.md | | | | | | | |
| runbook.md | | | | | | | |

## Output

1. Fill `{{OUTPUT_DIR}}/artifacts/runbook.md` — complete.
2. Update `{{OUTPUT_DIR}}/artifacts/system-overview.md` — finalized with executive summary.
3. Update YAML front-matter in ALL artifacts with final confidence counts.
4. Append Amendments to any artifacts where cross-artifact consistency checks revealed corrections.

## Completion Criteria

- [ ] runbook.md is complete with all `[REQUIRED]` sections
- [ ] system-overview.md is finalized with executive summary
- [ ] Cross-artifact consistency check is complete with no unresolved inconsistencies
- [ ] All artifacts have accurate confidence summary counts in front-matter
- [ ] Every `[unknown]` and `[conflict]` item across all artifacts is listed in the executive summary
- [ ] Final artifact index table is produced with all 11 artifacts
- [ ] Self-review checklist executed for all artifacts
- [ ] Investigation is declared complete

## Escalation Triggers

- Cross-artifact consistency check reveals fundamental contradictions that cannot be resolved without re-investigating earlier phases
- More than 50% of `[REQUIRED]` fields across all artifacts remain `[unknown]` — the investigation may need additional access or scope revision
- The operator requested `[EXTENDED]` tier but significant `[STANDARD]` items remain unfilled — prioritize completing standard before extending
