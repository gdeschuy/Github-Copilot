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

For simple validation logic:
  - Default to a single conditional that checks all necessary conditions together
  - Combine related checks into one `if` condition when it remains readable and within line length limits.
  - Do not use early returns for simple validation logic
  - Avoid splitting simple validations into multiple early returns.
  - If a condition becomes too long or complex, refactor instead of splitting arbitrarily

Use early returns only when:
  - The logic is complex (e.g., loops, SOQL queries, multiple processing steps)
  - They significantly improve readability by reducing deeply nested structures

## Naming Conventions

### General Principles

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

## Implementation Flexibility

### Principles

- Prefer the simplest and most direct implementation that satisfies the specification.
- Only implement what is explicitly required by the specification.

### Allowed Changes
- Code may be restructured if required to implement the requested change.
- Restructuring should be minimal and limited to what is necessary.
  - Do not refactor or rewrite unaffected logic.
  - Preserve existing patterns and structures unless the change requires deviation

### Prohibited Changes
- Do not change the behavior of the function beyond what is explicitly required by the specification.
- Do not introduce additional logic, state, structure, or UI elements unless explicitly required by the specification.
- Do not introduce alternative patterns (e.g., early returns, different control flow) unless the change makes it necessary.
- Do not introduce defensive programming patterns (e.g., sanitization, deduplication, or normalization) unless explicitly required by the specification.