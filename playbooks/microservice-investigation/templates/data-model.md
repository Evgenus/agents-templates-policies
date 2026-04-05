---
service_name: ""
investigator: ""
date: ""
phase: "5"
completeness_tier: ""
confidence_summary:
  verified: 0
  inferred: 0
  uncertain: 0
  unknown: 0
  conflict: 0
---

# Data Model

## Data Stores `[REQUIRED]`

<!-- All databases, caches, search engines, file/object stores, and other persistent or semi-persistent storage this service uses. -->

| Store | Type | Version | Purpose | Connection Config |
|---|---|---|---|---|

Source:

## Schema Definitions `[REQUIRED]`

<!-- Key entities, tables, collections, or document types. Include field names, types, and constraints for the most important entities. -->

### Entity: <!-- name -->

| Field | Type | Constraints | Notes |
|---|---|---|---|

Source:

<!-- Repeat for each significant entity. -->

## Relationships `[STANDARD]`

<!-- How do entities relate to each other? Foreign keys, references, embedded documents, etc. -->

Source:

## Data Flow `[STANDARD]`

<!-- How does data enter, move through, and exit the service? Describe the key write and read paths. Use a diagram if helpful. -->

Source:

## Migrations `[REQUIRED]`

### Migration Tool

<!-- What tool manages schema migrations? e.g. Flyway, Alembic, Knex, TypeORM migrations, Rails ActiveRecord, etc. -->

Source:

### Migration History

| Metric | Value |
|---|---|
| Total migrations | |
| First migration date | |
| Latest migration date | |
| Latest migration description | |

Source:

### Migration Strategy `[REQUIRED]`

<!-- How are migrations applied? At deploy time, via a separate job, manually, or not managed at all? -->

Source:

## Caching `[STANDARD]`

<!-- Caching layers: what is cached, where (Redis, Memcached, in-memory), TTL, invalidation strategy. -->

| Cached Data | Cache Store | TTL | Invalidation |
|---|---|---|---|

Source:

## Data Retention and Archival `[EXTENDED]`

<!-- Retention policies, cleanup jobs, archival processes, data lifecycle rules. -->

Source:

## Data Sensitivity `[EXTENDED]`

<!-- Classification of data handled: PII, financial data, health data, authentication credentials. Any compliance implications (GDPR, HIPAA, PCI-DSS). -->

| Entity / Field | Sensitivity | Classification | Compliance |
|---|---|---|---|

Source:

## Seed and Fixture Data `[STANDARD]`

<!-- How is test/development data provisioned? Seed scripts, fixtures, factories, data generators. -->

Source:

## Amendments

<!-- If corrections or additions are made after the initial investigation, record them here with date and reason. -->
