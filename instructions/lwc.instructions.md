---
description: 'Guidelines and best practices for developing Lightning Web Components (LWC) on Salesforce Platform.'
applyTo: '**/main/default/lwc/**'
---

# LWC Development

## 1. Component Usage

### Rule
Prefer Salesforce Lightning Base Components (`lightning-*`) over plain HTML elements.

### Preferred
```html
<lightning-button label="Save"></lightning-button>
<lightning-input label="Name"></lightning-input>
<lightning-card title="Details"></lightning-card>
```

### Avoid
```html
<button>Save</button>
<input type="text" />
<div class="card"></div>
```
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

## 6. Array Handling

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