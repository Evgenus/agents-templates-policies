# Prompt: Phase 10 — Risk Assessment

## Role

You are investigating a microservice codebase. This is Phase 10 of an 11-phase investigation. Your goal is to identify and classify technical risks, debt, and operational hazards based on all prior investigation findings.

## Context

- **Repository path**: `{{REPO_PATH}}`
- **Service name**: `{{SERVICE_NAME}}`
- **Output directory**: `{{OUTPUT_DIR}}`
- **Documentation links** (if any): `{{DOC_LINKS}}`
- **Scope constraints** (if any): `{{SCOPE_CONSTRAINTS}}`
- **Prior artifacts**: Read ALL completed artifacts from `{{OUTPUT_DIR}}/artifacts/`:
  - `system-overview.md`
  - `codebase-structure.md`
  - `business-logic.md`
  - `glossary.md`
  - `dependency-inventory.md`
  - `api-surface.md`
  - `data-model.md`
  - `deployment-and-infra.md`
  - `observability.md`

## Policies

Follow all policies from `policies/gathering-policy.md`, `policies/completeness-policy.md`, and `policies/verification-policy.md`.

## Severity Rubric

Use the severity rubric and risk categories defined at the top of the `risk-register.md` template (the single source of truth for both). Apply them consistently across all risk entries.

## Steps

### 1. Collect Signals from Prior Artifacts

Review each artifact and extract risk signals:

1. **From system-overview.md**:
   - Missing or unclear ownership
   - No SLAs/SLOs defined
   - Service in maintenance mode with no active contributors

2. **From codebase-structure.md**:
   - Outdated language/framework versions
   - Missing or inadequate test coverage
   - Circular dependencies, unclear architecture
   - High density of TODO/FIXME/HACK markers
   - Dead code or abandoned modules

3. **From business-logic.md**:
   - Undocumented or unclear business rules that could be misinterpreted during changes
   - State machines with missing transition guards or unreachable states
   - Business rules implemented inconsistently across different code paths
   - Missing edge case handling for critical business operations
   - Scheduled jobs without idempotency guarantees

4. **From glossary.md**:
   - Overloaded terms that could cause developer confusion and bugs
   - Undocumented abbreviations in critical code paths
   - Mismatches between code naming and business terminology

5. **From dependency-inventory.md**:
   - Known vulnerabilities in dependencies
   - Significantly outdated dependencies
   - Phantom dependencies (declared but unused)
   - Single-maintainer or archived packages in critical paths

6. **From api-surface.md**:
   - Endpoints without authentication
   - Missing input validation
   - Deprecated endpoints still in use
   - No API versioning strategy

7. **From data-model.md**:
   - Unmanaged schema migrations
   - No migration strategy
   - PII/sensitive data without classification
   - Missing data retention policies
   - Model/migration discrepancies

8. **From deployment-and-infra.md**:
   - No CI/CD pipeline or incomplete pipeline
   - Committed secrets or insecure secret management
   - Missing rollback procedure
   - No autoscaling or inadequate resource limits
   - Environment variables referenced in code but not defined in config

9. **From observability.md**:
   - Missing logging, metrics, or health checks
   - Superficial health checks (always return 200)
   - Potential PII in logs
   - No alerting rules
   - No distributed tracing

### 2. Collect Unknowns and Conflicts

1. Scan all artifacts for `[unknown]` tags. Each unknown on a `[REQUIRED]` field is itself a risk — information that should exist but could not be determined.
2. Scan all artifacts for `[conflict]` tags. Unresolved conflicts indicate potential misconfigurations or documentation drift.

### 3. Additional Code-Level Risk Scan

Perform targeted searches for common risk patterns:

1. **Security**:
   - Search for hardcoded credentials, API keys, passwords in code (not config).
   - Search for SQL string concatenation (SQL injection risk).
   - Search for disabled security features (CORS `*`, CSRF disabled, TLS verification disabled).
   - Search for `eval`, `exec`, or dynamic code execution.
2. **Reliability**:
   - Search for missing error handling: unhandled promise rejections, empty catch blocks, swallowed errors.
   - Search for missing timeouts on HTTP/database/cache clients.
   - Search for retry logic without backoff or circuit breakers.
   - Check for single points of failure (single replica, no health checks).
3. **Maintainability**:
   - Assess code complexity: very large files (>500 lines), very large functions (>100 lines).
   - Check for duplicated logic across handlers or services.
   - Assess documentation currency vs. code reality.

### 4. Classify and Record Risks

For each identified risk:

1. Assign a unique ID (RISK-001, RISK-002, etc.).
2. Assign a category (Security, Reliability, Maintainability, Operational, Compliance).
3. Write a clear description.
4. Assign severity using the template's rubric with a brief justification.
5. Cite the evidence: which artifact, which source file/line.
6. Note any existing mitigation.
7. Recommend an action if clear.

### 5. Consolidate

1. Merge risks that share a root cause (e.g. "no tests" and "untested error paths" are one risk).
2. Produce summary counts by severity and category.
3. List all unresolved `[unknown]` and `[conflict]` items with their potential impact.

## Output

Fill `{{OUTPUT_DIR}}/artifacts/risk-register.md`:

- All `[REQUIRED]` fields for each risk entry.
- Summary tables by severity and category.
- Unresolved unknowns and conflicts sections.
- Update YAML front-matter.

## Completion Criteria

- [ ] All prior artifacts have been reviewed for risk signals
- [ ] All `[unknown]` and `[conflict]` items are collected and assessed
- [ ] Additional code-level risk scan has been performed
- [ ] Every risk has a unique ID, category, severity, description, and evidence citation
- [ ] No duplicate risks (same root cause)
- [ ] Summary counts are accurate
- [ ] Self-review checklist executed
- [ ] Phase completion summary produced

## Escalation Triggers

- Critical security risks are discovered (committed secrets, SQL injection, authentication bypass) — report immediately, do not wait for phase completion
- Evidence suggests the service handles sensitive data (PII, financial, health) with no compliance controls — flag for compliance review
- The risk register exceeds 30 entries — consider grouping and summarizing by theme
