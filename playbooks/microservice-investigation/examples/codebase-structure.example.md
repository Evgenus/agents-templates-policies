# Golden Example: codebase-structure.md

> This is a **reference example** of a filled `codebase-structure.md` artifact for a small
> synthetic service (`billing-gateway`). It shows the expected granularity, citation style,
> confidence tags, and front-matter usage. It is not a real investigation output.

---

```markdown
---
playbook_version: "1.1.0"
service_name: "billing-gateway"
investigator: "agent:phase-2"
date: "2026-06-11"
phase: "1, 2"
completeness_tier: "standard"
confidence_summary:
  verified: 9
  inferred: 5
  uncertain: 1
  unknown: 1
  not_applicable: 1
  conflict: 1
---

# Codebase Structure

## Language and Runtime

### Primary Language and Version `[REQUIRED]`

TypeScript 5.4 running on Node.js 20 LTS. [verified]

Source: package.json:5-7 (engines.node ">=20") | Dockerfile:1 (FROM node:20-alpine)

### Framework `[REQUIRED]`

Express 4.19. [verified]

Source: package.json:14 | src/app.ts:1-4 (express import and app construction)

### Major Libraries `[REQUIRED]`

| Library | Version | Role |
|---|---|---|
| knex | 3.1 | Query builder and migrations for PostgreSQL [verified] |
| zod | 3.23 | Request schema validation at route boundaries [verified] |
| bullmq | 5.7 | Redis-backed job queue for invoice generation [inferred] |
| pino | 9.0 | Structured JSON logging [verified] |

Source: package.json:12-22 | src/db/knexfile.ts:3 | src/queues/invoice.queue.ts:1-8

## Repository Layout

### Directory Structure `[REQUIRED]`

[verified]

```
billing-gateway/
├── src/
│   ├── routes/        # Express route registrations, one file per resource
│   ├── services/      # Business logic (charge calculation, proration)
│   ├── db/            # Knex config, repositories, migrations/
│   ├── queues/        # BullMQ queue and worker definitions
│   └── app.ts         # Express app wiring; server start in src/main.ts
├── test/              # Jest tests mirroring src/ layout
├── Dockerfile
└── docker-compose.yml # Local Postgres + Redis
```

Source: ls -R output (top two levels)

### Key Files `[REQUIRED]`

| File | Purpose |
|---|---|
| Dockerfile | Two-stage build, runtime on node:20-alpine [verified] |
| docker-compose.yml | Local dev: postgres:16, redis:7 [verified] |
| .github/workflows/ci.yml | Lint, test, build, push image on tag [verified] |

Source: Dockerfile:1-24 | docker-compose.yml:1-30 | .github/workflows/ci.yml:1-58

## Architecture

### Architectural Pattern `[REQUIRED]`

Layered: routes → services → repositories, with unidirectional imports. Routes never import
`db/` directly; all data access goes through repository classes in `src/db/repositories/`.
[inferred] (single source category — code imports only)

Source: src/routes/invoices.routes.ts:1-9 | src/services/invoice.service.ts:1-12 | src/db/repositories/invoice.repo.ts:1-6

### Module / Package Structure `[STANDARD]`

Four internal modules with imports pointing inward: routes → services → repositories → knex.
`queues/` imports from `services/` only. No circular imports detected (madge run, read-only).
[inferred]

Source: madge --circular src (no cycles reported)

### Entrypoints `[REQUIRED]`

| Entrypoint | File | Trigger |
|---|---|---|
| HTTP server | src/main.ts | npm start → node dist/main.js [verified] |
| Invoice worker | src/queues/invoice.worker.ts | npm run worker [verified] |

Source: package.json:8-10 (scripts) | Dockerfile:23 (CMD ["node", "dist/main.js"])

### Interface Inventory `[REQUIRED]`

[verified] 7 interfaces total: 5 HTTP routes, 1 consumed queue, 1 scheduled job. No gRPC
(`[not-applicable]` — no .proto files, no gRPC server registration; searched *.proto,
grpc imports).

| Type | Method / Trigger | Path / Topic / Command | Handler |
|---|---|---|---|
| HTTP | POST | /v1/charges | src/routes/charges.routes.ts:12 |
| HTTP | GET | /v1/charges/:id | src/routes/charges.routes.ts:21 |
| HTTP | POST | /v1/invoices | src/routes/invoices.routes.ts:10 |
| HTTP | GET | /v1/invoices/:id | src/routes/invoices.routes.ts:19 |
| HTTP | GET | /healthz | src/app.ts:31 |
| Queue (consume) | BullMQ job | invoice-generation | src/queues/invoice.worker.ts:14 |
| Scheduled | cron 0 2 * * * | nightly-reconciliation | src/queues/reconcile.job.ts:9 |

Source: src/routes/*.routes.ts | src/app.ts:28-33 | src/queues/*.ts

## Build System

### Build Tool and Commands `[REQUIRED]`

| Command | Purpose |
|---|---|
| npm run build | tsc compile to dist/ [verified] |
| npm start | Run compiled server [verified] |
| npm run dev | ts-node-dev with reload [inferred] |

Source: package.json:8-11 | .github/workflows/ci.yml:24 (runs npm run build)

### Code Generation `[STANDARD]`

None found. [not-applicable] — searched for protobuf, OpenAPI generators, GraphQL codegen,
and ORM model generators; no codegen config or generated-code directories exist.

Source: package.json (file-level) | repository file listing

## Testing

### Test Framework and Structure `[STANDARD]`

| Aspect | Details |
|---|---|
| Framework | Jest 29 [verified] |
| Test location | test/, mirrors src/ [verified] |
| Run command | npm test [verified] |
| Test types present | Unit (services), integration (routes via supertest) [inferred] |

Source: package.json:11,24 | test/services/invoice.service.test.ts:1-8 | .github/workflows/ci.yml:20

### Test Coverage `[STANDARD]`

Coverage not measured in CI. Services layer has tests for charge calculation and proration;
`queues/` has no tests. [uncertain] — based on file presence only, not executed coverage.

Source: test/ directory listing | .github/workflows/ci.yml (no coverage step)

## Patterns and Conventions

### Notable Patterns `[STANDARD]`

Manual constructor injection (services receive repositories as constructor args); zod schemas
validate request bodies at the route boundary; errors are normalized by a single Express error
middleware. [inferred]

Source: src/services/invoice.service.ts:8-15 | src/routes/charges.routes.ts:12-18 | src/app.ts:35-42

### Coding Conventions `[STANDARD]`

ESLint with @typescript-eslint recommended config; Prettier enforced in CI. [verified]

Source: .eslintrc.json:1-12 | .github/workflows/ci.yml:18

**Node version**: [conflict]
- Source A: Node 20 — Dockerfile:1 (node:20-alpine)
- Source B: Node 18 — README.md:12 ("requires Node 18+")
- Assessment: Dockerfile is authoritative (higher source priority); README likely stale.
  [stale-source: README last modified 2024-09-02]

### Dead Code and Unused Modules `[EXTENDED]`

[unknown] — not assessed in the default pass. Attempted: none (EXTENDED tier not requested).

## Amendments

<!-- If corrections or additions are made after the initial investigation, record them here with date and reason. -->
```
