# Prompt: Phase 4 — Glossary Construction

## Role

You are investigating a microservice codebase. This is Phase 4 of an 11-phase investigation. Your goal is to build a comprehensive domain vocabulary that maps business concepts to code-level names and identifies non-obvious terminology.

## Context

- **Repository path**: `{{REPO_PATH}}`
- **Service name**: `{{SERVICE_NAME}}`
- **Output directory**: `{{OUTPUT_DIR}}`
- **Prior artifacts**: Read all Phase 1-3 artifacts:
  - `{{OUTPUT_DIR}}/templates/system-overview.md`
  - `{{OUTPUT_DIR}}/templates/codebase-structure.md`
  - `{{OUTPUT_DIR}}/templates/business-logic.md`

## Policies

Follow all policies from `policies/gathering-policy.md`, `policies/completeness-policy.md`, and `policies/verification-policy.md`.

## Steps

### 1. Collect Terms from Prior Artifacts

1. Read system-overview.md: extract the business domain, purpose description, and any domain-specific terms mentioned.
2. Read codebase-structure.md: note module names, directory names, and any domain-specific naming patterns.
3. Read business-logic.md: extract every domain term used in use case names, business rule descriptions, state names, event names, and algorithm descriptions.
4. Create an initial term list from these sources.

### 2. Scan Code-Level Names

1. Search for entity/model class definitions. Extract all class names, noting any that use domain-specific terms or non-obvious abbreviations.
2. Search for enum type definitions. Extract all enum names and their values — these often encode domain vocabulary (e.g. `OrderStatus.PENDING_REVIEW`, `AccountType.PREMIUM`).
3. Search for constant/configuration key definitions. Extract named constants, especially those with business meaning (e.g. `MAX_RETRY_ATTEMPTS`, `FREE_TRIAL_DAYS`).
4. Scan database table/collection names from migrations or ORM models.
5. Scan event/topic names from event publishing and subscribing code.
6. Scan API endpoint paths for domain terms (e.g. `/api/v1/reconciliation/`).

### 3. Harvest Definitions from Documentation and Comments

1. Read README and any docs/ files for glossary sections, terminology explanations, or domain overviews.
2. Search for doc comments (JSDoc, Javadoc, docstrings, Go doc comments) on classes, interfaces, and functions — these often define terms in their first sentence.
3. Search for inline comments that explain non-obvious names: patterns like `// "txn" = transaction`, `# A "widget" is...`, `/* FOB = Free On Board */`.
4. Search for GLOSSARY, TERMINOLOGY, DICTIONARY, or DEFINITIONS sections in any markdown files.

### 4. Identify Abbreviations and Acronyms

1. From the collected code names, identify all abbreviations (typically 2-5 uppercase letters or shortened words):
   - Class/function names: `TxnProcessor`, `AcctSvc`, `ReconcJob`
   - Config keys: `SVC_URL`, `AUTH_TTL`, `MSG_Q`
   - Database columns: `txn_id`, `acct_no`, `ref_dt`
2. For each abbreviation, determine the expansion:
   - Check comments and documentation first.
   - If no documentation exists, infer from context and mark as `[inferred]`.
   - If the expansion is genuinely unclear, mark as `[uncertain]` and note what was attempted.
3. Exclude universally understood abbreviations (HTTP, URL, ID, API, DB, JSON, XML, UUID, etc.) unless they have a domain-specific meaning in this codebase.

### 5. Detect Overloaded Terms

1. For each term in the collected list, search for its usage across different modules/packages.
2. Flag terms that appear to mean different things in different contexts. Common patterns:
   - An entity named `Account` in the user module vs. `Account` in the billing module.
   - `Transaction` meaning a database transaction in one context and a financial transaction in another.
   - `Event` meaning a domain event in one module and a calendar event in another.
3. For each overloaded term, document both meanings with their respective contexts and source files.

### 6. Map External / Industry Terms

1. Based on the business domain identified in system-overview.md, search for domain-specific jargon:
   - Finance: ledger, reconciliation, settlement, clearing, escrow, accrual
   - E-commerce: SKU, fulfillment, cart, checkout, inventory, catalog
   - Healthcare: encounter, claim, provider, formulary, adjudication
   - Logistics: shipment, manifest, bill of lading, consignment, waybill
   - Other domains: identify relevant terms from the codebase
2. For each industry term found in code, provide a brief definition that would help a developer unfamiliar with the domain.

### 7. Document Naming Conventions

1. Analyze the collected names for consistent patterns:
   - Prefixes: `I` for interfaces, `Base` for abstract classes, `_` for private
   - Suffixes: `Service`, `Repository`, `Handler`, `Controller`, `Factory`, `Manager`
   - Entity naming: singular vs. plural, PascalCase vs. snake_case
   - Event naming: past tense (`OrderCreated`), imperative (`CreateOrder`), noun-based (`OrderCreation`)
   - Table naming: singular vs. plural, prefixed by module name
   - Config key naming: `PREFIX_CATEGORY_NAME` pattern
2. Document each convention with examples from the codebase.

### 8. Cross-Reference and Validate

1. Verify every term in the glossary actually appears in the codebase — search for each term.
2. Verify abbreviation expansions by finding at least one occurrence of the full form in comments, docs, or variable names.
3. Ensure business-logic.md terms are all represented in the glossary.
4. Flag any terms that appear in code but have no discoverable definition — these are knowledge gaps.

## Output

Fill `{{OUTPUT_DIR}}/templates/glossary.md`:

- All `[REQUIRED]` sections: domain terms, abbreviations and acronyms.
- All `[STANDARD]` sections: overloaded terms, external/industry terms, naming conventions.
- Update YAML front-matter.

## Completion Criteria

- [ ] All entity/model names have glossary entries
- [ ] All non-obvious abbreviations in code identifiers are expanded
- [ ] Overloaded terms (if any) are identified with both meanings and contexts
- [ ] Terms from business-logic.md are all present in the glossary
- [ ] Every term has a source citation
- [ ] Every definition has a confidence tag
- [ ] Self-review checklist executed
- [ ] Phase completion summary produced

## Escalation Triggers

- The codebase uses a domain-specific language or terminology that cannot be understood from code alone — request domain documentation or expert access
- Abbreviations are pervasive and undocumented — more than 20 abbreviations cannot be expanded even with inference
- The service spans multiple business domains with conflicting terminology — request clarification on primary domain scope
