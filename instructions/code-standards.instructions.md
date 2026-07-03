---
description: 'General coding standards applicable across all languages in this repository.'
applyTo: '**/*'
---

# General Coding Standards

## Function Design

### General Principles

- Prefer pure functions for business logic. Isolate side effects (e.g. database operations, logging) to dedicated layers to improve testability and predictability
- Separate command functions (change state) from query functions (return info)
- Avoid unintended side effects; functions should not modify external state unless it is explicit and part of their responsibility
- Avoid nesting beyond 3 levels deep; refactor complex blocks into smaller, single-purpose functions
- Avoid horizontal scrolling in code; keep lines to a reasonable length (e.g., 80-120 characters) to improve readability
- Avoid global variables; encapsulate state within functions or modules
- Limit argument count to 3 or fewer

### Structure

- Keep functions small and focused on a single responsibility
- Use a consistent top-down structure: main logic first, helper functions after, and data structures at the bottom, to improve readability and maintainability.
- Group related elements together; use alphabetical ordering within those groups when it improves readability.

## Control Flow

### Logic Execution

- Combine related logical checks within the main body into a single `if` condition when it remains readable.
- Do not split regular business logic into multiple arbitrary early returns.
- If a regular control flow condition becomes too long or complex, refactor the logic into a helper function instead of splitting it.

### Data Validation (Guard Clauses)

- Use early returns (guard clauses) immediately after data retrieval or parameter input to exit early if data is invalid, null, or empty.
- Keep data validation out of the main business logic and control flow to prevent deep nesting.
- Ensure all method parameters and external variables are checked for null values before they are used in the business logic.

## Naming Conventions

### General Principles

- Use intention-revealing, searchable names
- Avoid abbreviations unless widely understood
- Avoid repeating domain context already implied by the class or scope
- Avoid using names that are too similar to each other (e.g. `user` and `users`, `data` and `date`) to prevent confusion
- Avoid magic numbers and hardcoded strings; extract them into well-named constants, enums, or configuration files to improve maintainability.

### Methods

- Method and function names should be verbs or verb phrases (e.g., `calculateTotal`, `fetchData`)
- Method names should follow an action + subject pattern
- Use concise, intention-revealing names; avoid redundant or overly specific terms
- Prefer shorter names when removing a word does not reduce clarity (e.g., `removeWarrantyLines` over `removeWarrantyContractLines`)

### Variables

- Variable names should be nouns or noun phrases (e.g. `totalAmount`)
- Keep variable names concise; avoid unnecessary or redundant words while preserving clarity
- Avoid using names that include the variable type (e.g. `userList`, `isActiveFlag`) unless it adds clarity where the type is not obvious from context
- Avoid using names that include implementation details (e.g. `tempData`) that do not convey the purpose or intent
- Declare variables in the narrowest possible scope, preferably within the block where they are used.
- Do not declare variables at the top of a function unless they are used throughout the function.

## Comments

- The code should be self-explanatory; do not add comments unless absolutely necessary.
- Write comments to explain why something is done, not what the code is doing.
- Avoid using comments to explain complex code; instead, refactor the code to be simpler and more understandable
- Delete code that is no longer needed instead of commenting it out

## Error Handling

- Handle errors gracefully and provide informative messages
- Use try/catch for expected errors; let unexpected errors propagate
- Use consistent error handling strategies (e.g., try/catch, error-first callbacks, or promise rejections) based on the language and context
- Avoid swallowing exceptions; if you catch an exception, make sure to log it or handle it in a way that does not silently fail