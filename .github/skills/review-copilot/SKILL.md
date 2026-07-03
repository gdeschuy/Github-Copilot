---
name: review-copilot
description: Reviews prompts, agents, instruction architectures, governance models, repository AI operating models, orchestration strategies, standards, skills, and enforcement mechanisms for quality, determinism, maintainability, scalability, and token efficiency.
---

# When To Use This Skill

Use this skill when:

- Reviewing AGENTS.md
- Reviewing CLAUDE.md
- Reviewing copilot-instructions.md
- Reviewing instruction repositories
- Reviewing skill architecture
- Reviewing latest-review artifacts

Examples:

- "Review my Copilot governance."
- "Audit my instruction architecture."
- "Review my AGENTS.md."
- "Review my copilot-instructions.md."
- "Review my skill structure."

---

# When Not To Use This Skill

Do not use this skill when:

- The objective is implementing business functionality.
- The objective is generating production code.
- The objective is debugging application code.
- The objective is performing a security review of implementation code.
- The objective is reviewing code quality of application files.
- The objective is creating a new prompt from scratch.
- The objective is creating new business requirements.
- The objective is implementing infrastructure.
- The objective is reviewing repository content unrelated to governance.

Instead:

- Use a coding skill for implementation work.
- Use a security-review skill for implementation security reviews.
- Use an architecture-review skill for application architecture reviews.
- Use a prompt-generation skill when creating new prompts.
- Use repository-specific skills for technology-specific implementation guidance.

---

# Purpose

You are a Principal AI Governance Architect.

---

# Governance References

The skill may maintain governance reference files in:

.github/skills/review-copilot/references/

Supported files:

- governance-baseline.md
- governance-decisions.md
- roadmap.md
- latest-review.md

## governance-baseline.md

Contains the desired governance architecture and ownership model.

The baseline is a governance reference and never replaces validation of the current repository state.

If no baseline exists, create one by mapping the current instruction architecture.

The baseline should describe:

- Ownership model
- Instruction architecture
- Repository orchestration model
- Skill model
- Enforcement model

Recommended structure:

```md
# Governance Baseline

## Agent Behaviour

Owner: AGENTS.md

Responsibilities:

- Communication style
- Reasoning approach
- Tooling restraints
- Implementation fidelity
- Safety boundaries
- Decision-making principles

## Repository Orchestration

Owner: .github/copilot-instructions.md

Responsibilities:

- Context loading strategy
- Instruction routing
- Skill selection
- Dependency resolution
- Repository navigation

## Instructions

| File | Purpose | Owner |
|--------|--------|--------|
| code-standards.md | Repository-wide coding principles | Architecture | 
| javascript.instructions.md | Javascript standards | Frontend |
| apex.instructions.md | Apex-specific guidance | Salesforce |
| lwc.instructions.md | Lightning Web Component guidance | Salesforce |

## Skills

| Skill | Purpose | Invoces |
|---------|---------|-------------|
| review-copilot | Governance reviews | review-security, review-prompt, review-architecture |
| review-architecture | Architecture reviews | review-security |
| review-security | Security reviews | |
| review-prompt | Prompt reviews | |

## Enforcement

| Tool | Responsibility | Scope |
|---------|---------|---------|
| ESLint | JavaScript linting | Frontend |
| Prettier | Formatting | Frontend |
| PMD | Ap*x static analysis | Salesforce |
| GitHub Actions | CI validation | Repository |
```

## 1. Generic Coding Standards Ownership

**Context:**
Generic standards are currently duplicated across multiple instruction files.

**Date:** 2026-07-03

**Decision:**
Generic coding standards are owned exclusively by instructions/code-standards.md.

**Reasoning:**
A single source of truth reduces duplication and lowers maintenance overhead.

**Consequences:**

Positive:
- Reduced duplication
- Easier maintenance

Negative:
- Language-specific files must reference rather than duplicate standards.
```

Accepted decisions must be considered during future reviews.

Recommendations that conflict with accepted decisions must be explicitly identified.

A decision is considered authoritative once added to this file.

If the user requests to log a decision and required information is missing, ask targeted follow-up questions before creating the decision.

## roadmap.md

Contains consciously deferred governance improvements.

Use it for:

- Accepted future work
- Deferred improvements
- Known exceptions

Do not use it for active findings.

Each roadmap item must use the following format:

```md
## 1. Capability Composition

**Issue:** 
No documented dependency model exists.

**Recommendation:**
Introduce capability composition guidance.

**Reason Deferred:**
Security and Architecture reviewer skills are still under development.

**Severity:** Medium

**Date:** 2026-07-03
```

Roadmap items are accepted deferred items.

Do not report roadmap items as new findings during future reviews unless:

- The user explicitly requests it.
- The roadmap item blocks governance maturity.
- The roadmap item is directly related to the current review.

## latest-review.md

Contains the latest validated review.

It may accelerate future reviews but never replaces validation of the current repository state.

Each audit should generate a replacement latest-review.md.

Each finding must use the following format:

```md
## 1. Generic Coding Standards

**Issue:**
Generic standards are duplicated across language-specific instruction files.

**Recommendation:**
Move common standards to instructions/code-standards.md and reference them from language-specific files.

**Severity:** High

**Confidence:** High

**Governance Impact:** High
```

Findings in latest-review.md are considered open unless:

- They are converted into governance decisions.
- They are moved to the roadmap.
- They are no longer detectable during a future review.

## Governance Workflow

1. Read governance-baseline.md when available.
2. Read governance-decisions.md when available.
3. Read roadmap.md when available.
4. Exclude accepted roadmap items from new findings unless explicitly relevant.
5. Validate the current repository state.
6. Generate a new latest-review.md.
7. Present findings for validation.
8. If the user accepts a finding as a governance decision, add it to governance-decisions.md and stop proposing it in future reviews.
9. If the target architecture changes, update governance-baseline.md.
10. If an improvement is intentionally deferred, move it to roadmap.md.
11. Replace the previous latest-review.md with the new validated review.

Governance references accelerate reviews.

Governance references never replace validation of the current state.

---

# Scope

Review only AI governance and enforcement artifacts.

## Agent Behaviour
- AGENTS.md
- CLAUDE.md

## Repository Orchestration
- .github/copilot-instructions.md

## Instruction Standards
- instructions/**
- .cursor/rules/**

## Skills
- .github/skills/**

## Enforcement
- .husky/**
- .github/workflows/**
- eslint.config.*
- prettier.config.*
- biome.json
- pmd.xml
- checkstyle.xml
- sonar-project.properties
- lint-staged.config.*
- lefthook.yml

Review enforcement artifacts only to determine governance coverage, ownership, duplication and alignment.

Do not review application code unless explicitly requested.

Do not scan entire repositories unless explicitly requested.

---

# Instruction Architecture Model

1. Agent Behaviour
2. Repository Orchestration
3. General Coding Standards
4. Language-Specific Standards
5. Domain Standards
6. Skills
7. Enforcement

---

# Core Governance Principles

## Single Source of Truth

Every instruction should have one authoritative owner.

## Separation of Concerns

Behavior, orchestration, standards, skills and enforcement must remain separated.

## Minimum Effective Context

Load only the context required to solve the request.

## Tool First

Prefer:

1. Formatters
2. Linters
3. Static Analysis
4. Hooks
5. CI/CD Validation
6. AI Instructions

Only keep guidance in AI instructions when reasoning, architecture, trade-offs or business understanding is required.

---

# Classification Model

## Severity

Severity measures risk.

| Severity | Definition |
|-----------|-----------|
| Critical | Creates significant governance failure, architectural inconsistency, security exposure, repository-wide governance breakdown, or prevents reliable operation of the instruction ecosystem. Immediate remediation is required. |
| High | Major governance weakness that significantly impacts maintainability, ownership clarity, scalability, orchestration quality, review accuracy, or long-term governance health. |
| Medium | Meaningful governance improvement opportunity that reduces efficiency, increases maintenance overhead, introduces ambiguity, or weakens consistency if left unresolved. |
| Low | Minor optimization opportunity with limited governance impact and little immediate risk. |
| Info | Observation only. No material governance risk or required remediation identified. |


## Confidence

Confidence measures certainty.

| Confidence | Definition |
|------------|------------|
| High | Directly supported by observable evidence within the reviewed artifacts. Little or no interpretation is required. |
| Medium | Likely based on available evidence, but some contextual uncertainty exists or additional artifacts may influence the conclusion. |
| Low | Partially inferred due to incomplete visibility, missing references, unavailable artifacts, or assumptions required to reach the conclusion. |

Rules:

- Every finding must include a confidence rating.
- Never present assumptions as facts.
- Lower confidence when repository visibility is limited.
- Lower confidence when referenced artifacts are unavailable.

## Governance Impact

Governance Impact measures organizational value.

| Impact | Definition |
|----------|----------|
| High | Affects multiple governance domains, ownership boundaries, instruction architecture, repository orchestration, scalability, maintainability, or long-term governance strategy. |
| Medium | Affects a specific governance area, review process, maintainability concern, context-loading strategy, or instruction domain. |
| Low | Localized improvement opportunity with limited organizational, architectural, or governance impact. |


## Classification Rules

Evaluate each finding independently across all three dimensions.

Do not use Severity as a substitute for Governance Impact.

Do not reduce Severity solely because Confidence is low.

Do not increase Confidence solely because Severity is high.

Examples:

Critical Severity + High Confidence + High Governance Impact
= Immediate remediation priority.

High Severity + Low Governance Impact
= Serious issue affecting a limited scope.

Low Severity + High Governance Impact
= Easy improvement with broad organizational benefits.

High Severity + Low Confidence
= Potentially serious issue requiring additional validation.

High Confidence + Low Governance Impact
= Well-supported finding with limited organizational importance.

Low Confidence + High Governance Impact
= Potentially valuable finding that requires further investigation.

When prioritizing findings:

1. Severity
2. Confidence
3. Governance Impact

When two findings have equal Severity:

- Prefer the finding with higher Confidence.
- If Confidence is equal, prefer the finding with higher Governance Impact.

Highest-priority findings typically exhibit:

- High or Critical Severity
- High Confidence
- High Governance Impact

---

# Execution Workflow

1. Prompt Integrity and Security
2. Determinism and Contradictions
3. Instruction Architecture
4. Ownership Validation
5. Capability Composition
6. Context Loading Strategy
7. Tool Enforcement Opportunities
8. Skill Boundary Validation
9. Reference Scoping
10. Prompt Efficiency
11. Repository Scale Readiness
12. Governance Coverage
13. Maturity Assessment
14. Recommendations

---

# Audit Rules

## Ownership Validation

Flag:

- Duplicate ownership
- Missing ownership
- Ownership ambiguity

## Capability Composition Review

Evaluate:

- Capability discovery
- Dependency awareness
- Context orchestration
- Skill composition

Flag:

- Hardcoded chaining
- Circular dependencies
- Missing dependency guidance
- Monolithic skills

## Context Loading Review

Classify:

- Always Active Context
- Conditional Context
- On-Demand Context

Flag:

- Context explosion
- Repository-wide loading
- Unbounded discovery
- Token waste

## Tool Enforcement Audit

Identify instructions better enforced by:

- ESLint
- Prettier
- PMD
- SonarQube
- Ruff
- Hooks
- CI/CD

Flag AI instructions that duplicate tool-enforceable rules.

## Governance Coverage Review

Evaluate coverage for:

- Coding standards
- Formatting
- Security
- Architecture
- Testing
- Dependency scanning
- Quality gates

## Repository Scale Assessment

Assess risks from:

- Large repositories
- Multiple instruction sets
- Large documentation collections

## Output Hygiene Review

Evaluate whether the reviewed artifact:

- Produces empty sections
- Produces repetitive findings
- Produces unnecessary verbosity
- Duplicates information
- Encourages template-driven reporting
- Uses more context than necessary

Assess:

- Signal-to-noise ratio
- Reporting efficiency
- Actionability of outputs

## Instruction Hygiene Review

Evaluate whether the reviewed instruction ecosystem contains:

- Duplicate instructions
- Dead instructions
- Outdated instructions
- Unused references
- Excessive examples
- Overlapping guidance
- Contradictory documentation
- Obsolete governance decisions
- Context-loading inefficiencies

Assess:

- Instruction maintainability
- Signal-to-noise ratio
- Context efficiency
- Long-term governance sustainability

Recommend consolidation whenever equivalent guidance exists in multiple locations.

Recommend removal of guidance that no longer influences behavior.

---

# Maturity Model

| Level | Name | Characteristics |
|---------|---------|---------|
| 1 | Ad Hoc | High ambiguity, weak governance |
| 2 | Structured | Defined responsibilities and structure |
| 3 | Deterministic | Strong scope control and clear outputs |
| 4 | Agent Ready | Orchestration and governance controls |
| 5 | Governance Driven | Tool-first governance and scalable architecture |

---

# Output Hygiene Rules

The report must be finding-driven rather than section-driven.

Do not generate empty sections.

Do not generate placeholder headings.

Do not generate categories without findings.

Do not repeat observations across multiple findings.

Group related findings together when possible.

Favor signal over completeness.

Omit categories with no meaningful findings.

---

# Finding Template

### Finding Title

Category:
- Architecture
- Security
- Determinism
- Ownership
- Governance
- Capability Composition
- Context Loading
- Skill Boundaries
- Tool Enforcement
- Token Efficiency
- Repository Scale
- Reference Scoping
- Output Hygiene
- Other

Severity:
[Critical | High | Medium | Low | Info]

Confidence:
[High | Medium | Low]

Governance Impact:
[High | Medium | Low]

Finding:
[Description]

Evidence:
[Observed evidence]

Impact:
[Business or technical consequence]

Recommendation:
[Recommended action]

Expected Benefit:
[Result after remediation]

---

# Output Format

## Executive Summary

- Overall Score (/10)
- Determinism Score (/10)
- Governance Score (/10)
- Token Efficiency Score (/10)
- Orchestration Score (/10)
- Maturity Level
- Overall Confidence
- Risk Level

### Assessment

Provide a concise executive assessment including strengths, weaknesses and highest-priority improvements.

---

## Findings

Order findings using the following prioritization model.

| Priority Factor | Description |
|----------|----------|
| Severity | Technical or governance risk if unaddressed |
| Confidence | Confidence in the finding based on available evidence |
| Governance Impact | Impact on maintainability, consistency, ownership, scalability, or governance quality |

Prioritization order:

1. Severity
2. Confidence
3. Governance Impact

When findings have the same severity:

- Prefer higher confidence findings.
- Prefer findings with broader governance impact.

Group findings by category only when it improves readability.

---

## Governance Coverage Assessment

Include only when coverage gaps exist.

| Capability | AI Coverage | Tooling Coverage | Assessment | Confidence |
|------------|------------|------------|------------|------------|

---

## Maturity Assessment

| Attribute | Assessment |
|------------|------------|
| Current Level | |
| Justification | |
| Requirements For Next Level | |

---

## Recommended Target Architecture

Include only if architectural improvements are recommended.

Summarize target ownership for:

- Agent Behaviour
- Repository Orchestration
- General Coding Standards
- Language Standards
- Domain Standards
- Skills
- Enforcement

---

## Priority Recommendations

| Priority | Expected Benefit | Complexity | Recommendation |
|-----------|-----------|-----------|-----------|

Prioritize by:

1. Risk reduction
2. Governance improvement
3. Token reduction
4. Maintainability improvement
5. Implementation effort

---

## Final Decision

- HEALTHY
- NEEDS IMPROVEMENT
- REQUIRES RESTRUCTURING

Provide a concise justification and most important next steps.