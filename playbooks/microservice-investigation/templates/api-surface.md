---
playbook_version: "1.1.0"
service_name: ""
investigator: ""
date: ""
phase: "6"
completeness_tier: ""
confidence_summary:
  verified: 0
  inferred: 0
  uncertain: 0
  unknown: 0
  not_applicable: 0
  conflict: 0
---

# API Surface

## HTTP / REST Endpoints `[REQUIRED]`

<!-- All HTTP endpoints exposed by this service. Extract from route registrations, controller decorators, or OpenAPI specs. -->

| Method | Path | Handler | Auth | Description |
|---|---|---|---|---|

Source:

## gRPC Services `[REQUIRED]`

<!-- If the service exposes gRPC, list services and methods. Reference the proto files.
If the service exposes no gRPC interface, mark this section `[not-applicable]` and cite the
searches performed (e.g. no .proto files, no gRPC server registration). -->

| Service | Method | Request Type | Response Type | Description |
|---|---|---|---|---|

Source:

## Event / Message Contracts `[REQUIRED]`

<!-- Events or messages this service publishes or consumes. -->

### Published Events

| Event / Topic | Payload Schema | Trigger | Destination |
|---|---|---|---|

### Consumed Events

| Event / Topic | Payload Schema | Handler | Source |
|---|---|---|---|

Source:

## CLI Commands `[STANDARD]`

<!-- If the service has a CLI interface, list commands and their purpose. -->

| Command | Arguments | Description |
|---|---|---|

Source:

## Scheduled Jobs / Cron `[STANDARD]`

<!-- Periodic tasks, cron jobs, or scheduled functions. -->

| Schedule | Handler | Description |
|---|---|---|

Source:

## Authentication and Authorization `[REQUIRED]`

### Authentication Scheme

<!-- How are callers authenticated? JWT, API key, OAuth2, mTLS, session cookie, etc. -->

Source:

### Authorization Model

<!-- How are permissions enforced? RBAC, ABAC, scope-based, policy engine, etc. -->

Source:

### Middleware / Guard Chain

<!-- What middleware or guards are applied to routes? In what order? -->

| Middleware / Guard | Applied To | Purpose |
|---|---|---|

Source:

## API Versioning `[STANDARD]`

<!-- How is API versioning handled? URL path (/v1/), header, query param, or not at all? -->

Source:

## Request / Response Schemas `[STANDARD]`

<!-- Key request and response shapes for the most important endpoints. Reference OpenAPI spec, types, or validation schemas. -->

Source:

## Known Consumers `[STANDARD]`

<!-- Which services, frontend apps, or external clients consume this API? How was this determined? -->

| Consumer | Endpoints Used | How Discovered |
|---|---|---|

Source:

## Rate Limiting and Throttling `[EXTENDED]`

<!-- Rate limiting configuration, per-client or global limits, throttling behavior. -->

Source:

## Deprecations `[STANDARD]`

<!-- Endpoints, fields, or events that are marked as deprecated or appear unused. -->

| Item | Type | Deprecation Signal | Replacement |
|---|---|---|---|

Source:

## Amendments

<!-- If corrections or additions are made after the initial investigation, record them here with date and reason. -->
