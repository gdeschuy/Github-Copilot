---
description: 'Guidelines and best practices for developing Lightning Web Components (LWC) on Salesforce Platform.'
applyTo: '**/lwc/**'
---

# LWC Development

## 1. Component Usage

### Rule
You must use Salesforce Lightning Base Components (`lightning-*`) instead of plain HTML elements whenever possible.
- <button> must always be replaced with <lightning-button>
- <input> must always be replaced with <lightning-input>

### Exceptions
- No equivalent Lightning component exists
- Structural elements (div, span)
- Highly custom UI (justified)

## 2. Avoid Custom Styles

### Rule
Prefer SLDS utility classes over custom CSS.

### Preferred
```html
<div class="slds-m-around_medium slds-p-horizontal_small"></div>
<div class="slds-grid slds-wrap slds-gutters"></div>
```

### Avoid
```css
.custom-margin {
    margin: 16px;
}
```

## 3. Avoid Inline Styles

### Rule
Do not use inline style attributes.

### Preferred
```html
<div class="slds-text-align_center slds-m-top_medium"></div>
```

```css
.custom-container {
    display: flex;
    justify-content: center;
}
```

### Avoid
```html
<div style="margin-top: 1rem; text-align: center;"></div>
```

### Exceptions
Only for dynamic values that cannot be handled otherwise

```html
<div style={dynamicStyle}></div>
```

### Guidelines
- Use SLDS spacing (slds-m-*, slds-p-*)
- Use SLDS grid (slds-grid, slds-col)
- Keep CSS minimal
- Reuse SLDS before writing CSS

## 4. Conditional Rendering

### Rule
Use `lwc:if` for conditional rendering in templates. Avoid using `if:true` and `if:false` directly with complex expressions in templates.

### Preferred
```html
<template lwc:if={showLoading}></template>
<template lwc:elseif={hasItems}></template>
<template lwc:else></template>
```

### Avoid
```html
<template if:true={hasItems}></template>
<template if:false={hasItems}></template>
```

## 5. UI States

### Rule
Model UI states in JavaScript using getters.

```js
get showLoading() {
    return this.isLoading;
}

get hasItems() {
    return Array.isArray(this.items) && this.items.length > 0;
}

get isEmpty() {
    return !this.hasItems && !this.isLoading;
}
```
## 6. Data Fetching

### Rule
Use `@wire` for read-only, reactive data fetching. Use imperative Apex for:
  - user-initiated actions (e.g., button clicks)
  - data mutations (create, update, delete)
  - controlled execution flows

## 7. Array Handling

### Rule
Always use getters for array checks used in templates.

### Preferred
```js
get hasItems() {
    return Array.isArray(this.items) && this.items.length > 0;
}

get isEmpty() {
    return !Array.isArray(this.items) || this.items.length === 0;
}
```

```html
<template if:true={hasItems}></template>
<template if:true={isEmpty}></template>
```

### Avoid
```html
<template if:true={items.length > 0}></template>
```

## 8. Error Handling

### Rule
Always handle errors explicitly and display them using a standardized error component (c-error-panel).

### Example
```html
<template if:true={hasErrors}>
  <c-error-panel errors={errors}></c-error-panel>
</template>
```

## 9. Event Communication

### Rule
Use custom events for communication from child to parent components. Use `@api` properties for parent to child communication.

### Guidelines
- Use lowercase event names (e.g., `save`, `recordchange`)
- Keep event payload (detail) minimal and structured

## 9. Template vs DOM Elements

### Rule
Use `template` for rendering logic and structural directives (`for:each`, `if:true`, etc.). Use DOM elements (e.g., `div`, `span`) for layout and styling.

```html
<template if:true={hasItems}>
    <div class="slds-p-around_medium">
        
        <template for:each={items} for:item="item">
            <div key={item.id} class="slds-m-bottom_small">
                <span>{item.name}</span>
            </div>
        </template>

    </div>
</template>
```

## 10. Template Iteration

### Rule
Always provide a unique key for each item in a list when using `for:each` directive.

### Example
```html
<template for:each={items} for:item="item">
    <div key={item.id}>
        {item.name}
    </div>
```
