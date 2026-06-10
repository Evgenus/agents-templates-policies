# Prompt: Phase 5 — Dependency Mapping

## Role

You are investigating a microservice codebase. This is Phase 5 of an 11-phase investigation. Your goal is to inventory all internal and external dependencies — libraries, services, infrastructure, and external APIs.

## Context

- **Repository path**: `{{REPO_PATH}}`
- **Service name**: `{{SERVICE_NAME}}`
- **Output directory**: `{{OUTPUT_DIR}}`
- **Documentation links** (if any): `{{DOC_LINKS}}`
- **Scope constraints** (if any): `{{SCOPE_CONSTRAINTS}}`
- **Prior artifacts**: Read `{{OUTPUT_DIR}}/artifacts/codebase-structure.md` from Phase 2.

## Policies

Follow all policies from `policies/gathering-policy.md`, `policies/completeness-policy.md`, and `policies/verification-policy.md`.

## Steps

### 1. Library Dependencies

1. Read the primary dependency manifest(s): package.json, go.mod, requirements.txt, Cargo.toml, pom.xml, build.gradle, Gemfile, etc.
2. Read the lock file (if present) for pinned versions.
3. Separate runtime dependencies from development-only dependencies.
4. For each runtime dependency, determine its purpose by:
   - Checking where it is imported in the codebase (search for import/require statements).
   - Reading its one-line description from the manifest or its known purpose.
5. Flag any dependencies that appear in the manifest but are never imported in code (phantom dependencies).

### 2. Internal Service Dependencies

1. Search the codebase for HTTP client instantiations and calls:
   - `fetch`, `axios`, `http.Get`, `requests.get`, `HttpClient`, `RestTemplate`, etc.
2. Search for gRPC client/stub creation and service URLs.
3. Search for service discovery patterns: environment variables containing service URLs, service registry lookups, DNS names.
4. For each discovered service dependency, record: service name, protocol, purpose, and how it was discovered.

### 3. Infrastructure Dependencies

1. Search for database connection setup:
   - Connection strings, ORM configuration, database client instantiation.
   - Identify the database type (PostgreSQL, MySQL, MongoDB, etc.) and version if specified.
2. Search for cache connections: Redis, Memcached, in-memory cache libraries.
3. Search for message broker connections: Kafka, RabbitMQ, SQS, NATS, etc.
4. Search for object/file storage: S3, GCS, Azure Blob, local filesystem access patterns.
5. Search for search engine connections: Elasticsearch, OpenSearch, Solr.
6. For each infrastructure dependency, find the connection configuration location.

### 4. External API Dependencies

1. Search for third-party API client libraries or SDK instantiations.
2. Search for outbound HTTP calls to external domains (non-internal URLs).
3. Identify authentication methods for each external API (API keys, OAuth tokens).
4. Note: Do NOT extract or report actual credential values. Report their presence and location as a security consideration.

### 5. Dependency Health Assessment

1. If an audit tool is available (npm audit, pip audit, safety, govulncheck), note what audit results would provide. If the tool can be run read-only, record its output.
2. For key dependencies, check if the installed version is significantly behind the latest by examining the lock file timestamps and version numbers.
3. Flag any dependencies that are deprecated, archived, or unmaintained (if discoverable from the manifest metadata).

### 6. Cross-Verification

1. Compare the dependency manifest against actual imports in code. Flag:
   - Dependencies declared but never imported (potential dead dependencies).
   - Dependencies imported but not in the manifest (transitive dependency reliance or missing declarations).
2. Cross-reference infrastructure dependencies found in code with configuration files (docker-compose, Helm values, Terraform).

## Output

Fill `{{OUTPUT_DIR}}/artifacts/dependency-inventory.md`:

- All `[REQUIRED]` sections: runtime libraries, internal services, infrastructure, external APIs.
- All `[STANDARD]` sections: dev dependencies, vulnerabilities, freshness, management approach.
- Update YAML front-matter.

## Completion Criteria

- [ ] All `[REQUIRED]` fields are filled or marked `[unknown]`
- [ ] Every dependency has a cited source (manifest file + line, or code import location)
- [ ] Infrastructure dependencies are verified by finding both config and code usage
- [ ] Service dependencies are verified by finding client code and URL/config
- [ ] Cross-verification between manifest and imports is complete
- [ ] Self-review checklist executed
- [ ] Phase completion summary produced

## Escalation Triggers

- Private package registry is referenced but not accessible
- Dependencies reference internal packages that are not in the repository
- The service has no dependency manifest (manually managed dependencies)
- Actual credential values are found committed in the repository (report as critical risk, do not extract)
