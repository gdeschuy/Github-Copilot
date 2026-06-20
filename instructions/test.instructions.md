---
description: 'Guidelines and best practices for Apex development on the Salesforce Platform'
applyTo: '**/*Test.cls, **/*Tests.cls'
---

# Test Development

## Test Coverage

- All new or modified Apex logic must be covered by tests, aiming for the highest possible coverage.
- Tests must cover all relevant execution paths and business behavior, not just basic execution.
- Strive for near-complete coverage of new and changed code.
- Never use @IsTest(SeeAllData=true).
- Tests must validate business logic, not just achieve coverage.
- Cover edge cases and boundary conditions where applicable.
- No outdated or failing tests are allowed.

## Test Design

- Follow Arrange–Act–Assert structure.
- Test one scenario per method.
- Cover both positive and negative cases where relevant.
- Avoid test interdependencies; each test must be independent and deterministic.
- Each test must include assertions with descriptive failure messages.
- Use @TestSetup to create reusable test data.