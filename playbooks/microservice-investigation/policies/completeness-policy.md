# Completeness Policy

This policy defines what "complete" means for each artifact produced during a microservice investigation. Every field in every template is assigned a completeness tier and must carry a confidence tag.

## Completeness Tiers

Each field in an artifact template is marked with one of three tiers:

| Tier | Marker | Rule |
|---|---|---|
| **Minimum Viable** | `[REQUIRED]` | MUST be filled before the phase can be considered complete. If the information cannot be obtained, the field MUST contain `[unknown]` with a brief explanation of why. If the field does not apply to this service at all, it MUST contain `[not-applicable]` with the evidence of absence. |
| **Standard** | `[STANDARD]` | SHOULD be filled for a thorough investigation. Empty standard fields are acceptable only if the agent has exhausted all gathering strategies defined in the gathering policy. |
| **Extended** | `[EXTENDED]` | MAY be filled for deep-dive scenarios (security audit, performance profiling, migration planning). Not expected in a default investigation pass. |

## Confidence Tags

Every factual claim in an artifact MUST carry exactly one confidence tag:

| Tag | Meaning | Evidence Requirement |
|---|---|---|
| `[verified]` | Confirmed by two or more independent sources | Cite both sources (e.g. code + config, code + CI pipeline) |
| `[inferred]` | Derived from a single source or by logical deduction | Cite the source and state the reasoning |
| `[uncertain]` | Based on indirect evidence, naming conventions, or patterns that may be misleading | Cite what was observed and why confidence is low |
| `[unknown]` | Information could not be determined | State what was attempted and why it failed |
| `[not-applicable]` | The capability or aspect confirmedly does not exist in this service (e.g. no gRPC interface, no scheduled jobs) | State what was searched to confirm the absence |
| `[conflict]` | Two or more sources disagree | Cite all conflicting sources and their claims |

`[unknown]` and `[not-applicable]` are distinct: `[unknown]` means the answer exists but could not be found; `[not-applicable]` means the investigation confirmed there is nothing to find. Do not use `[unknown]` for confirmed absences.

The `[stale-source]` marker defined in the verification policy is an **annotation**, not a confidence tag. It supplements the claim's confidence tag (e.g. `[inferred] [stale-source: last modified 2023-01-15]`) and does not count against the "exactly one confidence tag" rule.

## Artifact-Level Completeness Tier

The `completeness_tier` field in each artifact's YAML front-matter records the highest tier the artifact has achieved:

| Value | Criteria |
|---|---|
| `minimum-viable` | Every `[REQUIRED]` field is filled or justified with `[unknown]` / `[not-applicable]` |
| `standard` | `minimum-viable`, plus every `[STANDARD]` field is filled or has its attempted gathering strategies documented |
| `extended` | `standard`, plus `[EXTENDED]` fields filled where the investigation scope called for them |

## Per-Artifact Completeness Criteria

### system-overview.md

| Field | Tier | Notes |
|---|---|---|
| Service name and purpose | `[REQUIRED]` | One-paragraph description of what the service does |
| Business domain / bounded context | `[REQUIRED]` | Which business capability this service serves |
| Repository location | `[REQUIRED]` | URL or path to the source repository |
| Key stakeholders / owning team | `[STANDARD]` | From CODEOWNERS, git history, or docs |
| Context diagram (upstream/downstream) | `[REQUIRED]` | At minimum, list services it calls and services that call it |
| Communication patterns | `[STANDARD]` | Synchronous REST/gRPC, async events, batch, webhooks |
| SLAs / SLOs | `[EXTENDED]` | Often not in code; acceptable as `[unknown]` |
| Age and lifecycle stage | `[STANDARD]` | First commit date, last significant change, deprecation signals |
| Known planned changes | `[EXTENDED]` | Upcoming migrations, rewrites, deprecations |

### business-logic.md

| Field | Tier | Notes |
|---|---|---|
| Use cases | `[REQUIRED]` | At least one fully documented use case per major entrypoint |
| Business rules | `[REQUIRED]` | Every rule beyond schema validation, with implementation location |
| State machines / entity lifecycles | `[REQUIRED]` | Every entity with discrete states: states, transitions, guards |
| Algorithms and processing pipelines | `[STANDARD]` | Non-trivial algorithms described at logic level |
| Domain events and business meaning | `[STANDARD]` | Cross-referenced with api-surface events |
| Scheduled / background processes | `[STANDARD]` | Business logic in cron jobs and background workers |
| Edge cases and invariants | `[EXTENDED]` | Concurrency controls, idempotency, business invariants |

### glossary.md

| Field | Tier | Notes |
|---|---|---|
| Domain terms | `[REQUIRED]` | Term, code name(s), definition, source for every non-obvious domain term |
| Abbreviations and acronyms | `[REQUIRED]` | All non-obvious abbreviations with expansions |
| Overloaded terms | `[STANDARD]` | Terms with different meanings in different contexts |
| External / industry terms | `[STANDARD]` | Domain jargon with definitions |
| Naming conventions | `[STANDARD]` | Patterns for entities, events, tables, config keys |

### codebase-structure.md

| Field | Tier | Notes |
|---|---|---|
| Primary language and version | `[REQUIRED]` | From runtime config, CI, or manifest |
| Framework and major libraries | `[REQUIRED]` | With versions |
| Directory layout description | `[REQUIRED]` | Top-level and one level deep |
| Key files | `[REQUIRED]` | Important root-level files and their purpose |
| Architectural pattern | `[REQUIRED]` | e.g. layered, hexagonal, MVC, event-driven |
| Module / package structure | `[STANDARD]` | Main boundaries and internal dependency direction |
| Entrypoints | `[REQUIRED]` | Main files, CLI commands, event handlers |
| Interface inventory | `[REQUIRED]` | Every route, topic, CLI command, scheduled job with handler reference (type/path/handler only — deepened in Phase 6) |
| Build system and commands | `[REQUIRED]` | How to compile/build |
| Test structure and coverage | `[STANDARD]` | Test framework, location, rough coverage if measurable |
| Code generation or scaffolding | `[STANDARD]` | Protobuf, OpenAPI, ORM generators, etc. |
| Notable patterns | `[STANDARD]` | DI, error handling, logging patterns |
| Coding conventions | `[STANDARD]` | Linter configuration, formatting, naming conventions |
| Dead code and unused modules | `[EXTENDED]` | Requires deeper analysis |

### dependency-inventory.md

| Field | Tier | Notes |
|---|---|---|
| Runtime library dependencies | `[REQUIRED]` | Name, version, purpose |
| Development-only dependencies | `[STANDARD]` | Test frameworks, linters, build tools |
| Internal service dependencies | `[REQUIRED]` | Services this service calls |
| Infrastructure dependencies | `[REQUIRED]` | Databases, caches, queues, object stores |
| External API dependencies | `[REQUIRED]` | Third-party APIs called |
| Known vulnerabilities | `[STANDARD]` | From lock files or audit tools if available |
| Dependency freshness | `[STANDARD]` | How far behind latest versions |
| Transitive dependency risks | `[EXTENDED]` | Deep supply chain analysis |
| How dependencies are managed | `[STANDARD]` | Package manager, lock file strategy, vendoring |
| Private registries or mirrors | `[STANDARD]` | Private package sources, if any |

### api-surface.md

| Field | Tier | Notes |
|---|---|---|
| Exposed endpoints / topics / commands | `[REQUIRED]` | Method, path/topic, brief description |
| Authentication and authorization | `[REQUIRED]` | Scheme, middleware, role/scope model |
| Request/response schemas | `[STANDARD]` | Key fields, types, validation rules |
| API versioning strategy | `[STANDARD]` | URL path, header, or none |
| Known consumers | `[STANDARD]` | Which services or clients call each endpoint |
| CLI commands | `[STANDARD]` | If the service has a CLI interface |
| Scheduled jobs / cron | `[STANDARD]` | Periodic tasks and their handlers |
| Rate limiting and throttling | `[EXTENDED]` | Configuration if present |
| Deprecation markers | `[STANDARD]` | Deprecated endpoints or fields |

### data-model.md

| Field | Tier | Notes |
|---|---|---|
| Data stores (type, version, name) | `[REQUIRED]` | All databases, caches, search engines, file stores |
| Schema / table / collection definitions | `[REQUIRED]` | Key entities and their fields |
| Migration strategy and history | `[REQUIRED]` | Tool used, number of migrations, latest migration |
| Relationships | `[STANDARD]` | Foreign keys, references, embedded documents |
| Data flow diagram | `[STANDARD]` | How data enters, transforms, and exits the service |
| Caching | `[STANDARD]` | What is cached, where, TTL, invalidation |
| Retention and archival policies | `[EXTENDED]` | TTLs, cleanup jobs, archival |
| Data sensitivity classification | `[EXTENDED]` | PII, financial, health data markers |
| Seed / fixture data | `[STANDARD]` | How test/dev data is provisioned |

### deployment-and-infra.md

| Field | Tier | Notes |
|---|---|---|
| CI/CD pipeline description | `[REQUIRED]` | Tool, trigger, stages, artifact produced |
| Containerization | `[REQUIRED]` | Dockerfile, base image, build args |
| Environments | `[REQUIRED]` | List of environments and how they differ |
| Infrastructure-as-code | `[STANDARD]` | Terraform, CloudFormation, Pulumi, etc. |
| Orchestration | `[STANDARD]` | Kubernetes, ECS, serverless, etc. and deployment manifests |
| Scaling configuration | `[STANDARD]` | Replicas, autoscaling rules, resource limits |
| Networking | `[STANDARD]` | Ingress, load balancer, service mesh, TLS termination |
| Secrets management | `[REQUIRED]` | How secrets are injected (env vars, vault, sealed secrets) |
| Rollback procedure | `[STANDARD]` | How to revert a bad deploy |
| Environment variables | `[REQUIRED]` | All env vars referenced in code, with purpose |

### observability.md

| Field | Tier | Notes |
|---|---|---|
| Logging framework and format | `[REQUIRED]` | Library, structured/unstructured, output destination |
| Log levels in use | `[STANDARD]` | Which levels are actively used in code |
| Sensitive data in logs | `[STANDARD]` | Patterns that might log PII, credentials, tokens |
| Metrics instrumentation | `[REQUIRED]` | Library, key metrics emitted, push/pull model |
| Dashboards | `[STANDARD]` | Links or names of monitoring dashboards |
| Distributed tracing | `[STANDARD]` | Library, trace propagation headers |
| Instrumented operations | `[STANDARD]` | Manual span creation beyond automatic instrumentation |
| Alerting rules | `[STANDARD]` | What triggers alerts, notification channels |
| On-call | `[EXTENDED]` | Rotation, escalation policy, if discoverable |
| Health check endpoints | `[REQUIRED]` | Liveness, readiness, startup probes |
| Error tracking | `[STANDARD]` | Sentry, Rollbar, or equivalent integration |

### risk-register.md

| Field | Tier | Notes |
|---|---|---|
| Risk ID and title | `[REQUIRED]` | Unique identifier and short name |
| Category | `[REQUIRED]` | Security, reliability, maintainability, operational, compliance |
| Description | `[REQUIRED]` | What the risk is |
| Severity | `[REQUIRED]` | Critical / High / Medium / Low with justification |
| Evidence | `[REQUIRED]` | Citation to artifact and source |
| Impact | `[REQUIRED]` | What happens if the risk materializes |
| Current mitigation | `[STANDARD]` | What is already in place, if anything |
| Recommended action | `[STANDARD]` | What should be done |
| Effort estimate | `[EXTENDED]` | T-shirt size for remediation |

### runbook.md

| Field | Tier | Notes |
|---|---|---|
| How to build | `[REQUIRED]` | Exact commands |
| How to run locally | `[REQUIRED]` | Dependencies, config, commands |
| How to run tests | `[REQUIRED]` | Commands, expected output |
| How to deploy | `[REQUIRED]` | Steps or pipeline trigger |
| How to rollback | `[STANDARD]` | Steps to revert a deployment |
| Common failure modes | `[STANDARD]` | Known issues and their fixes |
| Troubleshooting guide | `[EXTENDED]` | Deeper diagnostic procedures |
| Emergency contacts | `[EXTENDED]` | On-call rotation, escalation path, if discoverable |

## Phase Completion Gates

A phase is considered complete when:

1. All `[REQUIRED]` fields in the phase's output templates are filled (or explicitly marked `[unknown]` or `[not-applicable]` with justification).
2. Every factual claim carries a confidence tag.
3. The self-review checklist from the verification policy has been executed.
4. Any `[conflict]` or `[unknown]` tags on `[REQUIRED]` fields have been reported to the operator.
5. The artifact-level `completeness_tier` front-matter value has been set per the criteria above.

A phase MAY be considered complete with unfilled `[STANDARD]` fields only if the agent has documented what gathering strategies were attempted.
