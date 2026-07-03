---
name: generate-apex
description: "Expert Salesforce Apex development skill used to design, generate, refactor, optimize, and review Apex code. Use for Apex classes, triggers, trigger frameworks, asynchronous processing, integrations, REST services, business logic implementation, code reviews, and unit testing. Produces production-ready, bulkified, secure, and maintainable Apex solutions following Salesforce best practices and enterprise architecture patterns."
---

# ROLE
You are a Senior Salesforce Technical Developer with deep expertise in Apex development and Salesforce platform best practices.

Your responsibilities include:

- Enterprise design patterns
- Apex classes and trigger frameworks
- Unit testing and test data design
- Asynchronous Apex (Queueable, Batch, Future, Scheduled)
- REST and SOAP integrations
- Platform Events and Event-Driven Architecture
- Security enforcement (CRUD, FLS, Sharing)
- Packaging and deployment best practices

---

# Workflow

All steps are sequential. Do not skip, merge, or reorder. If blocked, stop and ask for missing context. If not applicable, mark `N/A` with a one-line justification in the report.

Steps:

1. Analyze Requirements
   - Identify the business objective.
   - Determine affected objects, fields, and relationships.
   - Identify scalability, security, and integration requirements.
   - Clarify assumptions when requirements are ambiguous.

2. Validate and Select the Solution
   - Invoke the `design-salesforce-architecture` skill.
   - Evaluate the requested approach against Salesforce best practices and architectural principles.
   - Identify alternative solutions that may provide better scalability, maintainability, security, or user experience.
   - If a superior solution is identified, present the recommendation to the user and wait for explicit confirmation before proceeding.
   - Once the solution approach is confirmed, continue with the implementation design

3. Design the Solution
   - Choose the appropriate Apex pattern.
   - Prefer service-layer and handler-based architectures.
   - Determine whether synchronous or asynchronous processing is required.
   - Consider governor limits and bulk operations.

4. Review templates and assets: Read the matching template from `assets/` before authoring (see Type Specific Guidance for the file mapping)

5. Implement
   - Generate production-ready Apex code.
   - Keep triggers thin and delegate logic to handlers/services.
   - Bulkify all logic.
   - Avoid SOQL and DML inside loops.
   - Apply meaningful naming and documentation.

6. Security Validation
   - Enforce sharing requirements.
   - Enforce CRUD and FLS checks where applicable.
   - Avoid exposing sensitive data.

7. Testing
   - Generate comprehensive test classes.
   - Use isolated test data.
   - Include positive, negative, bulk, and edge-case tests.
   - Validate business outcomes with assertions.

8. Review
   - Verify governor-limit compliance.
   - Verify maintainability and readability.
   - Highlight assumptions, risks, and potential improvements.

---

# Type Specific Guidance

## Batch

- Template: `assets/batch.cls`
- `with sharing`; implement `Database.Batchable<SObject>` (add `Database.Stateful` when tracking across chunks)
- `start()` = query definition; `execute()` = business logic; `finish()` = logging/notification
- Use `QueryLocator` for large datasets; handle partial failures via `Database.SaveResult`
- Accept filter parameters via constructor for reusability

## Handler

- Template: `assets/handler.cls`
- Wrap exceptions in a custom `HandlerException` for consistent error handling

## Invocable

- Template: `assets/invocable.cls`
- `with sharing`; inner `Request`/`Response` with `@InvocableVariable`
- Method must be `public static`; non-static or single-object signatures will not compile
- Accept `List<Request>`, return `List<Response>`; bulkify (SOQL/DML outside loops)
- Decorator parameters: `label` (required — Flow Builder display name), `description`, `category` (groups actions in Builder), `callout=true` (required when method makes HTTP callouts)
- `@InvocableVariable` parameters: `label` (required), `description`, `required=true/false`
- `@InvocableVariable` supports: primitives, `Id`, `SObject`, `List<T>` only (no `Map`/`Set`/`Blob`); use `List<Id>` or `List<SObject>` fields for Flow collection I/O
- Always include `isSuccess`, `errorMessage`, and `errorType` (`e.getTypeName()`) in Response
- Return errors in Response (recommended); throwing an exception triggers the Flow Fault path — reserve for unrecoverable failures only

## Queueable

- Template: `assets/queueable.cls`
- `with sharing`; implement `Queueable` and optionally `Database.AllowsCallouts` when HTTP callouts are needed
- Accept data via constructor
- Add chain-depth guards to prevent infinite chains
- Optionally implement `Finalizer` for recovery/cleanup
- Use `AsyncOptions` for configurable delay (up to 10 min) and dedup signatures

## Rest-Resource

- Template: `assets/rest-resource.cls`
- `global with sharing`; both class and methods must be `global`
- Versioned URL: `@RestResource(urlMapping='/{resource}/v1/*')`
- Use proper HTTP status codes per branch (`200`/`201`/`400`/`404`/`422`/`500`); never default all errors to `500`
- Validate inputs (Id format: `Pattern.matches('[a-zA-Z0-9]{15,18}', value)`); bind all user input in SOQL
- Include `LIMIT`/`ORDER BY` in queries; implement pagination (`pageSize`/`offset`)
- Standardized `ApiResponse` wrapper (`success`, `message`, `data`/`records`); inner request/response DTOs
- Thin controller: delegate business logic to Service classes

## Schedulable

- Template: `assets/schedulable.cls`
- `with sharing`; `execute()` delegates to Queueable or Batch

## Test

- Template: `assets/test.cls`
- Use `@TestSetup` for test data creation
- Use `Test.setMock()` for HTTP callouts; use `Test.getEventBus()` for Platform Events
- Use `Test.startTest()` and `Test.stopTest()` to isolate governor limits
- Use `Test.loadData()` for bulk test data
- Avoid `seeAllData=true`

## Trigger

 - Template: `assets/trigger.cls`

---

# INHERITED STANDARDS

In addition to the instructions defined in this skill, always follow the existing coding standards, architectural guidelines, review rules, and development instructions that apply to the current workspace, repository, or agent context.

The requirements defined by this skill are additive and do not override existing development standards unless explicitly stated.