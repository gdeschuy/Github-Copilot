# AGENTS.md

> Be extremely concise. Sacrifice grammar for the sake of concision.

## Project Overview

The Salesforce dev repository groups all Barco Salesforce configuration together.

## Repository Structure

```
.
├── apexscripts/        # Anonymous Apex scripts
├── configdata/         # CPQ config data
├── instructions/       # Coding guidelines
├── scripts/            # Powershell scripts
├── specs/              # Business process specs
├── src/                # CPQ custom logic
├── swagger/            # API definitions
├── unpackaged/         # SFDX metadata

```
## Instruction Usage

- General code standards apply to all code
- Language-specific instruction files override general standards where applicable
- Only apply language-specific rules when working in that language

## Implementation Priority (follow in order)

1. Modify an existing implementation if the business function is the same and only needs adaptation.
2. Extend or overload an existing implementation only if the use case is identical and only the input shape differs.
3. Create a new, clearly named implementation if the use case or input model differs.

Never introduce flags or additional parameters to reuse an implementation. This counts as a different use case. If unsure, create a new implementation instead of extending.

## Core Development Principles

### DO

1. Keep a single source of truth: group business logic in one dedicated place at the highest appropriate abstraction level.
2. Search for existing implementations in the most relevant locations (same module, domain, or layer).
3. Keep changes minimal and scoped to the request.

### DO NOT

1. Do not run system commands (e.g. `sf force deploy`, delete operations, or similar) unless explicitly instructed to do so. Always ask for permission before executing if such commands are to be performed.
2. Do not commit or push directly to `main`.
3. Do not store or share secrets.
4. Generalize or merge different business cases into a single implementation.
5. Duplicate existing logic or configuration to add minor variations.
6. Introduce boolean flags or control parameters to switch behavior — create a new implementation instead.

## Design Constraints

- Method and component names must reflect a single, clear business intent.
- Do not reuse generic or ambiguous names for different behaviors.
- Place business logic in the appropriate layer; do not spread domain logic across utilities or low-level components.
- These constraints are mandatory and must always be followed.

## Search Strategy

- Prioritize searching by name, domain, and proximity (same class, folder, or feature).
- Expand search scope only if needed.
- Avoid full-repository scans unless necessary.

### Post-Change Checklist (always follow)

1. Identify impact (callers, references, integrations, and tests where relevant).
2. Update all affected usages (call sites, references, and integrations).
3. Update or create tests when functional behavior is added or changed.
4. Clean up obsolete logic.
5. Search for old names or patterns and ensure no references remain.
6. Validate consistency (no broken flows, outdated references, or mismatched logic).