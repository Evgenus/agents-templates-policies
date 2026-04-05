# Prompt: Phase 2 — Codebase Analysis

## Role

You are investigating a microservice codebase. This is Phase 2 of an 11-phase investigation. Your goal is to map the architecture, identify patterns, layering, and key abstractions.

## Context

- **Repository path**: `{{REPO_PATH}}`
- **Service name**: `{{SERVICE_NAME}}`
- **Output directory**: `{{OUTPUT_DIR}}`
- **Phase 1 artifacts**: Read `{{OUTPUT_DIR}}/templates/system-overview.md` and `{{OUTPUT_DIR}}/templates/codebase-structure.md` from the prior phase.

## Policies

Follow all policies from `policies/gathering-policy.md`, `policies/completeness-policy.md`, and `policies/verification-policy.md`.

## Steps

### 1. Review Phase 1 Artifacts

1. Read the Phase 1 codebase-structure.md to understand what was already discovered.
2. Note any `[unknown]` or `[uncertain]` items that may be resolvable with deeper analysis.

### 2. Architectural Pattern Identification

1. Starting from the entrypoints identified in Phase 1, trace the request handling path:
   - How does a request enter the system? (HTTP handler, gRPC method, event handler, CLI command)
   - What layers does it pass through? (controller → service → repository, handler → usecase → adapter, etc.)
   - Where does business logic live vs. infrastructure concerns?
2. Classify the architectural pattern:
   - **Layered / MVC**: Controllers, services, repositories in separate layers with unidirectional dependencies.
   - **Hexagonal / Ports and Adapters**: Core domain with interfaces (ports) implemented by adapters.
   - **Event-driven**: Primarily reacts to events; produces events; minimal synchronous API.
   - **CQRS**: Separate read and write models.
   - **Simple handler-based**: Flat structure, handlers directly access data stores.
   - **Mixed / unclear**: Document which parts follow which pattern.
3. Cite specific files and import relationships as evidence.

### 3. Module Dependency Analysis

1. For each major module or package directory, identify:
   - What it exports (public interface).
   - What it imports from other internal modules.
   - What external libraries it depends on.
2. Identify the dependency direction: do all dependencies point inward (clean architecture) or are there circular dependencies?
3. Create a module dependency summary.

### 4. Key Abstractions and Interfaces

1. Identify the most important interfaces, base classes, or types that define the service's contracts:
   - Repository/DAO interfaces
   - Service interfaces
   - Event/message types
   - Configuration types
   - Error types
2. Read their definitions to understand the service's domain vocabulary.

### 5. Cross-Cutting Concerns

1. Identify how these are handled (search for patterns, middleware, decorators, interceptors):
   - **Error handling**: Global error handler, error types, error responses.
   - **Validation**: Input validation approach (schema validation, decorators, manual).
   - **Configuration**: How config is loaded (env vars, files, remote config).
   - **Dependency injection**: Manual wiring, DI container, or no DI.
   - **Middleware/interceptors**: What middleware is registered and in what order.

### 6. Testing Structure

1. Identify test directories and files.
2. Determine the test framework(s) in use.
3. Categorize test types present: unit, integration, e2e, contract, performance.
4. Estimate coverage: are key paths well-tested, partially tested, or untested?

### 7. Code Quality Signals

1. Check for linter configuration and what rules are enforced.
2. Search for TODO, FIXME, HACK, XXX markers and note their density and themes.
3. Identify any code generation (protobuf, OpenAPI, ORM) and where generated code lives.

## Output

Update `{{OUTPUT_DIR}}/templates/codebase-structure.md`:

- Fill all remaining `[REQUIRED]` and `[STANDARD]` fields.
- Update the architectural pattern section with evidence.
- Add module structure and dependency analysis.
- Fill testing and code quality sections.
- Update YAML front-matter confidence summary.

## Completion Criteria

- [ ] All `[REQUIRED]` fields in codebase-structure.md are filled or marked `[unknown]`
- [ ] All `[STANDARD]` fields have been attempted
- [ ] Architectural pattern is identified with evidence from at least 3 file citations
- [ ] Entrypoints are verified by tracing from build/start config to file
- [ ] Every claim has a source citation and confidence tag
- [ ] Self-review checklist executed
- [ ] Phase completion summary produced

## Escalation Triggers

- The codebase uses an unfamiliar or proprietary framework with no discoverable documentation
- The code is heavily generated and the generation source/tooling is not in the repository
- The codebase appears to contain multiple distinct services — clarify scope
