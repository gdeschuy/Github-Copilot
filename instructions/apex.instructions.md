---
description: 'Guidelines and best practices for Apex development on the Salesforce Platform'
applyTo: '**/*.cls, **/*.trigger'
---

# Apex Development

## General Instructions

- Always use the latest Apex features and best practices for the Salesforce Platform.
- Design for bulkification - write code that handles collections of records, not single records.
- Be aware of governor limits and design solutions that scale efficiently.

## Apex Implementation

### Core Implementation Rules

- Triggers must not contain business logic and must delegate to a single trigger handler.
- Do not add guards for operations that are safe on empty collections (e.g., DML statements).
- Do not perform SOQL and DML operations inside loops.
- Perform DML operations in bulk where possible.

### Sharing Model

- Sharing settings control data access and must always be explicitly defined, regardless of access modifiers. Never omit the sharing declaration, as it leads to unpredictable behavior.
  - **with sharing**: Enforces user-level record access; default for most business logic.
  - **without sharing**: Ignores sharing rules (system context); use only when explicitly required.
  - **inherited sharing**: Inherits the caller’s sharing context; use for helper and service classes where behavior depends on the caller's context.

### Code Style and Readability

- Prefer using ternary operators for simple conditional assignments to improve readability.
- Prefer switch expressions over chained if-else statements for readability and performance.

## Access Modifiers & Keywords

Use the most restrictive access level possible to enforce encapsulation and reduce unintended usage.

- **private**: Default; use for methods and variables that should only be accessed within the same class.
- **public**: Use for methods and variables that need to be accessed from other classes within the same namespace.
- **protected**: Allows access within the class and its subclasses.
- **global**: Use only when cross-namespace access is required (e.g., managed packages).
- **static**: Use for shared state across a transaction. Prefer instance methods over static unless there is a clear reason.
- **final**: Use for classes and methods that should not be extended or overridden. This promotes immutability and prevents unintended behavior changes.

## Asynchronous Processing

Choose the appropriate asynchronous mechanism based on use case; avoid unnecessary asynchronous execution unless requiredfor limits or performance.

- **@future**: Use for simple fire-and-forget operations; avoid for complex or chained logic.
- **Queueable Apex**: Preferred for asynchronous processing; supports chaining and more complex logic.
- **Batch Apex**: Use for large data volumes; processes records in manageable chunks to stay within limits.

## Naming Conventions

- **Classes**: Use `PascalCase` for class names. Name classes descriptively to reflect their purpose.
  - Controllers: suffix with `Controller` (e.g., `AccountController`)
  - Trigger Handlers: suffix with `TriggerHandler` (e.g., `AccountTriggerHandler`)
  - Handlers: suffix with `Handler` (e.g., `AccountHandler`)
  - Test Classes: suffix with `Test` (e.g., `AccountServiceTest`)
  - Batch Classes: suffix with `Batch` (e.g., `AccountCleanupBatch`)
  - Queueable Classes: suffix with `Queueable` (e.g., `EmailNotificationQueueable`)

- **Methods**: Use `camelCase` for method names. Use verbs to indicate actions.
  - Good: `getActiveAccounts()`, `updateContactEmail()`, `deleteExpiredRecords()`
  - Avoid abbreviations: `getAccs()` → `getAccounts()`

- **Variables**: Use `camelCase` for variable names. Use descriptive names.
  - Good: `accountList`, `emailAddress`, `totalAmount`
  - Avoid single letters except for loop counters: `a` → `account`

- **Constants**: Use `UPPER_SNAKE_CASE` for constants.
  - Good: `MAX_BATCH_SIZE`, `DEFAULT_EMAIL_TEMPLATE`, `ERROR_MESSAGE_PREFIX`

- **Triggers**: Name triggers as `ObjectName` + trigger event (e.g., `AccountTrigger`, `ContactTrigger`)

## Null Handling

Always explicitly handle null values to avoid runtime exceptions and ensure predictable behavior.

- **Safe Navigation Operator**: Use the safe navigation operator (`?.`) to safely access properties or methods on potentially null objects.
    ```apex
    String accountName = account?.Name;
    ```
- **Null-Coalescing Operator**: Use the null-coalescing operator (`??`) where appropriate for default values.
    ```apex
    String accountName = account?.Name ?? 'Default Name';
    ```
- **Variables**: Check for null before accessing properties or methods.
    ```apex
    if (account != null) {
        String accountName = account.Name;
    }
    ```
- **Collections (Lists & Sets)**: Check for null before iterating or performing operations.
    ```apex
    if (accountList != null && accountList.size() > 0) {
        for (Account acc : accountList) {
            // Process accounts
        }
    }
    ```
- **Maps**: Check for null before accessing keys or values.
    ```apex
    if (accountMap != null && accountMap.containsKey('someKey')) {
        Account acc = accountMap.get('someKey');
        // Process account
    }
    ```

  ## SOQL Queries

  ### Formatting

  All SOQL queries must follow a consistent multi-line format for readability.
    - The opening square bracket [ must always be followed by a newline
    - Each clause (SELECT, FROM, WHERE) must be on its own line
    - All clauses must always be written in uppercase
    - Fields must be comma-separated with no space before commas and one space after
    - Conditions must be on separate lines, each starting with AND / OR
    - The closing bracket ] must be placed on its own line
  
  ```apex
  List<Account> accounts = [
    SELECT Id, Name, Industry
    FROM Account
    WHERE Industry = 'Technology'
  ];
  
  for (Account accnt : [
    SELECT Id, Name
    FROM Account
    WHERE Name = 'Test Account'
  ]) {
    // logic
  }
  ```

### Selectivity

- When a SOQL query is used inside a for loop, all filtering logic must be applied in the WHERE clause
- Every SOQL query must include a WHERE clause
- Ensure filters use indexed or selective fields where possible
- Use `LIMIT` to restrict results when appropriate
- Do not perform full-table scans

### Dynamic SOQL

When using dynamic SOQL, ensure proper escaping to prevent SOQL injection:

```apex
String name = String.escapeSingleQuotes(userInput);
String query = 'SELECT Id, Name FROM Account WHERE Name = \'' + name + '\'';
List<SObject> results = Database.query(query);
```