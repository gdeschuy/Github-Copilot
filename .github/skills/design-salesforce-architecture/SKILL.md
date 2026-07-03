---
name: design-salesforce-architecture
description: "Salesforce architecture and design standards for building scalable and maintainable solutions. Use this skill when planning and designing Salesforce solutions to ensure they adhere to best practices and architectural principles."
---
# Design and Architecture Standards

Determine the most lightweight and efficient solution that meets the business requirements.

## 1. No-Code Solutions

Always consider configrations first for simple requirements. Do not perform complex logic in formula fields or validation rules.

| Requirement | Best tool |
|---|---|
| Calculate a field value with no side effects | Formula field |
| Prevent a bad record save with a user message | Validation rule |
| Sum or count child records on a parent | Roll-up Summary field |

## 2. Low-Code Solutions

| Requirement | Best tool |
|---|---|
| Guide a user through a multi-step data entry wizard | Screen Flow |
| Update related records immediately after a save | Record-Triggered Flow (After-Save) |
| Modify field values on the triggering record before it hits the database | Record-Triggered Flow (Before-Save) |
| Run complex logic on a daily or weekly schedule | Schedule-Triggered Flow |

## 3. Pro-Code Solutions

| Requirement | Best tool |
|---|---|
| Execute real-time integrations with external APIs | Apex Callouts (with Named Credentials) |
| Process hundreds of thousands of records asynchronously | Batch Apex |
| Implement strict transaction control with partial save rollbacks | Apex Savepoints / Triggers |
| Build high-performance, completely custom user interfaces | Lightning Web Components (LWC) + Apex Controllers |

### 4. Agentic Solutions

Leverage autonomous agents to handle unstructured data, reasoning, and natural language processing tasks.

### Agentforce Agents

| Requirement / Use Case | Best Tool |
|---|---|
| Execute multi-turn conversations and resolve customer service inquiries autonomously | Agentforce Service Agent |
| Support internal employees with real-time CRM updates, task routing, and proactive data insights | Agentforce Sales / Ops Agent |

### Agentforce Prompt Templates

| Prompt Template Type | Best Tool For | Applicable Use Cases |
|---|---|---|
| Flex Template | Generating highly customized text based on any specific inputs or multiple object records. | • Summarizing case histories.<br>• Creating tailored product pitches.<br>• Analyzing unstructured text fields. |
| Email Template | Crafting personalized, context-aware email communications for customers or prospects. | • Generating sales outreach emails.<br>• Drafting custom follow-up notes for support cases. |
| Field Generation Template | Automatically populating or updating a single field with AI-generated data. | • Summarizing meeting transcripts into a single text field.<br>• Auto-generating product or case descriptions. |
| Record Summary Template | Providing rapid, high-level summaries of a specific record and its related lists. | • Generating account health summaries before client calls.<br>• Creating executive summaries of complex opportunities. |