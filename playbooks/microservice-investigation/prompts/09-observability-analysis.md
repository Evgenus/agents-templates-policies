# Prompt: Phase 9 — Observability Analysis

## Role

You are investigating a microservice codebase. This is Phase 9 of an 11-phase investigation. Your goal is to assess the logging, metrics, tracing, and alerting posture of the service.

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

### 1. Logging Analysis

1. Identify the logging library from the dependency inventory and imports:
   - Node.js: winston, pino, bunyan, console
   - Java: SLF4J/Logback, Log4j, java.util.logging
   - Python: logging, structlog, loguru
   - Go: log, zap, logrus, zerolog, slog
2. Find the logging configuration: initialization code, config files, log level settings.
3. Determine the log format: structured JSON, unstructured text, custom format.
4. Determine the log output destination: stdout, file, remote service (CloudWatch, Datadog, ELK).
5. Search for log statements across the codebase. Categorize by log level (debug, info, warn, error).
6. Check for sensitive data in log statements:
   - Search for log statements near request/response handling that might log PII, tokens, or credentials.
   - Look for broad object logging (`log.info(req.body)`, `logger.debug(user)`) that could leak data.

### 2. Metrics Analysis

1. Identify the metrics library from dependencies and imports:
   - Prometheus client (prom-client, prometheus_client, client_golang/prometheus)
   - StatsD (hot-shots, datadog-metrics)
   - Micrometer
   - OpenTelemetry metrics
   - Cloud-specific (CloudWatch SDK, Datadog APM)
2. Find the metrics initialization and configuration.
3. Determine the export model: pull (Prometheus scrape endpoint) or push (StatsD, OTLP).
4. Search for custom metric definitions and recordings:
   - Counter increments, histogram observations, gauge sets.
   - For each metric: name, type, labels, and what it measures.
5. Distinguish between framework-provided automatic metrics (request duration, etc.) and custom business/operational metrics.

### 3. Distributed Tracing Analysis

1. Identify the tracing library:
   - OpenTelemetry, Jaeger client, Zipkin client, AWS X-Ray SDK, Datadog APM.
2. Find the tracer initialization and configuration.
3. Determine the trace propagation format (W3C TraceContext, B3, X-Ray).
4. Search for manual span creation beyond automatic HTTP/gRPC instrumentation.
5. Check for trace context propagation in outbound calls (HTTP headers, message metadata).

### 4. Health Check Analysis

1. Search for health check endpoint registrations:
   - `/health`, `/healthz`, `/ready`, `/readyz`, `/live`, `/livez`, `/startup`
   - Framework-specific health modules (Spring Actuator, Terminus for NestJS, etc.)
2. Read the health check handlers. Determine what they check:
   - Basic liveness (just returns 200)
   - Readiness (checks database connection, cache availability, etc.)
   - Deep health (checks all dependencies)
3. Record the discovered health endpoints precisely — Phase 11 reconciles them against the orchestration probe configuration from deployment-and-infra.md (Phase 8 runs in parallel with this phase, so do not read its output here).

### 5. Alerting Analysis

1. Search for alert rule definitions within the repository:
   - Prometheus alerting rules (`.rules`, `.yml` with `alert:` key)
   - CloudWatch alarm definitions in IaC
   - Datadog monitors in code/config
   - PagerDuty/Opsgenie integration setup
2. If alert rules are found, extract: alert name, condition/threshold, severity, notification channel.
3. If no alert rules are in the repository, note as `[unknown]` — they may be managed externally.

### 6. Error Tracking Analysis

1. Search for error tracking service integration:
   - Sentry: `Sentry.init`, `@sentry/node`, `sentry-sdk`
   - Rollbar: `Rollbar.init`, `rollbar`
   - Bugsnag: `Bugsnag.start`, `@bugsnag`
   - Airbrake, Honeybadger, etc.
2. If found, identify: initialization location, DSN/project configuration (note the config key, not the value), custom context or tags attached to errors.

### 7. Observability Gaps Assessment

Based on findings, identify:
1. Are errors logged consistently, or are some swallowed silently?
2. Are key business operations instrumented with metrics?
3. Can a request be traced end-to-end across service boundaries?
4. Are health checks meaningful (checking dependencies) or superficial (just return 200)?
5. Is there any mechanism to detect and alert on degraded performance?

## Output

Fill `{{OUTPUT_DIR}}/artifacts/observability.md`:

- All `[REQUIRED]` sections: logging framework, metrics instrumentation, key metrics, health checks.
- All `[STANDARD]` sections: log levels, tracing, dashboards, alerting, error tracking.
- Update YAML front-matter.

## Completion Criteria

- [ ] Logging library, format, and destination are identified
- [ ] Metrics library and key custom metrics are documented
- [ ] Health check endpoints are documented with what they verify
- [ ] At least one log statement is verified in handler/service code (not just setup)
- [ ] At least one metric recording is verified in code (not just initialization)
- [ ] Observability gaps are assessed
- [ ] Self-review checklist executed
- [ ] Phase completion summary produced

## Escalation Triggers

- No logging, metrics, or health checks are present in the codebase at all
- Observability is handled entirely by a sidecar/mesh and is invisible in the service code
- Log statements appear to leak credentials or PII — flag as critical risk
