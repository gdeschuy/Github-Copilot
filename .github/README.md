# Salesforce Skill Repository

## Operational Stages

The framework is structured into seven decoupled operational stages, driven by a specialized library of AI Skills and automation utilities.

### 1. 💬 DISCOVER
Acts as the conversational interaction layer, listening to the user to extract, clarify, and align on requirements before downstream processing begins.

#### Skills in this Section

| Skill Name | One-Line Description |
| :--- | :--- |
| `discover-get-requirements` | Engages in a clarifying dialogue to extract structured user stories, functional parameters, and acceptance criteria from raw text prompts. |

* **Explanation**: This stage acts as the interactive intake gate. Instead of jumping straight into code or data, the AI acts as a conversational partner. It probes the user's intent, resolves ambiguities, and establishes the functional scope and business boundaries before any analytical or design workflows are triggered.

---

### 2. 🔍 ANALYSE
The discovery and inventory layer that maps the existing Salesforce setup to understand what is already available.

#### Skills in this Section

| Skill Name | One-Line Description |
| :--- | :--- |
| `analyse-sf-metadata` | Scans and dissects the existing codebase to inventory the current metadata structure and active configurations. |
| `analyse-sf-data` | Maps existing multi-domain data relationships (Sales, CPQ, RLM, FSL) and crawls record lineages to understand the live situation. |

* **Explanation**: This stage acts as an X-ray of the current environment. Before any new solution is designed, these skills read the centralized configuration models (`references/*.json`) to dynamically guide workers through existing directories, file extensions, and data paths. The output is a crystal-clear picture of the current technical status quo.

---

### 3. 🗺️ DESIGN
Translates analytical discoveries into a concrete technical blueprint, working out the optimal solution architecture before implementation begins.

#### Skills in this Section

| Skill Name | One-Line Description |
| :--- | :--- |
| `design-sf-architecture` | Synthesizes requirements and metadata insights to architect the new solution topology, selecting the path of least customization (Configuration vs. Pro-Code). |

* **Explanation**: This layer bridges analysis and execution. It uses the gathered repository insights to actively model new code topologies, data relationships, and framework patterns, producing an exact architectural blueprint before a single line of code is authored.

---

### 4. 🏗️ BUILD
The build and generation engine that handles automated code authorship, template compilation, and localized validation preparation.

#### Skills in this Section

| Skill Name | One-Line Description |
| :--- | :--- |
| `build-generate-apex` | Authors highly optimized, pattern-compliant Apex classes, triggers, and unit tests using method-level context. |
| `build-generate-prompt` | Compiles advanced LLM prompt layouts, automatically embedding dynamic tokens and live data providers. |
| `build-sf-data-load` | Extracts cloud datasets as local CSVs and executes dependency-aware, sequenced bulk cloud deployments. |

* **Explanation**: The proactive build layer. These skills automate the creation of assets—writing code, composing system prompts, or staging records sequentially based on calculated graph dependencies and local validations.

---

### 5. 🚀 RELEASE
The deployment and activation framework responsible for pushing validated metadata packages into live environments.

#### Skills in this Section

| Skill Name | One-Line Description |
| :--- | :--- |
| `release-sf-metadata` | Deploys validated Salesforce metadata to the target environment using the Salesforce CLI. |

* **Explanation**: The deployment gate. This stage handles the transactional release of code and metadata to target Salesforce orgs once all upstream compilation and verification stages are passed.

---

### 6. ⚡ OPTIMIZE
The review, evaluation, and quality assurance framework ensuring maximum efficiency and security compliance.

#### Skills in this Section

| Skill Name | One-Line Description |
| :--- | :--- |
| `optimize-review-code` | Performs deep static code analysis, catching governance limit violations, security vulnerabilities, and code smells. |
| `optimize-review-copilot` | Evaluates inline AI assistant suggestions to ensure they align with the repository's established code patterns. |
| `optimize-review-prompt` | Refines and token-optimizes prompt templates to maximize LLM instruction adherence and minimize costs. |

* **Explanation**: The safety net. These skills ensure that all generated code or data scripts adhere to strict enterprise quality metrics before they are committed to production environments.

---

### 7. 🛠️ UTILITY
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