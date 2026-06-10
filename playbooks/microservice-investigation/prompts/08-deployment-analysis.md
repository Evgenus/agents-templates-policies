# Prompt: Phase 8 — Deployment Analysis

## Role

You are investigating a microservice codebase. This is Phase 8 of an 11-phase investigation. Your goal is to understand how the service is built, deployed, and run across environments.

## Context

- **Repository path**: `{{REPO_PATH}}`
- **Service name**: `{{SERVICE_NAME}}`
- **Output directory**: `{{OUTPUT_DIR}}`
- **Documentation links** (if any): `{{DOC_LINKS}}`
- **Scope constraints** (if any): `{{SCOPE_CONSTRAINTS}}`
- **Prior artifacts**: Read `{{OUTPUT_DIR}}/artifacts/codebase-structure.md` and `{{OUTPUT_DIR}}/artifacts/dependency-inventory.md`.

## Policies

Follow all policies from `policies/gathering-policy.md`, `policies/completeness-policy.md`, and `policies/verification-policy.md`.

## Steps

### 1. CI/CD Pipeline Analysis

1. Identify CI/CD configuration files:
   - `.github/workflows/*.yml` (GitHub Actions)
   - `.gitlab-ci.yml` (GitLab CI)
   - `Jenkinsfile` (Jenkins)
   - `.circleci/config.yml` (CircleCI)
   - `azure-pipelines.yml` (Azure DevOps)
   - `bitbucket-pipelines.yml` (Bitbucket)
   - Other: `Makefile` deploy targets, shell scripts in `scripts/` or `deploy/`.
2. Read each configuration file. For each pipeline, extract:
   - Trigger conditions (push, PR, tag, manual).
   - Stages/jobs and their sequence.
   - What each stage does (lint, test, build, push image, deploy).
   - What artifact is produced (Docker image, binary, archive).
   - Where the artifact is pushed (registry, S3, artifact repository).
3. Identify the deploy stage specifically: what tool triggers the actual deployment, to which environment, with what approval gates.

### 2. Container Analysis

1. Read Dockerfile(s). Extract:
   - Base image and version.
   - Build stages (multi-stage builds).
   - Exposed ports.
   - CMD / ENTRYPOINT.
   - Build arguments and their purposes.
2. Read docker-compose file(s) if present. Extract:
   - Services defined (the application, databases, caches, etc.).
   - Volume mounts, environment variables, port mappings.
   - Whether it is used for local development, CI, or both.
3. Cross-verify the Dockerfile base image version matches the language version from codebase-structure.md.

### 3. Environment Configuration

1. Search for environment-specific configuration:
   - `.env`, `.env.example`, `.env.development`, `.env.production` files.
   - Environment-specific config directories or files.
   - Helm values files per environment (values-dev.yaml, values-prod.yaml).
2. List all known environments and how they differ.
3. Collect all environment variables referenced in the codebase:
   - Search for `process.env`, `os.Getenv`, `os.environ`, `System.getenv`, `ENV`, `ConfigurationManager`, etc.
   - For each variable, determine: name, purpose, default value (if any), whether it is required.
4. Cross-reference environment variables between code, CI/CD config, Docker config, and Helm/IaC.

### 4. Infrastructure as Code

1. Search for IaC files: Terraform (`.tf`), CloudFormation (`.yaml`/`.json` with AWSTemplateFormatVersion), Pulumi, CDK, Ansible, etc.
2. If found, identify what resources are managed: compute, networking, databases, storage, IAM, DNS.
3. Note how IaC is applied: in the CI/CD pipeline, manually, or via a separate process.

### 5. Orchestration and Deployment Manifests

1. Search for Kubernetes manifests: Deployment, Service, Ingress, ConfigMap, Secret, HPA, PDB.
2. Search for Helm charts: `Chart.yaml`, `values.yaml`, templates.
3. Search for other orchestration: ECS task definitions, serverless configs (serverless.yml, SAM templates), Docker Swarm configs.
4. Extract: replica counts, resource limits, autoscaling rules, health check configuration, update strategy (rolling, blue-green, canary).

### 6. Secrets Management

1. Identify how secrets are provided to the service:
   - Kubernetes Secrets (referenced in manifests)
   - External secrets operator (ExternalSecret resources)
   - Vault integration (code or sidecar)
   - Cloud provider secrets (AWS Secrets Manager, GCP Secret Manager)
   - Environment variables from CI/CD
   - `.env` files (flag as risk if used in production)
2. Check for any committed secrets (even in example/test files). Note their presence as a risk — do NOT extract values.

### 7. Networking and Ingress

1. Search for ingress rules, load balancer configuration, service mesh sidecar config.
2. Identify TLS termination point.
3. Note any domain names or URL patterns configured.

### 8. Rollback

1. Search for rollback mechanisms: deployment strategy (rolling update with rollback), Helm rollback, manual procedures documented in scripts or README.
2. If no rollback mechanism is found, note as a risk.

## Output

Fill `{{OUTPUT_DIR}}/artifacts/deployment-and-infra.md`:

- All `[REQUIRED]` sections: CI/CD, containerization, environments, secrets, environment variables.
- All `[STANDARD]` sections: IaC, orchestration, scaling, networking, rollback.
- Update YAML front-matter.

## Completion Criteria

- [ ] CI/CD pipeline is documented with stages and triggers
- [ ] Dockerfile is analyzed and cross-verified with codebase language version
- [ ] All environments are listed with their differences
- [ ] All environment variables from code are documented with purpose
- [ ] Secrets management approach is identified
- [ ] Deployment pipeline can be traced from commit to production
- [ ] Self-review checklist executed
- [ ] Phase completion summary produced

## Escalation Triggers

- Deployment is handled by a separate team/repo and no deploy config exists in this repository
- Secrets appear to be committed in the repository
- The CI/CD pipeline references external scripts or tools not in the repository
- No containerization or deployment configuration exists — service may be deployed manually
