# Prompt: Phase 7 — Data Model Analysis

## Role

You are investigating a microservice codebase. This is Phase 7 of an 11-phase investigation. Your goal is to map all data stores, schemas, migrations, and data flows.

## Context

- **Repository path**: `{{REPO_PATH}}`
- **Service name**: `{{SERVICE_NAME}}`
- **Output directory**: `{{OUTPUT_DIR}}`
- **Documentation links** (if any): `{{DOC_LINKS}}`
- **Scope constraints** (if any): `{{SCOPE_CONSTRAINTS}}`
- **Prior artifacts**: Read `{{OUTPUT_DIR}}/artifacts/codebase-structure.md` and `{{OUTPUT_DIR}}/artifacts/dependency-inventory.md` (specifically the infrastructure dependencies section).

## Policies

Follow all policies from `policies/gathering-policy.md`, `policies/completeness-policy.md`, and `policies/verification-policy.md`.

## Steps

### 1. Data Store Identification

1. From the dependency-inventory, list all infrastructure dependencies classified as data stores (databases, caches, search engines, object stores).
2. For each data store, find the connection setup code and configuration.
3. Verify the data store type and version from connection configuration (driver name, connection string format, Docker image version in docker-compose).

### 2. Schema Discovery

#### ORM / Model Definitions
1. Search for ORM model/entity definitions:
   - TypeORM: `@Entity`, Sequelize: `Model.init` / `define`, Django: `models.Model`, SQLAlchemy: `Base`, Prisma: `schema.prisma`, Mongoose: `Schema`, ActiveRecord, etc.
2. For each model/entity, extract: entity name, field names, field types, constraints (not null, unique, default, indexes), and relationships (foreign keys, references).

#### Raw Schema Definitions
1. Search for SQL DDL files, JSON Schema definitions, Avro/Protobuf schema files.
2. Search for raw SQL query strings that reveal table structure (CREATE TABLE, ALTER TABLE).

### 3. Migration Analysis

1. Locate the migration directory (migrations/, db/migrate/, alembic/versions/, etc.).
2. Identify the migration tool (Flyway, Alembic, Knex, TypeORM migrations, Rails migrations, Prisma migrate, etc.).
3. Count total migrations. Read the first migration (to understand the initial schema) and the latest migration (to understand recent changes).
4. Determine how migrations are applied: at deploy time, as a separate job, manually, or automatically on startup.

### 4. Cross-Verification: Models vs. Migrations

1. Compare ORM model definitions against migration history.
2. Check if the current model state is consistent with what migrations would produce.
3. Flag any discrepancies (fields in models not covered by migrations, or migration-created columns not reflected in models).

### 5. Data Flow Mapping

1. For the primary write path: trace how data enters the service (API endpoint, event consumer) through validation, transformation, and persistence.
2. For the primary read path: trace how data is fetched, transformed, and returned.
3. Identify data transformation patterns: DTOs, serializers, mappers between layers.

### 6. Caching Layer

1. From the dependency-inventory, identify cache infrastructure (Redis, Memcached, in-memory).
2. Search for cache read/write patterns in the code.
3. For each cached item, determine: what data is cached, the cache key pattern, TTL, and invalidation strategy.

### 7. Data Access Patterns

1. Identify the data access pattern: repository pattern, DAO, direct queries, active record.
2. Search for complex queries: joins, aggregations, transactions, raw SQL.
3. Note any query builder or ORM patterns that may have performance implications (N+1 queries, large result sets, missing indexes).

### 8. Seed and Fixture Data

1. Search for seed scripts, fixture files, factory definitions.
2. Determine how test data is provisioned for development and testing.

## Output

Fill `{{OUTPUT_DIR}}/artifacts/data-model.md`:

- All `[REQUIRED]` sections: data stores, schema definitions, migrations, migration strategy.
- All `[STANDARD]` sections: relationships, data flow, caching, seed data.
- Update YAML front-matter.

## Completion Criteria

- [ ] All data stores from dependency-inventory are accounted for
- [ ] Key entity schemas are documented with fields and types
- [ ] Migration tool and strategy are identified
- [ ] ORM models and migrations have been cross-referenced
- [ ] At least one write path and one read path have been traced
- [ ] Self-review checklist executed
- [ ] Phase completion summary produced

## Escalation Triggers

- No migrations exist and the schema management approach is unclear
- The service connects to a shared database that may be owned by another service
- The data model includes sensitive data (PII, financial) that may have compliance implications — flag for policy review
- The codebase uses raw SQL exclusively with no schema definitions or migrations
