---
name: utility-tooling-check
description: "A self-healing environment utility skill. It embeds all required Python modules and system binaries directly within its prompt workspace, enabling the agent to execute pre-flight health checks and automatically heal the runtime environment when execution errors occur."
---

# Utility Environment Validator Skill

## Embedded Requirements Matrix (Single Source of Truth)
The AI agent must ensure that the following packages and versions are active in the local runtime environment before launching any core orchestrators:

| Package / Binary Name | Minimum Version | Target Parser / Script Purpose | Criticality |
| :--- | :--- | :--- | :--- |
| `tree-sitter` | `>=0.21.0` | `tree_sitter_parser.py` (AST Code Parser) | **Blocker** |
| `tree-sitter-languages` | `>=1.10.0` | `tree_sitter_parser.py` (Pre-compiled Language Grammars) | **Blocker** |
| `simple-salesforce` | `>=1.12.0` | `execute-sf-data-load.md` (Live API and Python fallbacks) | High |
| `sf` (Salesforce CLI) | `Latest` | `execute-sf-data-load.md` (Live SOQL extraction & bulk uploads) | **Blocker** |

## Capabilities
- **Inlined Requirement Validation**: Eliminates external file lookups by storing the source configuration matrix directly inside the skill context.
- **Automated Dependency Recovery**: Dynamically executes package managers (`pip`) to install or upgrade missing modules on-demand without human intervention.
- **CLI Health Checks**: Verifies if necessary terminal command binaries (like `sf`) are globally mapped in the Windows `%PATH%` or Unix environment.

## Usage Schema (Windows PowerShell & Bash Commands)

### 1. Verification and On-Demand Installation of an Embedded Package
If a package from the matrix is missing, or if a specific script crashes with a `ModuleNotFoundError`, execute this command to force-install the package on-demand:

#### PowerShell Environment (Windows)
```powershell
python -m pip install "<package_name>==<minimum_version>"
```

*Example: Force-installing tree-sitter-languages on Windows:*
```powershell
python -m pip install "tree-sitter-languages>=1.10.0"
```

#### Bash Environment (Linux / macOS / Git Bash)
```bash
python -m pip install "<package_name>==<minimum_version>"
```

---

### 2. Live Verification of System CLI Binaries
To test if the Salesforce CLI binary is correctly installed and globally accessible by the agent session:

#### PowerShell Environment (Windows)
```powershell
Get-Command sf -ErrorAction SilentlyContinue
```

#### Bash Environment (Linux / macOS / Git Bash)
```bash
which sf
```

---

## Agent Execution Instructions

### Scenario A: Proactive Pre-Flight Check (Before Starting a Session)
1. **Scan Matrix**: Read the **Embedded Requirements Matrix** above.
2. **Execute Diagnostic Check**: For each Python package listed, run a silent import check (e.g., `python -c "import tree_sitter"`).
3. **Auto-Install Missing Items**: If any check fails, immediately execute the **On-Demand Installation Command** (Schema 1) using the package name and version from the matrix.
4. **Verify Salesforce CLI**: Run the **CLI Health Check** (Schema 2). If missing, halt execution and kindly instruct the user to install the Salesforce CLI system binary.

### Scenario B: Reactive Self-Healing Loop (After a Runtime Error)
1. **Analyze Error Output**: If any parser, router, or reducer script throws an error, inspect the `stderr` string.
2. **Detect Missing Module**: Look for signature exceptions such as `ModuleNotFoundError: No module named '<module_name>'` or `ImportError`.
3. **Match and Heal**: Cross-reference the missing module name with the Embedded Requirements Matrix, extract the correct package, and trigger the **On-Demand Installation Command** (Schema 1).
4. **Retry Pipeline**: Once the installation output returns a success state, clear your error buffer and immediately retry the original pipeline command from the orchestrator skill (`sf-metadata` or `sf-data`).
