---
playbook_version: "1.1.0"
service_name: ""
investigator: ""
date: ""
phase: "10"
completeness_tier: ""
confidence_summary:
  verified: 0
  inferred: 0
  uncertain: 0
  unknown: 0
  not_applicable: 0
  conflict: 0
---

# Risk Register

## Severity Rubric

| Severity | Criteria |
|---|---|
| **Critical** | Could cause complete service outage, data loss, or security breach. Requires immediate attention. |
| **High** | Could cause significant service degradation, data integrity issues, or compliance violations. Should be addressed in the current planning cycle. |
| **Medium** | Affects maintainability, developer productivity, or creates conditions for future incidents. Should be planned for remediation. |
| **Low** | Cosmetic, minor inefficiency, or theoretical risk with low probability. Address opportunistically. |

## Risk Categories

| Category | Scope |
|---|---|
| **Security** | Vulnerabilities, insecure patterns, exposed secrets, missing auth |
| **Reliability** | Single points of failure, missing error handling, no retry/circuit-breaker, missing health checks |
| **Maintainability** | Tech debt, outdated dependencies, missing tests, unclear architecture, dead code |
| **Operational** | Missing runbooks, no observability, unclear deployment process, no rollback path |
| **Compliance** | Data handling violations, missing audit trails, retention policy gaps |

## Identified Risks `[REQUIRED]`

<!-- One entry per distinct risk. Risks with the same root cause should be consolidated. -->

### RISK-001: <!-- Title -->

| Field | Details |
|---|---|
| **Category** | `[REQUIRED]` |
| **Severity** | `[REQUIRED]` |
| **Description** | `[REQUIRED]` |
| **Evidence** | `[REQUIRED]` <!-- Cite the artifact and source where this was discovered --> |
| **Impact** | `[REQUIRED]` <!-- What happens if this risk materializes --> |
| **Current Mitigation** | `[STANDARD]` <!-- What, if anything, is already in place --> |
| **Recommended Action** | `[STANDARD]` <!-- What should be done --> |
| **Effort Estimate** | `[EXTENDED]` <!-- T-shirt size: S/M/L/XL --> |

<!-- Copy this block for each additional risk: RISK-002, RISK-003, etc. -->

## Risk Summary

### By Severity

| Severity | Count |
|---|---|
| Critical | |
| High | |
| Medium | |
| Low | |

### By Category

| Category | Count |
|---|---|
| Security | |
| Reliability | |
| Maintainability | |
| Operational | |
| Compliance | |

## Unresolved Unknowns

<!-- List all `[unknown]` items from prior artifacts that could not be resolved and may represent hidden risks. -->

| Source Artifact | Field | Impact if Risk Materializes |
|---|---|---|

## Unresolved Conflicts

<!-- List all `[conflict]` items from prior artifacts that could not be resolved. -->

| Source Artifact | Field | Conflicting Claims |
|---|---|---|

## Amendments

<!-- If corrections or additions are made after the initial investigation, record them here with date and reason. -->
