# Verification Policy

This policy defines how the investigating agent verifies its findings to ensure accuracy and reliability of the investigation artifacts.

## Core Verification Principles

1. **Trust code over docs**: When documentation and code disagree, code is the source of truth. Document the discrepancy.
2. **Cross-reference**: Claims backed by two independent sources receive `[verified]`; single-source claims receive `[inferred]` at best.
3. **Flag uncertainty**: It is better to mark something `[uncertain]` than to present a guess as fact.
4. **Preserve contradictions**: Never silently resolve a conflict. Record both sides with `[conflict]`.

## Cross-Reference Rule

A claim MAY be tagged `[verified]` only when confirmed by at least two independent sources from different source categories (as defined in the gathering policy).

Valid cross-reference pairs:

| Primary Source | Confirming Source | Example |
|---|---|---|
| Code (handler) | Configuration (route registration) | "This endpoint exists" confirmed by both route config and handler code |
| Code (import) | Dependency manifest | "Service uses Redis" confirmed by import statement and package.json |
| Migration file | ORM model definition | "users table has email column" confirmed by migration and model |
| Dockerfile | CI/CD pipeline | "Service runs on Node 20" confirmed by Dockerfile FROM and CI matrix |
| Code (env var read) | Config/IaC (env var definition) | "Service reads DATABASE_URL" confirmed by code and Helm values |

Invalid cross-references (same source category):

- Two different code files asserting the same thing (still `[inferred]` — same category)
- README and a wiki page (both documentation — same category)

## Staleness Detection

The agent MUST flag potential staleness when:

| Indicator | Action |
|---|---|
| File not modified in >12 months (by git blame/log) | Add `[stale-source]` annotation with last modified date |
| README or docs reference versions/tools that differ from manifest/config | Record discrepancy with `[conflict]` tag |
| Commented-out code blocks | Note as potential dead code; do not treat as active behavior |
| TODO/FIXME markers older than 12 months | Include in risk register as potential tech debt |
| Deprecated dependency versions (major versions behind) | Flag in dependency inventory |
| CI/CD steps that reference nonexistent files or scripts | Flag as broken pipeline risk |

`[stale-source]` is an annotation, not a confidence tag. It is appended alongside the claim's confidence tag (e.g. `[inferred] [stale-source: last modified 2023-01-15]`) and never replaces it.

## Contradiction Handling

When two sources provide conflicting information:

1. **Record both claims** in the artifact with a `[conflict]` tag:
   ```markdown
   **Database engine**: [conflict]
   - Source A: PostgreSQL 14 — `docker-compose.yml:12` (postgres:14 image)
   - Source B: PostgreSQL 15 — `terraform/rds.tf:8` (engine_version = "15")
   - Assessment: docker-compose likely reflects local dev; Terraform likely reflects production.
   ```

2. **Assess which is more likely authoritative** based on context (e.g. IaC > docker-compose for production config) and note the reasoning.

3. **Do NOT silently pick one**. The operator must see both.

4. **If the conflict affects a `[REQUIRED]` field**, include it in the phase completion report as requiring operator resolution.

## Self-Review Checklist

At the end of each phase, the agent MUST execute this checklist against each artifact updated in that phase:

### Structure Check
- [ ] All `[REQUIRED]` fields are filled or explicitly marked `[unknown]` or `[not-applicable]`
- [ ] YAML front-matter is present and metadata fields are populated
- [ ] No placeholder text (e.g. `<!-- ... -->` prompts) remains in filled fields

### Evidence Check
- [ ] Every factual claim has a source citation
- [ ] Every claim has exactly one confidence tag
- [ ] All file path citations reference files that exist in the repository
- [ ] No citations reference line numbers that are outside the file's range

### Consistency Check
- [ ] Service name is used consistently across all artifacts
- [ ] Dependency names match between dependency-inventory and other artifacts that reference them
- [ ] Environment variable names match between deployment-and-infra and code references
- [ ] API endpoints listed in api-surface match route registrations found in codebase-structure

### Completeness Check
- [ ] Cross-reference against the completeness policy for the current tier
- [ ] All `[unknown]` entries include attempted gathering strategies
- [ ] All `[not-applicable]` entries cite the searches that confirmed the absence
- [ ] All `[conflict]` entries include both sources and an assessment
- [ ] All `[uncertain]` entries include the reasoning for low confidence

## Verification Procedures by Artifact

### system-overview.md
- Verify service purpose by reading the main entrypoint's top-level logic, not just the README.
- Verify upstream/downstream services by searching for HTTP/gRPC client instantiations and incoming route registrations.

### codebase-structure.md
- Verify directory layout claims by listing actual directory contents.
- Verify entrypoints by tracing from the build/start command (package.json scripts, Dockerfile CMD, Makefile targets) to the referenced files.
- Verify framework claims by checking import statements, not just package manifest.
- Verify the interface inventory by sampling at least three entries and confirming their registrations exist in code.

### dependency-inventory.md
- Verify declared dependencies are actually imported/used in code.
- Verify infrastructure dependencies by finding connection/client setup code, not just config entries.
- Cross-reference service dependency claims with actual HTTP/gRPC/event client code.

### api-surface.md
- Cross-check the endpoint list against the Phase 2 interface inventory in codebase-structure.md; investigate and document any additions or removals.
- Trace at least one endpoint from route registration through middleware to handler to response.
- Verify auth claims by finding middleware application on routes, not just middleware definition.
- Verify event contracts by finding both publish and subscribe code for at least one event.

### data-model.md
- Verify schema definitions match between ORM models and migration files.
- Verify data store connections are actually established in code (not just configured).
- Check that migration count and latest migration match the migration directory contents.

### deployment-and-infra.md
- Verify Dockerfile base image matches the language/framework version in the codebase-structure artifact.
- Verify CI/CD stages reference scripts and files that exist.
- Verify environment variables referenced in code are defined in deployment configuration.

### observability.md
- Verify logging by finding actual log statements in handler/service code, not just library setup.
- Verify metrics by finding recording calls, not just library initialization.
- Verify health check endpoints by finding their route registration and handler.

### business-logic.md
- Verify use cases by tracing at least one end-to-end from API call through business logic to side effects (data writes, events emitted).
- Verify state machines by finding the state field definition in the entity/model and confirming each documented transition has corresponding code.
- Verify business rules by finding their enforcement in handler or service code — not just their definition but their actual invocation.
- Cross-reference domain events with event publishing code in the codebase.
- Verify scheduled job descriptions by reading the job handler code.

### glossary.md
- Verify every domain term appears in the codebase — search for each term's code name(s).
- Verify abbreviation expansions by finding at least one occurrence of the full form in comments, documentation, or variable names.
- Verify overloaded terms by confirming different usage contexts with code citations from different modules.
- Flag any term that appears in the glossary but is not referenced in any other artifact — it may be unnecessary.
- Flag any domain-specific term used in other artifacts that is missing from the glossary.

### risk-register.md
- Verify every risk cites evidence from a prior artifact.
- Verify severity ratings follow the rubric (Critical: service down; High: degraded; Medium: maintainability; Low: cosmetic/minor).
- Verify no duplicate risks (same root cause reported multiple times).

### runbook.md
- Verify build commands by cross-referencing with CI/CD pipeline steps.
- Verify local run commands by cross-referencing with docker-compose or README instructions.
- Verify deploy steps by cross-referencing with CI/CD deploy stages.
