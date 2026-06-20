---
description: 'Guidelines and best practices for JavaScript development on the Salesforce Platform'
applyTo: '**/*.js'
---

# JavaScript Development

## 1. Variable Declaration

### Rule
- Use `const`by default for all variable declarations to promote immutability and prevent unintended reassignments.
- Use `let` only when a variable needs to be reassigned
- Avoid using `var` to prevent issues with hoisting and scope.

## 2. Reactivity
- Do not mutate arrays or objects directly; instead, create new instances to trigger reactivity in frameworks like LWC and React.

### Preferred
```js
this.items = [...this.items, newItem];

this.items = this.items.map(item =>
    item.id === updated.id ? { ...item, ...updated } : item
);
```

### Avoid
```js
this.items.push(newItem);
this.items[0].name = 'Updated';
```

## 3. Strict Equality

### Rule
Always use strict equality operators (`===` and `!==`) to avoid unexpected type coercion and ensure predictable comparisons.

### Preferred
```js
if (value === 0) { }
```

### Avoid
```js
if (value == 0) { }
```

## 4. Array Iteration

### 🔹 Rule

Choose the appropriate iteration method based on data size, intent, and readability:
- Use `map()` when transforming arrays into a new array of the same size
- Use `for` loops for large datasets or performance-critical operations
- Use `forEach()` with arrow functions for small datasets where readability is preferred

## 5. Asynchronous Code

### Rule
- Prefer `async/await` for handling asynchronous operations to improve readability and maintainability. Use `try/catch` blocks for error handling in asynchronous code.
- Use Promise patterns when running operations in parallel or handling multiple asynchronous operations that do not depend on each other.