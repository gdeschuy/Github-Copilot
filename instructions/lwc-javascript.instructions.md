---
description: 'Guidelines and best practices for JavaScript development on the Salesforce Platform'
applyTo: '**/lwc/*.js'
---
# LWC JavaScript Development

## 1. File structure

### File-Level Ordering

All LWC JavaScript files should be structured in the following order:

1. Imports from LWC and standard libraries
2. Imports from Apex classes
3. Other imports (utilities, labels, schema, etc.)
4. Constants (defined outside the class)

```javascript
// 1. LWC / standard libraries
import { LightningElement, api, track } from 'lwc';

// 2. Apex imports
import getData from '@salesforce/apex/MyController.getData';

// 3. Other imports
import SOME_LABEL from '@salesforce/label/c.SomeLabel';

// 4. Constants
const DEFAULT_LIMIT = 10;
```
### Class-Level Ordering

Inside the component class, members should be ordered as follows:

1. Properties and variable declarations
2. @wire adapters and wired functions
3. Public methods (exposed via @api)
4. Getters
5. UI triggered event handlers (prefix with handle)
6. Private methods for internal logic and reusable functions
7. Lifecycle hooks (connectedCallback, renderedCallback, etc.)

```javascript
export default class MyComponent extends LightningElement { 
    // 1. Properties
    @track data;
    @api recordId;

    // 2. @wire
    @wire(getData, { recordId: '$recordId' })
    wiredData({ error, data }) { }

    // 3. Public methods
    @api refresh() { }

    // 4. Getters
    get hasData() { }

    // 5. Event handlers
    handleClick() { }

    // 6. Private methods
    processData(data) { }

    // 7. Lifecycle hooks
    connectedCallback() { }
}
```
## 2. Data Fetching

### Rule
Use `@wire` for read-only, reactive data fetching. Use imperative Apex for:
  - user-initiated actions (e.g., button clicks)
  - data mutations (create, update, delete)
  - controlled execution flows


## 3. Reactivity

### Rules

1. Do not use `@track` for primitive properties (string, number, boolean)
2. Do not use `@track` when updating objects or arrays by replacing their reference
3. Prefer immutable updates over direct mutation
4. Only use `@track` when deep mutations of objects or arrays are unavoidable

## 4. Event Communication

### Rule
Use custom events for communication from child to parent components. Use `@api` properties for parent to child communication.

### Guidelines
- Use lowercase event names (e.g., `save`, `recordchange`)
- Keep event payload (detail) minimal and structured





