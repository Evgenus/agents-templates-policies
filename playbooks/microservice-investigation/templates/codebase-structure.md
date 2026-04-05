---
service_name: ""
investigator: ""
date: ""
phase: "1, 2"
completeness_tier: ""
confidence_summary:
  verified: 0
  inferred: 0
  uncertain: 0
  unknown: 0
  conflict: 0
---

# Codebase Structure

## Language and Runtime

### Primary Language and Version `[REQUIRED]`

<!-- e.g. "TypeScript 5.3, running on Node.js 20 LTS" or "Go 1.22" or "Python 3.11". -->

Source:

### Framework `[REQUIRED]`

<!-- Primary web/application framework and version. e.g. "Express 4.18", "Spring Boot 3.2", "FastAPI 0.109". -->

Source:

### Major Libraries `[REQUIRED]`

<!-- List the most significant libraries beyond the framework that shape the architecture. Not an exhaustive dependency list — that goes in dependency-inventory. Focus on libraries that define how the code is structured. -->

| Library | Version | Role |
|---|---|---|

Source:

## Repository Layout

### Directory Structure `[REQUIRED]`

<!-- Top-level directory listing with one level of depth below each significant directory. Annotate each directory's purpose. -->

```
repo-root/
├── ...
```

Source:

### Key Files `[REQUIRED]`

<!-- Important root-level files and their purpose: Dockerfile, Makefile, CI configs, etc. -->

| File | Purpose |
|---|---|

Source:

## Architecture

### Architectural Pattern `[REQUIRED]`

<!-- e.g. "Layered MVC", "Hexagonal / Ports and Adapters", "Event-driven with CQRS", "Simple handler-based". Describe the dominant pattern with evidence. -->

Source:

### Module / Package Structure `[STANDARD]`

<!-- How is the code organized into modules or packages? What are the main boundaries? Which modules depend on which? -->

Source:

### Entrypoints `[REQUIRED]`

<!-- Every way the service can be started or invoked. Trace from the build/start command to the actual file. -->

| Entrypoint | File | Trigger |
|---|---|---|
| <!-- e.g. "HTTP server" --> | <!-- e.g. "src/main.ts" --> | <!-- e.g. "npm start → node dist/main.js" --> |

Source:

## Build System

### Build Tool and Commands `[REQUIRED]`

<!-- How to compile or build the service. Include both development and production builds. -->

| Command | Purpose |
|---|---|

Source:

### Code Generation `[STANDARD]`

<!-- Protobuf compilation, OpenAPI client generation, ORM model generation, GraphQL codegen, etc. -->

Source:

## Testing

### Test Framework and Structure `[STANDARD]`

<!-- Which test framework(s), where tests live, how to run them. -->

| Aspect | Details |
|---|---|
| Framework | |
| Test location | |
| Run command | |
| Test types present | |

Source:

### Test Coverage `[STANDARD]`

<!-- Approximate coverage if measurable. Which areas are well-tested vs. untested? -->

Source:

## Patterns and Conventions

### Notable Patterns `[STANDARD]`

<!-- Dependency injection approach, error handling conventions, request/response patterns, middleware structure, configuration management pattern. -->

Source:

### Coding Conventions `[STANDARD]`

<!-- Linter configuration, formatting rules, naming conventions evident from the code. -->

Source:

### Dead Code and Unused Modules `[EXTENDED]`

<!-- Files, modules, or exports that appear unused. Directories that seem abandoned. -->

Source:

## Amendments

<!-- If corrections or additions are made after the initial investigation, record them here with date and reason. -->
