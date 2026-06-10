# Microservice Investigation Playbook

**Version**: 1.1.0 — see [CHANGELOG](CHANGELOG.md). Filled artifacts record this version in their `playbook_version` front-matter field.

## Purpose

This playbook defines a structured, repeatable process for investigating a brownfield or legacy microservice. It is designed for execution by an AI coding agent, with human oversight at defined checkpoints.

The goal is to produce a complete set of artifacts that capture the service's business logic, domain vocabulary, architecture, dependencies, contracts, data model, deployment topology, observability posture, and operational risks — all backed by evidence from the codebase and its surrounding infrastructure.

## Prerequisites

Before starting, the operator MUST provide:

| Prerequisite | Description |
|---|---|
| **Repository access** | Local clone or path to the service repository |
| **Service name** | The canonical name used in deployment, logging, and inter-service communication |
| **Output directory** | Path where filled artifacts will be written |
| **Scope constraints** | Any areas explicitly in/out of scope (e.g. "ignore the legacy v1 API") |

The operator SHOULD also provide (if available):

- Links to existing documentation, wikis, or architecture diagrams
- Access to CI/CD pipeline definitions (if outside the repo)
- Access to infrastructure-as-code repositories (if separate)
- Names of known upstream/downstream services
- Links to monitoring dashboards, runbooks, or on-call rosters

## Phases

The investigation proceeds in eleven phases. Each phase produces one or more artifacts.

### Phase 1: Initial Reconnaissance

- **Goal**: Establish a first-pass understanding of what the service is, what it does, and how the repository is organized.
- **Inputs**: Repository path, service name, any provided documentation links.
- **Outputs**: `system-overview.md` (partial), `codebase-structure.md` (partial).
- **Verification**: Run self-check against completeness policy minimum-viable tier for both templates.
- **Prompt**: `prompts/01-initial-reconnaissance.md`

### Phase 2: Codebase Analysis

- **Goal**: Map the architecture, identify patterns, layering, and key abstractions.
- **Inputs**: Phase 1 artifacts, repository access.
- **Outputs**: `codebase-structure.md` (complete).
- **Verification**: Cross-reference directory layout claims with actual file tree; verify entrypoints by tracing from build/start config.
- **Prompt**: `prompts/02-codebase-analysis.md`

### Phase 3: Business Logic Analysis

- **Goal**: Understand and document use cases, business rules, state machines, algorithms, and domain events.
- **Inputs**: Phase 1-2 artifacts, repository access.
- **Outputs**: `business-logic.md` (complete).
- **Verification**: Trace at least one use case end-to-end from entrypoint through business logic to side effects; verify state machines by finding state fields and transition code.
- **Prompt**: `prompts/03-business-logic-analysis.md`

### Phase 4: Glossary Construction

- **Goal**: Build a domain vocabulary mapping business concepts to code-level names and identifying non-obvious terminology.
- **Inputs**: Phase 1-3 artifacts, repository access.
- **Outputs**: `glossary.md` (complete).
- **Verification**: Verify every glossary term appears in the codebase; verify abbreviation expansions against comments or documentation.
- **Prompt**: `prompts/04-glossary-construction.md`

### Phase 5: Dependency Mapping

- **Goal**: Inventory all internal and external dependencies — libraries, services, infrastructure, external APIs.
- **Inputs**: Phase 2 artifacts, dependency manifests, import analysis.
- **Outputs**: `dependency-inventory.md` (complete).
- **Verification**: Compare manifest-declared deps against actually-imported deps; flag discrepancies.
- **Prompt**: `prompts/05-dependency-mapping.md`

### Phase 6: API Surface Analysis

- **Goal**: Document all interfaces the service exposes and consumes.
- **Inputs**: Phase 2-5 artifacts, route/controller definitions, schema files, event declarations.
- **Outputs**: `api-surface.md` (complete).
- **Verification**: Trace at least one endpoint end-to-end from route definition to handler to response.
- **Prompt**: `prompts/06-api-surface-analysis.md`

### Phase 7: Data Model Analysis

- **Goal**: Map all data stores, schemas, migrations, and data flows.
- **Inputs**: Phase 2-5 artifacts, ORM models, migration files, connection configs.
- **Outputs**: `data-model.md` (complete).
- **Verification**: Cross-reference ORM/model definitions against migration history; verify store connection strings in config.
- **Prompt**: `prompts/07-data-model-analysis.md`

### Phase 8: Deployment Analysis

- **Goal**: Understand how the service is built, deployed, and run across environments.
- **Inputs**: Phase 2-5 artifacts, CI/CD configs, Dockerfiles, IaC, Helm charts, environment configs.
- **Outputs**: `deployment-and-infra.md` (complete).
- **Verification**: Trace the deployment pipeline from commit to production; verify environment variable references exist in code.
- **Prompt**: `prompts/08-deployment-analysis.md`

### Phase 9: Observability Analysis

- **Goal**: Assess logging, metrics, tracing, and alerting posture.
- **Inputs**: Phase 2-5 artifacts, logging config, metrics instrumentation, alert definitions.
- **Outputs**: `observability.md` (complete).
- **Verification**: Trace at least one log statement from code to configured output destination; verify metric names match any dashboard references.
- **Prompt**: `prompts/09-observability-analysis.md`

### Phase 10: Risk Assessment

- **Goal**: Identify and classify technical risks, debt, and operational hazards.
- **Inputs**: All Phase 1-9 artifacts.
- **Outputs**: `risk-register.md` (complete).
- **Verification**: Every risk entry must cite evidence from a prior artifact; severity ratings must follow the defined rubric.
- **Prompt**: `prompts/10-risk-assessment.md`

### Phase 11: Synthesis and Report

- **Goal**: Compile all artifacts into a coherent final report, fill the operational runbook, and produce an executive summary.
- **Inputs**: All completed artifacts.
- **Outputs**: `runbook.md` (complete), `system-overview.md` (finalized), executive summary section.
- **Verification**: All templates pass completeness policy standard tier; all `[unknown]` and `[conflict]` tags are listed in a summary section.
- **Prompt**: `prompts/11-synthesis-and-report.md`

## Execution Model

```
Phase 1 ──► Phase 2 ──┬──► Phase 3 ──► Phase 4 ─────────┐
                      └──► Phase 5 ──┬──► Phase 6 ──┐   │
                                     ├──► Phase 7 ──┤   ▼
                                     ├──► Phase 8 ──┼──► Phase 10 ──► Phase 11
                                     └──► Phase 9 ──┘
```

- **Phases 1-2** are strictly sequential. Each builds on the prior phase's output.
- After Phase 2, two branches MAY run in parallel:
  - **Domain branch**: Phase 3, then Phase 4 (the glossary harvests terms from `business-logic.md`, so Phase 4 depends on Phase 3).
  - **Dependency branch**: Phase 5, then Phases 6-9.
- **Phases 6-9** MAY run in parallel. They depend on Phase 5 but not on each other.
- **Phase 10** depends on all of Phases 4 and 6-9 (it reads every prior artifact).
- **Phase 11** depends on Phase 10 and all prior artifacts.

When delegating to multiple agents in parallel (Phase 3 alongside Phase 5, or Phases 6-9), the operator MUST provide each agent with the completed prior artifacts listed in that phase's prompt.

## Subagent Execution Model

To avoid context overflow, each phase SHOULD be executed by a separate subagent with a clean context window. A parent orchestrator manages phase ordering and passes artifacts between phases.

### Per-Phase Context

Each subagent receives only what it needs:

| Phase | Context Provided |
|---|---|
| 1: Reconnaissance | Prompt + policies + repository access |
| 2: Codebase Analysis | Prompt + policies + Phase 1 artifacts |
| 3: Business Logic | Prompt + policies + `system-overview.md` + `codebase-structure.md` |
| 4: Glossary | Prompt + policies + `system-overview.md` + `codebase-structure.md` + `business-logic.md` |
| 5: Dependencies | Prompt + policies + `codebase-structure.md` |
| 6: API Surface | Prompt + policies + `codebase-structure.md` + `dependency-inventory.md` |
| 7: Data Model | Prompt + policies + `codebase-structure.md` + `dependency-inventory.md` |
| 8: Deployment | Prompt + policies + `codebase-structure.md` + `dependency-inventory.md` |
| 9: Observability | Prompt + policies + `codebase-structure.md` + `dependency-inventory.md` |
| 10: Risk Assessment | Prompt + policies + all prior artifacts (REQUIRED sections first; see gathering policy Context Budget) |
| 11: Synthesis | Prompt + policies + all prior artifacts (same context budget rules) |

### Orchestrator Responsibilities

The orchestrator (parent agent or human operator):

1. Collects investigation parameters from the user.
2. Copies blank templates to the output directory's `artifacts/` subfolder.
3. Launches each phase as a subagent with the prompt, policies, and required prior artifacts inlined.
4. After each phase, reads the subagent's output artifacts and checks for escalation items.
5. Reports phase results to the user before proceeding.
6. For Phases 10-11 (which need all artifacts), applies the Context Budget rules from the gathering policy: include `[REQUIRED]` sections from all artifacts, `[STANDARD]` sections only for directly relevant artifacts.

### Benefits

- Each subagent gets a focused context window (~10-30K tokens) instead of accumulating the full investigation (~100K+ tokens).
- Parallel branches (3→4 alongside 5, then 6+7+8+9) can run as truly concurrent subagents.
- A failed or incomplete phase can be re-run without restarting the entire investigation.
- The orchestrator maintains a lightweight view of progress without carrying investigation details.

## Escalation Rules

The agent MUST stop and request human input when:

| Trigger | Action |
|---|---|
| Repository access fails or is incomplete | Report what is missing; do not guess |
| Credentials, tokens, or secrets are required | Request from operator; never fabricate or extract from config |
| A destructive or mutating action would be needed | Describe the action; wait for explicit approval |
| Contradictory evidence is found that cannot be resolved from code alone | Record both versions with `[conflict]` tag; ask operator to clarify |
| Critical information is entirely absent (no build system, no entrypoint, no deploy config) | Record as `[unknown]`; flag to operator with impact assessment |
| Investigation would require accessing production systems or live data | Describe what is needed; wait for operator to provide or approve |

## Artifact Management

- All filled templates are written to the operator-provided output directory under an `artifacts/` subfolder (e.g. `{{OUTPUT_DIR}}/artifacts/system-overview.md`). The blank templates in this playbook's `templates/` folder are never modified.
- Each artifact MUST retain its YAML front-matter with updated metadata (investigator, date, confidence summary).
- The agent MUST NOT delete or overwrite prior phase outputs. If corrections are needed, the agent appends an `## Amendments` section.
- At the end of each phase, the agent reports: which artifacts were updated, completeness tier achieved, and any `[unknown]`/`[conflict]` items.

## References

- [Completeness Policy](policies/completeness-policy.md)
- [Gathering Policy](policies/gathering-policy.md)
- [Verification Policy](policies/verification-policy.md)
- [Templates](templates/)
- [Prompts](prompts/)
- [Examples](examples/) — golden filled artifacts showing expected granularity, citations, and tags
- [CHANGELOG](CHANGELOG.md)
