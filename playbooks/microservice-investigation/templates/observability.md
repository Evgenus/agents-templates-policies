---
service_name: ""
investigator: ""
date: ""
phase: "7"
completeness_tier: ""
confidence_summary:
  verified: 0
  inferred: 0
  uncertain: 0
  unknown: 0
  conflict: 0
---

# Observability

## Logging `[REQUIRED]`

### Logging Framework

<!-- Library used (winston, pino, logback, zerolog, Python logging, etc.), configuration location, structured vs unstructured. -->

| Aspect | Details |
|---|---|
| Library | |
| Format | |
| Output destination | |
| Configuration location | |

Source:

### Log Levels in Use `[STANDARD]`

<!-- Which log levels appear in the codebase and approximate frequency of each? -->

| Level | Approximate Usage | Sample Location |
|---|---|---|

Source:

### Sensitive Data in Logs `[STANDARD]`

<!-- Are there any patterns that might log PII, credentials, or other sensitive data? -->

Source:

## Metrics `[REQUIRED]`

### Metrics Framework

<!-- Library (Prometheus client, StatsD, Micrometer, OpenTelemetry, etc.), push vs pull model, scrape endpoint. -->

| Aspect | Details |
|---|---|
| Library | |
| Model (push/pull) | |
| Scrape / push endpoint | |

Source:

### Key Metrics Emitted `[REQUIRED]`

<!-- Custom metrics defined in the service code. Not the default runtime metrics, but business and operational metrics the developers chose to track. -->

| Metric Name | Type | Labels | Description |
|---|---|---|---|

Source:

### Dashboards `[STANDARD]`

<!-- Links or names of monitoring dashboards, if discoverable from code, config, or docs. -->

Source:

## Distributed Tracing `[STANDARD]`

### Tracing Framework

<!-- Library (OpenTelemetry, Jaeger client, Zipkin, AWS X-Ray, etc.), trace propagation format. -->

| Aspect | Details |
|---|---|
| Library | |
| Propagation format | |
| Exporter | |

Source:

### Instrumented Operations `[STANDARD]`

<!-- Beyond automatic HTTP/gRPC instrumentation, what operations have manual span creation? -->

Source:

## Health Checks `[REQUIRED]`

<!-- Liveness, readiness, and startup probe endpoints. What do they check? -->

| Probe | Endpoint | Checks |
|---|---|---|

Source:

## Alerting `[STANDARD]`

### Alert Definitions

<!-- Alert rules, thresholds, and notification channels, if discoverable from code or config. -->

| Alert Name | Condition | Severity | Notification Channel |
|---|---|---|---|

Source:

### On-Call `[EXTENDED]`

<!-- On-call rotation, escalation policy, PagerDuty/Opsgenie integration, if discoverable. -->

Source:

## Error Tracking `[STANDARD]`

<!-- Sentry, Rollbar, Bugsnag, or equivalent. How is it initialized? What is captured? -->

| Aspect | Details |
|---|---|
| Tool | |
| Initialization location | |
| DSN / project config | |
| Custom context attached | |

Source:

## Amendments

<!-- If corrections or additions are made after the initial investigation, record them here with date and reason. -->
