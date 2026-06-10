# Prompt: Phase 3 — Business Logic Analysis

## Role

You are investigating a microservice codebase. This is Phase 3 of an 11-phase investigation. Your goal is to understand and document the business logic, use cases, domain rules, state machines, and algorithms implemented by the service.

## Context

- **Repository path**: `{{REPO_PATH}}`
- **Service name**: `{{SERVICE_NAME}}`
- **Output directory**: `{{OUTPUT_DIR}}`
- **Documentation links** (if any): `{{DOC_LINKS}}`
- **Scope constraints** (if any): `{{SCOPE_CONSTRAINTS}}`
- **Prior artifacts**: Read `{{OUTPUT_DIR}}/artifacts/system-overview.md` and `{{OUTPUT_DIR}}/artifacts/codebase-structure.md` from Phases 1-2.

## Policies

Follow all policies from `policies/gathering-policy.md`, `policies/completeness-policy.md`, and `policies/verification-policy.md`.

## Steps

### 1. Review Prior Artifacts

1. Read the system-overview to understand the service's stated purpose and business domain.
2. Read the codebase-structure to understand the architectural pattern, entrypoints, module layout, and key abstractions.
3. Identify the layers where business logic is expected to reside: service/usecase/domain layer (not controller/handler layer and not repository/adapter layer).

### 2. Use Case Discovery

1. Take the interface inventory from codebase-structure.md (Phase 2) as the authoritative list of API endpoints, event handlers, CLI commands, and scheduled jobs. Verify it against the code; flag any interface found in code but missing from the inventory (or vice versa) as a discrepancy.
2. For each entrypoint, trace the handling path inward through the code layers:
   - What controller/handler receives the request?
   - What service/usecase function does it call?
   - What business logic does that function execute?
   - What side effects does it produce (data writes, events emitted, external calls)?
3. Group related entrypoints into use cases. A single use case may involve multiple endpoints (e.g. "create order" might have a create endpoint and a confirm endpoint that are part of the same business operation).
4. For each use case, document:
   - Actor (user role, external service, scheduler)
   - Trigger (API call, event, schedule)
   - Preconditions
   - Main flow as numbered steps
   - Alternative flows (branching paths)
   - Error scenarios and their handling
   - Postconditions (data changes, events emitted, responses returned)

### 3. Business Rule Extraction

1. Within each use case's service/business logic layer, identify rules that go beyond input schema validation:
   - **Eligibility checks**: "User must have role X", "Account must be active", "Balance must be sufficient"
   - **Calculations**: Pricing formulas, tax calculations, discount logic, scoring algorithms
   - **Conditional logic**: "If the order is international, then...", "If the amount exceeds threshold, then..."
   - **Threshold-based decisions**: Rate limits, minimum/maximum values, time windows
   - **Cross-entity validation**: Rules that check state across multiple entities before allowing an operation
2. For each rule, document:
   - Description in plain language
   - Implementation location (file:function)
   - Inputs the rule operates on
   - Logic expressed as plain language or pseudocode
   - What happens when the rule is violated

### 4. State Machine Identification

1. Search for state/status fields in entity models and database schemas:
   - Search for fields named `status`, `state`, `phase`, `stage`, `lifecycle`
   - Search for enum types that represent states (e.g. `OrderStatus`, `PaymentState`)
2. For each stateful entity found:
   - List all possible states (from enum values or constants)
   - Trace transition logic: search for code that changes the state field
   - For each transition: identify the trigger (what causes it), guard conditions (what must be true), and side effects (what else happens)
3. Represent each state machine as a transitions table: From | To | Trigger | Guard

### 5. Algorithm and Pipeline Discovery

1. Search for non-trivial processing logic:
   - Sorting, ranking, or scoring functions
   - Data transformation pipelines (ETL-like operations)
   - Matching or reconciliation algorithms
   - Scheduling or optimization logic
   - Aggregation or reporting calculations
2. For each algorithm:
   - Describe its purpose (what business problem it solves)
   - Summarize the logic at a high level (not line-by-line)
   - Note inputs, outputs, and any complexity concerns

### 6. Domain Event Analysis

1. From the entrypoints and use cases already traced, identify all events emitted:
   - What business action triggers the event?
   - What does the event represent in real-world terms (not just "OrderCreatedEvent" but "a customer has placed a new order")?
   - What downstream processes depend on this event?
   - Are there ordering or idempotency requirements?
2. Cross-reference with event publishing code found during use case tracing.

### 7. Scheduled and Background Process Analysis

1. From the codebase-structure artifact, identify any cron jobs, scheduled tasks, or background workers.
2. For each:
   - What business function does it serve?
   - What data does it read or modify?
   - What happens if it fails or runs late?
   - Is it idempotent (safe to run twice)?

### 8. Edge Cases and Invariants (Extended)

If pursuing the `[EXTENDED]` tier:

1. Search for concurrency controls: locks, transactions, optimistic concurrency checks, mutex usage.
2. Search for idempotency keys or deduplication logic.
3. Search for business invariants enforced by database constraints (unique indexes, check constraints, foreign keys) that complement code-level rules.
4. Search for defensive coding patterns that suggest known edge cases: null checks on specific fields, special-case handling for specific values.

## Output

Fill `{{OUTPUT_DIR}}/artifacts/business-logic.md`:

- All `[REQUIRED]` sections: use cases, business rules, state machines.
- All `[STANDARD]` sections: algorithms, domain events, scheduled processes.
- Update YAML front-matter.

## Completion Criteria

- [ ] At least one use case has been fully documented with main flow, error scenarios, and postconditions
- [ ] All interface inventory entries from the codebase-structure artifact have been accounted for (mapped to a use case or documented as thin wrappers with no significant business logic)
- [ ] All business rules are documented with implementation location and violation behavior
- [ ] All stateful entities have their state machines documented with transitions and guards
- [ ] Domain events are documented with business meaning, not just technical names
- [ ] Every claim has a source citation and confidence tag
- [ ] Self-review checklist executed
- [ ] Phase completion summary produced

## Escalation Triggers

- Business logic is implemented in a language or DSL embedded within configuration files (e.g. rules engine, workflow engine) that requires specialized knowledge to interpret
- The service delegates significant business logic to stored procedures or database functions that are not in the repository
- Business rules reference external systems or data that are not accessible (e.g. "check against the fraud service" but no fraud service client is visible)
- The codebase contains no identifiable business logic layer — handlers directly access data stores with minimal logic (document this as a finding, not a failure)
