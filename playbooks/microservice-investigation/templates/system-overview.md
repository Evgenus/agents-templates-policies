---
playbook_version: "1.1.0"
service_name: ""
investigator: ""
date: ""
phase: "1, 11"
completeness_tier: ""
confidence_summary:
  verified: 0
  inferred: 0
  uncertain: 0
  unknown: 0
  not_applicable: 0
  conflict: 0
---

# System Overview

## Service Identity

### Service Name `[REQUIRED]`

<!-- The canonical name used in deployment, logging, service mesh, and inter-service communication. -->

Source:

### Purpose `[REQUIRED]`

<!-- One paragraph describing what this service does. Focus on the business capability it provides, not implementation details. -->

Source:

### Business Domain / Bounded Context `[REQUIRED]`

<!-- Which business domain or bounded context does this service belong to? e.g. "payments", "user identity", "order fulfillment". -->

Source:

## Ownership

### Owning Team `[STANDARD]`

<!-- Team name, from CODEOWNERS, git history, or organizational docs. -->

Source:

### Key Stakeholders `[STANDARD]`

<!-- People or roles who depend on or make decisions about this service. -->

Source:

### Repository Location `[REQUIRED]`

<!-- URL or path to the source repository. -->

Source:

## Context

### Context Diagram `[REQUIRED]`

<!-- Diagram or structured list showing:
- Services/systems that call this service (upstream)
- Services/systems this service calls (downstream)
- Data stores it connects to
- External APIs it integrates with

Use a mermaid diagram or a structured list. At minimum, list upstream and downstream services. -->

**Upstream (calls this service):**

| Caller | Protocol | Purpose |
|---|---|---|

**Downstream (this service calls):**

| Dependency | Protocol | Purpose |
|---|---|---|

Source:

### Communication Patterns `[STANDARD]`

<!-- How does this service communicate? Synchronous REST/gRPC, async events/messages, batch jobs, webhooks, etc. -->

Source:

## Lifecycle

### Age and History `[STANDARD]`

<!-- When was the first commit? When was the last significant change? Is this service actively developed, in maintenance mode, or slated for deprecation? -->

| Metric | Value |
|---|---|
| First commit | |
| Last significant commit | |
| Total commits | |
| Active contributors (last 6 months) | |
| Lifecycle stage | |

Source:

### SLAs / SLOs `[EXTENDED]`

<!-- Service-level agreements or objectives, if defined. Availability targets, latency budgets, error rate thresholds. -->

Source:

### Known Planned Changes `[EXTENDED]`

<!-- Any upcoming migrations, rewrites, deprecations, or feature additions that are known. -->

Source:

## Amendments

<!-- If corrections or additions are made after the initial investigation, record them here with date and reason. -->
