# Prompt: Phase 1 — Initial Reconnaissance

## Role

You are investigating a microservice codebase to produce a thorough technical assessment. This is Phase 1 of an 11-phase investigation. Your goal is to establish a first-pass understanding of what the service is, what it does, and how the repository is organized.

## Context

Provide the following before executing:

- **Repository path**: `{{REPO_PATH}}`
- **Service name**: `{{SERVICE_NAME}}`
- **Output directory**: `{{OUTPUT_DIR}}`
- **Documentation links** (if any): `{{DOC_LINKS}}`
- **Scope constraints** (if any): `{{SCOPE_CONSTRAINTS}}`

## Policies

You MUST follow these policies throughout the investigation:

- **Gathering Policy**: Every claim must cite a source file and line range. Prefer code over documentation. Do not modify the target repository. See `policies/gathering-policy.md` for full rules.
- **Completeness Policy**: Every field must carry a confidence tag (`[verified]`, `[inferred]`, `[uncertain]`, `[unknown]`, `[conflict]`). Fill all `[REQUIRED]` fields or mark them `[unknown]` with justification. See `policies/completeness-policy.md`.
- **Verification Policy**: Cross-reference claims when possible. Flag staleness and contradictions. See `policies/verification-policy.md`.

## Steps

Execute these steps in order:

### 1. Repository First Impressions

1. List the top-level directory contents.
2. Identify and read the README file (if present). Extract the service description, setup instructions, and any architecture notes.
3. Identify the primary language by examining file extensions, build configs, and dependency manifests.

### 2. Build and Configuration Files

1. Identify all root-level configuration files: Dockerfile, Makefile, package.json, go.mod, requirements.txt, pom.xml, build.gradle, Cargo.toml, or similar.
2. Read each one. Extract: language version, framework, build commands, start command.
3. Identify CI/CD configuration files (.github/workflows/, .gitlab-ci.yml, Jenkinsfile, etc.). Note their presence but do not deeply analyze yet — that is Phase 6.

### 3. Entrypoint Tracing

1. From the build/start configuration, identify the main entrypoint file(s).
2. Read each entrypoint. Identify: what it initializes (server, workers, CLI), what frameworks/libraries it imports, and what modules it wires together.
3. Trace one level of imports from the entrypoint to understand the top-level module structure.

### 4. Directory Layout Mapping

1. For each top-level directory, list its contents one level deep.
2. Annotate each directory's apparent purpose based on naming conventions and contents.
3. Identify standard patterns: src/, lib/, pkg/, cmd/, internal/, test/, config/, deploy/, docs/, scripts/.

### 5. Upstream/Downstream Quick Scan

1. Search for HTTP/gRPC/message client instantiations to identify downstream dependencies.
2. Search for route/handler registrations to identify what APIs this service exposes.
3. Search for event/message consumer registrations.
4. This is a quick scan — detailed analysis happens in Phases 4-5.

### 6. Documentation Inventory

1. If external documentation links were provided, note them for later reference.
2. Search for additional documentation: docs/ directory, wiki links in README, CONTRIBUTING.md, ARCHITECTURE.md, ADR (Architecture Decision Records) directories.
3. Note document freshness by checking last modification dates.

## Output

Fill the following templates and write them to `{{OUTPUT_DIR}}/templates/`:

1. **system-overview.md** — Fill: Service name, Purpose, Business domain, Repository location, Context diagram (preliminary upstream/downstream list). Other fields may remain as placeholders.
2. **codebase-structure.md** — Fill: Primary language and version, Framework, Directory structure, Key files, Entrypoints, Build commands. Architecture pattern and deeper fields are preliminary — they will be refined in Phase 2.

Update the YAML front-matter in each template: set `service_name`, `investigator`, `date`, and update `confidence_summary` counts.

## Completion Criteria

This phase is complete when:

- [ ] All `[REQUIRED]` fields in system-overview.md (Phase 1 scope) are filled or marked `[unknown]`
- [ ] All `[REQUIRED]` fields in codebase-structure.md (Phase 1 scope) are filled or marked `[unknown]`
- [ ] Every factual claim has a source citation and confidence tag
- [ ] The self-review checklist from the verification policy has been executed
- [ ] A phase completion summary has been produced listing: artifacts updated, completeness tier achieved, `[unknown]` and `[conflict]` items

## Escalation Triggers

Stop and request human input if:

- The repository path is inaccessible or empty
- No recognizable build system, language, or framework can be identified
- The repository appears to be a monorepo — clarify which service to investigate
- Credentials or authentication are needed to access referenced resources
