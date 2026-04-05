# Prompt: Phase 6 — API Surface Analysis

## Role

You are investigating a microservice codebase. This is Phase 6 of an 11-phase investigation. Your goal is to document all interfaces the service exposes and consumes.

## Context

- **Repository path**: `{{REPO_PATH}}`
- **Service name**: `{{SERVICE_NAME}}`
- **Output directory**: `{{OUTPUT_DIR}}`
- **Prior artifacts**: Read `{{OUTPUT_DIR}}/templates/codebase-structure.md` and `{{OUTPUT_DIR}}/templates/dependency-inventory.md`.

## Policies

Follow all policies from `policies/gathering-policy.md`, `policies/completeness-policy.md`, and `policies/verification-policy.md`.

## Steps

### 1. HTTP / REST Endpoint Discovery

1. Search for route registration patterns specific to the framework identified in Phase 2:
   - Express: `router.get`, `router.post`, `app.use`, etc.
   - Spring: `@GetMapping`, `@PostMapping`, `@RequestMapping`, etc.
   - FastAPI: `@app.get`, `@app.post`, `@router.get`, etc.
   - Go net/http: `http.HandleFunc`, `mux.Handle`, etc.
   - Rails: `routes.rb`, `resources`, `get`, `post`, etc.
   - Other: search for common patterns like `route`, `endpoint`, `handler`, `controller`.
2. For each endpoint, extract: HTTP method, path, handler function reference.
3. Check for OpenAPI/Swagger spec files. If present, cross-reference with code-registered routes.

### 2. gRPC Service Discovery

1. Search for `.proto` files in the repository.
2. If found, read service definitions to extract: service name, RPC methods, request/response types.
3. Find the gRPC server registration code and verify it matches the proto definitions.

### 3. Event / Message Interface Discovery

1. Search for event publishing code:
   - `emit`, `publish`, `produce`, `send`, `dispatch` with topic/queue/channel names.
2. Search for event consuming/subscribing code:
   - `on`, `subscribe`, `consume`, `listen`, `handle` with topic/queue/channel names.
3. For each event, identify: topic/queue name, payload schema (if typed), and the triggering condition or handler.

### 4. Authentication and Authorization Analysis

1. Identify the authentication mechanism:
   - Search for JWT verification, token validation, session checking, API key validation middleware.
   - Check for auth-related environment variables (JWT_SECRET, AUTH_URL, API_KEY, etc.).
2. Identify the authorization model:
   - Search for role checks, permission guards, scope validation, policy enforcement.
3. Map which middleware/guards are applied to which routes:
   - Look at route group definitions, middleware chains, decorator stacking.
4. Identify any routes that bypass authentication (public endpoints).

### 5. Request Validation and Error Handling

1. Identify the request validation approach:
   - Schema validation (Joi, Zod, Pydantic, class-validator, JSON Schema).
   - Manual validation in handlers.
   - OpenAPI/Swagger validation middleware.
2. Identify the error response format:
   - Consistent error schema, error codes, HTTP status code mapping.

### 6. API Versioning and Deprecation

1. Check for versioning in URL paths (/v1/, /v2/), headers, or query parameters.
2. Search for deprecation markers: `@Deprecated`, deprecated comments, sunset headers.
3. Look for feature flags or conditional routing that may indicate in-progress API changes.

### 7. CLI and Scheduled Jobs

1. Search for CLI command registrations (yargs, cobra, click, argparse, Thor, etc.).
2. Search for cron/scheduler registrations (node-cron, Quartz, Celery beat, etc.).
3. Document each command or job with its purpose and trigger.

### 8. End-to-End Trace

Trace at least one representative endpoint from route registration through the full handling chain:
1. Route definition → middleware applied → handler function → service/business logic → data access → response construction.
2. Document this trace as evidence that the endpoint inventory is correct.

## Output

Fill `{{OUTPUT_DIR}}/templates/api-surface.md`:

- All `[REQUIRED]` sections: endpoints, events, authentication/authorization.
- All `[STANDARD]` sections: CLI, scheduled jobs, versioning, consumers, deprecations, schemas.
- Update YAML front-matter.

## Completion Criteria

- [ ] All HTTP/gRPC endpoints are listed with method, path, and handler
- [ ] All event publish/subscribe interfaces are documented
- [ ] Authentication and authorization model is described with evidence
- [ ] At least one endpoint has been traced end-to-end
- [ ] OpenAPI spec (if present) has been cross-referenced with code routes
- [ ] Self-review checklist executed
- [ ] Phase completion summary produced

## Escalation Triggers

- Endpoints are dynamically registered and cannot be statically discovered
- Authentication relies on an external service (e.g. API gateway, auth proxy) not visible in the codebase
- The service exposes a protocol not covered in these steps (WebSocket, GraphQL, SOAP, etc.) — describe what was found and request guidance
