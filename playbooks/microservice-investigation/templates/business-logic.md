---
playbook_version: "1.1.0"
service_name: ""
investigator: ""
date: ""
phase: "3"
completeness_tier: ""
confidence_summary:
  verified: 0
  inferred: 0
  uncertain: 0
  unknown: 0
  not_applicable: 0
  conflict: 0
---

# Business Logic

## Use Cases `[REQUIRED]`

<!-- Each use case represents a distinct business operation the service performs.
Trace from the API endpoint or event handler through the service/business logic layer to identify
the complete flow. Group related endpoints by business operation. -->

### UC-001: <!-- Use Case Name -->

| Field | Details |
|---|---|
| **Actor** | <!-- Who or what initiates this: user role, external service, scheduler --> |
| **Trigger** | <!-- API call, event received, cron schedule, manual action --> |
| **Preconditions** | <!-- What must be true before this operation can execute --> |
| **Entrypoint** | <!-- File and function where this use case begins --> |

**Main Flow:**

1. <!-- Step 1 -->
2. <!-- Step 2 -->
3. <!-- Step 3 -->

**Alternative Flows:**

- <!-- Describe any branching paths -->

**Error Scenarios:**

| Error Condition | Handling | Result |
|---|---|---|

**Postconditions:**

- <!-- What is true after successful execution: data changes, events emitted, side effects -->

Source:

<!-- Copy this block for each additional use case: UC-002, UC-003, etc. -->

## Business Rules `[REQUIRED]`

<!-- Rules enforced in code that go beyond input schema validation. These are domain-specific
constraints, calculations, eligibility checks, and conditional logic that embody business decisions. -->

### BR-001: <!-- Rule Name -->

| Field | Details |
|---|---|
| **Description** | <!-- What the rule enforces or calculates --> |
| **Implementation** | <!-- File:function where the rule is implemented --> |
| **Inputs** | <!-- Data the rule operates on --> |
| **Logic** | <!-- The rule expressed in plain language or pseudocode --> |
| **Violation Behavior** | <!-- What happens when the rule is violated: error, rejection, fallback --> |

Source:

<!-- Copy this block for each additional rule: BR-002, BR-003, etc. -->

## State Machines / Entity Lifecycles `[REQUIRED]`

<!-- For each entity that has discrete states (e.g. order: draft → submitted → approved → fulfilled → closed),
document the state machine. Identify by searching for status/state fields in models, enum types
with state names, and transition functions. -->

### Entity: <!-- Entity Name -->

**States:**

| State | Description |
|---|---|

**Transitions:**

| From | To | Trigger | Guard / Condition |
|---|---|---|---|

**State Field Location:**

<!-- File and field name where the state is stored -->

Source:

<!-- Copy this block for each additional entity with state: -->

## Algorithms and Processing Pipelines `[STANDARD]`

<!-- Non-trivial algorithms, data transformation pipelines, batch processing flows,
sorting/ranking/scoring logic. Describe at the logic level, not line-by-line code walkthrough. -->

### Algorithm: <!-- Name -->

| Field | Details |
|---|---|
| **Purpose** | <!-- What business problem this solves --> |
| **Location** | <!-- File(s) and function(s) --> |
| **Input** | <!-- What data goes in --> |
| **Output** | <!-- What comes out --> |
| **Complexity** | <!-- Time/space if notable, or "simple" --> |

**Logic Summary:**

<!-- High-level description of the algorithm. Use pseudocode, numbered steps, or a diagram. -->

Source:

<!-- Copy this block for each additional algorithm. -->

## Domain Events and Their Business Meaning `[STANDARD]`

<!-- Cross-references api-surface.md events but focuses on the BUSINESS meaning:
what real-world thing happened, what downstream processes depend on it,
ordering and idempotency requirements. -->

| Event / Topic | Business Meaning | Real-World Trigger | Downstream Dependents | Ordering / Idempotency |
|---|---|---|---|---|

Source:

## Scheduled / Background Processes `[STANDARD]`

<!-- Business logic that runs on a timer or in the background, not triggered by an API call or event. -->

### Job: <!-- Name -->

| Field | Details |
|---|---|
| **Schedule** | <!-- Cron expression or trigger mechanism --> |
| **Purpose** | <!-- Business reason this job exists --> |
| **Implementation** | <!-- File and function --> |
| **Data Affected** | <!-- What entities or stores does it read/write --> |
| **Failure Impact** | <!-- What happens if this job fails or is delayed --> |
| **Idempotency** | <!-- Can it safely run twice? --> |

Source:

<!-- Copy this block for each additional job. -->

## Edge Cases and Invariants `[EXTENDED]`

<!-- Known edge cases the code handles, business invariants the code enforces,
concurrency safeguards, and idempotency guarantees. -->

### Invariant / Edge Case: <!-- Name -->

| Field | Details |
|---|---|
| **Description** | <!-- What the invariant/edge case is --> |
| **Enforcement** | <!-- How the code ensures it: locks, unique constraints, conditional checks --> |
| **Location** | <!-- File and function --> |
| **Failure Mode** | <!-- What happens if the invariant is violated --> |

Source:

<!-- Copy this block for each additional invariant or edge case. -->

## Amendments

<!-- If corrections or additions are made after the initial investigation, record them here with date and reason. -->
