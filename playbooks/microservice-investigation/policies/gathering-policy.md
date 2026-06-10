# Gathering Policy

This policy defines how the investigating agent acquires, records, and attributes information during a microservice investigation.

## Core Principles

1. **Read-only**: The agent MUST NOT modify the target repository, run mutating commands, start services, or write to any location other than the designated output directory.
2. **Evidence-backed**: Every claim MUST cite its source. Unsupported assertions are not permitted.
3. **Minimally invasive**: Prefer targeted reads over broad scans. Read symbol signatures before reading full bodies. Use search before reading entire files.
4. **Progressive depth**: Start with high-level structure, then drill into details as needed. Do not read every file in the repository.

## Source Priority

When the same information can be obtained from multiple sources, prefer higher-ranked sources:

| Priority | Source Type | Examples | Rationale |
|---|---|---|---|
| 1 | **Executable code** | Source files, entrypoints, handlers | The ground truth of behavior |
| 2 | **Configuration and IaC** | Config files, Terraform, Helm, Dockerfiles | Defines runtime environment |
| 3 | **CI/CD definitions** | GitHub Actions, Jenkinsfiles, GitLab CI | Defines build and deploy process |
| 4 | **Dependency manifests** | package.json, go.mod, requirements.txt, pom.xml | Declares explicit dependencies |
| 5 | **Schema definitions** | OpenAPI specs, protobuf, GraphQL SDL, DB migrations | Formal contracts |
| 6 | **Documentation** | README, docs/, wiki links in repo | May be stale but provides intent |
| 7 | **Commit history** | Git log, blame, tags | Temporal context, authorship |
| 8 | **Code comments and TODOs** | Inline comments, TODO/FIXME/HACK markers | Developer intent signals, often informal |
| 9 | **External documentation** | Wikis, Confluence, Notion pages linked from repo | Highest staleness risk |

When a lower-priority source contradicts a higher-priority source, the agent MUST record both with a `[conflict]` tag and note which source has higher priority.

## Evidence Citation Format

Every factual statement in an artifact MUST include a source citation in one of these formats:

```
Source: <relative-file-path>:<line-range>
Source: <relative-file-path> (file-level)
Source: git log --oneline -1 <commit-hash>
Source: <command> (output summary)
Source: <URL>
```

Multiple sources for the same claim are separated by ` | `:

```
Source: src/app.ts:15-23 | Dockerfile:1-3
```

## Sizing and Depth Control

Artifacts must be detailed enough to be useful but concise enough to be readable — by both humans and AI agents consuming them as context in later phases. The following rules govern how much detail to include.

### Artifact Size Budgets

Each artifact SHOULD stay under **300 lines** of filled content (excluding YAML front-matter and empty template sections). If an artifact exceeds this:

1. Move detailed enumerations (e.g. full endpoint lists, complete dependency tables) into a clearly marked `## Appendix` section at the end of the artifact.
2. Keep the main body as a summary with counts and the most significant items.
3. The appendix is still part of the artifact and still requires source citations and confidence tags.

These are soft limits. An artifact MAY exceed 300 lines if every line carries non-redundant, evidence-backed information. An artifact MUST NOT be padded with repetitive phrasing, boilerplate explanations, or restated template instructions.

### Enumeration Thresholds

When a category contains many items of the same kind, apply these rules:

| Item Count | Rule |
|---|---|
| 1-20 | List all items in the main body |
| 21-50 | List the 15 most significant items in the main body; move the full list to the appendix; include a count in the main body ("47 total runtime dependencies; 15 most significant listed below, full list in Appendix") |
| 51+ | List the 10 most significant items in the main body; move the full list to the appendix; add a summary by category or theme ("142 endpoints across 8 resource groups") |

"Most significant" means: highest risk, most central to business logic, most referenced by other components, or most likely to affect adoption decisions. The agent MUST state the selection criteria used.

### Depth Rules by Completeness Tier

The completeness tier (defined in the completeness policy) determines not only *whether* a field is filled but *how deeply*:

| Tier | Depth Guidance |
|---|---|
| `[REQUIRED]` | **Concise and structured.** Use tables, short numbered lists, or 1-3 sentences per item. Enough to answer "what is this?" and "where is it?" — not "explain everything about it." |
| `[STANDARD]` | **Moderate detail.** Up to a paragraph per item, or a detailed table with multiple columns. Enough to understand behavior and make decisions without reading the source code. |
| `[EXTENDED]` | **Full depth as needed.** Detailed analysis, multi-step explanations, edge case enumeration. No arbitrary limit, but every sentence must add non-redundant information. |

These depth rules work alongside — not instead of — the completeness policy's requirement that `[REQUIRED]` fields be filled and `[STANDARD]` fields be attempted. A concise `[REQUIRED]` entry is complete; a verbose one with padding is not "more complete."

### Cross-Reference Over Duplication

When the same information is relevant to multiple artifacts:

1. The **canonical location** is the artifact whose phase produced the information. For example, events are canonically documented in `api-surface.md` (technical contract) and `business-logic.md` (business meaning).
2. Other artifacts that reference this information SHOULD use a cross-reference rather than reproducing the content: `See api-surface.md § Event / Message Contracts` or `See business-logic.md § UC-003`.
3. An artifact MAY include a brief one-line summary alongside the cross-reference for context, but MUST NOT duplicate full tables or multi-line descriptions.
4. The only exception is `runbook.md`, which SHOULD be self-contained for operational use and MAY reproduce essential commands and steps from other artifacts.

### Context Budget for Multi-Phase Reads

When a phase requires reading prior artifacts as input (e.g. Phase 10 reads all nine prior artifacts):

1. Read YAML front-matter and `[REQUIRED]` sections first for every artifact.
2. Read `[STANDARD]` sections only for artifacts directly relevant to the current phase's task.
3. Read `[EXTENDED]` sections and appendices only when a specific question arises during the phase.
4. If the combined prior artifacts exceed the agent's effective context, prioritize by phase dependency: artifacts from immediately preceding phases first, then earlier phases.

## Gathering Strategies by Information Type

### Repository Structure
1. List top-level directory contents.
2. Identify build/config files (Makefile, package.json, Dockerfile, etc.).
3. Read README and any docs/ directory index.
4. Map directory tree to one level of depth below each top-level directory.

### Architecture and Patterns
1. Identify entrypoints from build config or standard conventions (main.*, index.*, app.*, cmd/).
2. Trace imports/requires from entrypoints to identify the dependency graph between internal modules.
3. Look for architectural markers: DI containers, middleware chains, router registrations, event bus setup.
4. Identify layering by examining which modules import from which other modules.

### Business Logic
1. From entrypoints, trace the handling path inward: handler → service/usecase → domain logic → side effects.
2. Search for validation functions beyond schema validation: eligibility checks, business rule enforcement, conditional logic.
3. Search for state/status fields in models and enum types with state names.
4. Trace state transition code: assignments to state fields, transition functions, guard conditions.
5. Search for calculation modules: pricing, scoring, ranking, aggregation logic.
6. Search for scheduled job registrations and trace the business logic they execute.
7. Search for concurrency controls: locks, transactions, optimistic concurrency, idempotency keys.

### Domain Vocabulary
1. Scan entity/model class names, enum type names and values, constant names.
2. Scan database table/collection names, event/topic names, API endpoint paths.
3. Search for doc comments on classes and functions for term definitions.
4. Search for glossary sections in README or docs/ files.
5. Cross-reference code names with business-logic findings to map code constructs to business concepts.
6. Identify abbreviations in identifiers and attempt expansion from comments, documentation, or context.
7. Flag terms used with different meanings in different modules.

### Dependencies
1. Parse dependency manifests (package.json, go.mod, requirements.txt, Cargo.toml, pom.xml, build.gradle).
2. Cross-reference with lock files for pinned versions.
3. Search code for service client instantiations (HTTP clients, gRPC stubs, SDK constructors).
4. Search config for connection strings, service URLs, queue names, bucket names.
5. Search for environment variable reads and map each to its purpose.

### API Surface
1. Search for route/endpoint registrations (router.get, @app.route, @Controller, etc.).
2. Identify middleware chains applied to routes (auth, validation, rate limiting).
3. Look for OpenAPI/Swagger spec files, protobuf definitions, GraphQL schemas.
4. Search for event publishing (emit, publish, produce, send) and subscribing (on, subscribe, consume, listen).
5. Identify CLI commands if the service has a CLI interface.

### Data Model
1. Search for ORM model/entity definitions.
2. Locate migration directories and read the most recent and first migrations.
3. Search for direct database query construction (SQL strings, query builders).
4. Identify connection configuration for each data store.
5. Look for caching patterns (Redis client usage, in-memory cache setup).

### Deployment and Infrastructure
1. Read Dockerfile(s) and docker-compose files.
2. Read CI/CD pipeline definitions.
3. Search for Helm charts, Kubernetes manifests, Terraform files.
4. Identify environment-specific configuration (dev, staging, production).
5. Map environment variables to their usage in code.

### Observability
1. Search for logging library initialization and log statements.
2. Search for metrics library initialization and metric recording calls.
3. Search for tracing/span creation.
4. Look for health check endpoint registrations.
5. Search for error tracking SDK initialization (Sentry, Rollbar, etc.).

### Risks
1. Review all `[unknown]`, `[uncertain]`, and `[conflict]` tags from prior artifacts.
2. Check dependency ages and known vulnerability databases (if audit tools are available).
3. Search for TODO, FIXME, HACK, XXX, DEPRECATED markers in code.
4. Identify single points of failure from architecture and deployment artifacts.
5. Assess test coverage gaps from codebase structure artifact.

## Scope Boundaries

### In Scope
- The service repository and all its contents.
- CI/CD definitions within the repository.
- Infrastructure-as-code within the repository.
- Referenced configuration that is accessible in the repository.
- Git history of the repository.

### Out of Scope (unless operator explicitly grants access)
- Other teams' service repositories.
- Production systems, databases, or live environments.
- Internal wikis or documentation systems (unless URLs are provided).
- Package registry internals or private artifact repositories.
- Secrets, credentials, or tokens (even if present in the repository — report their presence as a risk, do not extract values).

## Dealing with Missing Information

When information cannot be found:

1. Document what strategies were attempted.
2. Mark the field with `[unknown]` and the attempted strategies.
3. If the information is `[REQUIRED]`, flag it in the phase completion report for operator attention.
4. Suggest where the information might be found outside the current scope.

If the investigation conclusively shows the capability does not exist (e.g. no gRPC interface after searching for `.proto` files and server registrations), mark the field `[not-applicable]` with the searches performed — do **not** use `[unknown]` for confirmed absences.

Example:

```markdown
**Deployment target**: [unknown]
Attempted: Searched for Kubernetes manifests, Helm charts, Terraform files,
docker-compose files, and CI/CD deploy stages. No deployment configuration
found in the repository. The CI pipeline (`.github/workflows/ci.yml`) only
runs tests — no deploy stage. Deployment configuration may reside in a
separate infrastructure repository.
Source: .github/workflows/ci.yml (file-level)
```
