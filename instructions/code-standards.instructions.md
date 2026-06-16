---
description: 'General coding standards applicable across all languages in this repository.'
applyTo: '**/*'
---

# General Coding Standards

## Code Structure
- Use a consistent top-down structure: main logic first, helper functions after, and data structures at the bottom, to improve readability and maintainability.

## Function Design
- Keep functions small and focused on a single responsibility
- Prefer pure functions for business logic. Isolate side effects (e.g. database operations, logging) to dedicated layers to improve testability and predictability
- Use control flow constructs (e.g., if/else, switch, early returns, break, continue) to keep logic clear and reduce nesting, but only when they preserve readability and a predictable execution flow.
- Separate command functions (change state) from query functions (return info)
- Avoid unintended side effects; functions should not modify external state unless it is explicit and part of their responsibility
- Avoid nesting beyond 3 levels deep; refactor complex blocks into smaller, single-purpose functions
- Avoid horizontal scrolling in code; keep lines to a reasonable length (e.g., 80-120 characters) to improve readability
- Avoid global variables; encapsulate state within functions or modules
- Declare variables in alphabetical order when possible to improve readability and maintainability
- Limit argument count to 3 or fewer

## Naming Conventions

### General

- Use intention-revealing, searchable names
- Avoid abbreviations unless widely understood
- Avoid repeating domain context already implied by the class or scope
- Avoid using names that are too similar to each other (e.g. `user` and `users`, `data` and `date`) to prevent confusion

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