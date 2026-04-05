---
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
  conflict: 0
---

# Dependency Inventory

## Runtime Library Dependencies `[REQUIRED]`

<!-- All libraries the service depends on at runtime. Extract from the package manifest and lock file. Focus on direct dependencies; note transitive risks separately. -->

| Package | Version | Purpose | Confidence |
|---|---|---|---|

Source:

## Development Dependencies `[STANDARD]`

<!-- Test frameworks, linters, formatters, build tools, type checkers — anything not shipped to production. -->

| Package | Version | Purpose |
|---|---|---|

Source:

## Internal Service Dependencies `[REQUIRED]`

<!-- Other services within the organization that this service directly communicates with. -->

| Service | Protocol | Purpose | How Discovered |
|---|---|---|---|

Source:

## Infrastructure Dependencies `[REQUIRED]`

<!-- Databases, caches, message brokers, object stores, search engines, and other infrastructure this service connects to. -->

| Component | Type | Version | Connection Config Location | Purpose |
|---|---|---|---|---|

Source:

## External API Dependencies `[REQUIRED]`

<!-- Third-party APIs and services called by this service. -->

| Provider | API / Service | Auth Method | Client Location in Code | Purpose |
|---|---|---|---|---|

Source:

## Dependency Health

### Known Vulnerabilities `[STANDARD]`

<!-- Results from running audit tools (npm audit, pip audit, govulncheck, etc.) or analysis of lock file against known CVE databases. -->

| Package | Vulnerability | Severity | Status |
|---|---|---|---|

Source:

### Dependency Freshness `[STANDARD]`

<!-- How current are the dependencies? Highlight any that are significantly behind the latest version. -->

| Package | Current Version | Latest Version | Versions Behind | Risk |
|---|---|---|---|---|

Source:

### Transitive Dependency Risks `[EXTENDED]`

<!-- Significant risks in the transitive dependency tree: deeply nested critical deps, single-maintainer packages, packages with known supply-chain incidents. -->

Source:

## Dependency Configuration

### How Dependencies Are Managed `[STANDARD]`

<!-- Package manager, lock file strategy, monorepo tooling, vendoring, etc. -->

Source:

### Private Registries or Mirrors `[STANDARD]`

<!-- Does the service pull packages from a private registry, mirror, or artifact repository? -->

Source:

## Amendments

<!-- If corrections or additions are made after the initial investigation, record them here with date and reason. -->
