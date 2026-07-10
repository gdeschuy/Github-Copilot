# Salesforce SKill Repository

## Operational Stages

The framework is structured into six decoupled operational stages, driven by a specialized library of AI Skills and automation utilities.

### 1. 📅 PLAN
Defines the technical scope, business boundaries, and operational constraints before any code orchestration begins.

#### Skills in this Section

| Skill Name | One-Line Description |
| :--- | :--- |
| `plan-get-requirements` | Extracts structured user stories, functional parameters, and acceptance criteria from raw text prompts. |

* **Explanation**: This stage acts as the intake gate. It ensures the AI fully understands the user's intent, the functional scope, and the architectural rules before triggering downstream data or code discovery workflows.

---

### 2. 🧠 ANALYSE
The core intelligence and discovery layer that interprets domain models and maps target structures.

#### Skills in this Section

| Skill Name | One-Line Description |
| :--- | :--- |
| `analyse-sf-metadata` | Orchestrates the recursive parsing loop of the codebase and parses Salesforce metadata based on reference schemas. |
| `analyse-sf-data` | Navigates multi-domain data relationships (Sales, CPQ, RLM, FSL) and crawls record lineages. |

* **Explanation**: The brain of the operation. These skills read your centralized configuration models (`references/*.json`) to dynamically guide workers to the correct file extensions, directories, and abstract classifications.

---

### 3. 🗺️ DESIGN
Translates analytical discoveries into highly performant system architectures and technical blueprints.

#### Skills in this Section

| Skill Name | One-Line Description |
| :--- | :--- |
| `design-sf-architecture` | Generates enterprise-grade technical designs, entity-relationship diagrams (ERDs), and class structure layouts. |

* **Explanation**: This layer bridges analysis and execution. It uses the gathered repository insights to model optimal code topologies and data relationships before a single line of code is compiled.

---

### 4. ⚙️ EXECUTE
The execution and generation engine that handles automated code authorship and transactional data deployment.

#### Skills in this Section

| Skill Name | One-Line Description |
| :--- | :--- |
| `execute-generate-apex` | Authors highly optimized, pattern-compliant Apex classes, triggers, and unit tests using method-level context. |
| `execute-generate-prompt` | Compiles advanced LLM prompt layouts, automatically embedding dynamic tokens and live data providers. |
| `execute-sf-data-load` | Extracts cloud datasets as local CSVs and executes dependency-aware, sequenced bulk cloud deployments. |

* **Explanation**: The proactive execution layer. These skills automate the creation of assets—writing code, composing system prompts, or deploying records sequentially based on calculated graph dependencies.

---

### 5. ⚡ OPTIMIZE
The review, evaluation, and quality assurance framework ensuring maximum efficiency and security compliance.

#### Skills in this Section

| Skill Name | One-Line Description |
| :--- | :--- |
| `optimize-review-code` | Performs deep static code analysis, catching governance limit violations, security vulnerabilities, and code smells. |
| `optimize-review-copilot` | Evaluates inline AI assistant suggestions to ensure they align with the repository's established code patterns. |
| `optimize-review-prompt` | Refines and token-optimizes prompt templates to maximize LLM instruction adherence and minimize costs. |

* **Explanation**: The safety net. These skills ensure that all generated code or data scripts adhere to strict enterprise quality metrics before they are committed to production environments.

---

### 6. 🛠️ UTILITY
The underlying cross-platform scripting workers that execute heavy computing, piping, and environment validation.

#### Skills in this Section

| Skill Name | One-Line Description |
| :--- | :--- |
| `utility-request-router` | Distributes lists of target files concurrently across machine CPU threads using thread-pool executors. |
| `utility-parse-file` | A generic wrapper routing source files to specialized Tree-Sitter, XML, JSON, or CSV parser scripts. |
| `utility-graph-output` | Captures parallel stdout streams in-memory and merges them atomically into the state file using MD5 hashes. |
| `utility-graph-resolver` | Runs high-speed local graph-diffs to compute the remaining queue of unresolved dependency paths. |
| `utility-tooling-check` | Executes pre-flight validation and self-healing pip recovery routines when environment exceptions occur. |

* **Explanation**: The foundational muscle. These skills are completely decoupled from business or platform logic. They are deterministic, cross-platform Python scripts (optimized for Windows PowerShell and Unix Bash) that handle the fast, parallel, and low-level heavy lifting.

## Future Roadmap

To transform this powerful pipeline into a truly autonomous, self-directing AI agent ecosystem, the following capabilities should be integrated next:

1. **Dynamic Schema-Drift Detection**: Automatic detection of custom field changes or API version upgrades in Salesforce to trigger on-demand rebuilds of the reference model JSON files.
2. **Graph-Augmented Code Generation (True GraphRAG)**: Injecting structural relationship contexts directly into code generation prompts to ensure new Apex classes automatically respect existing architecture, utility classes, and framework design patterns.