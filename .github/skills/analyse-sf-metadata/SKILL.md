---
name: analyse-sf-metadata
description: The primary domain-expert and orchestration skill for Salesforce codebase analysis. It dynamicallly loads repository structural rules from a central configuration file, maps Salesforce metadata files to abstract file types, and manages the execution loop required to map complete dependency graphs without exhausting the AI context-window.
---

# Analyse Salesforce Metadata Orchestrator Skill

## Configuration Source
Before executing any analysis or routing decisions, the AI **must** read the metadata rules and directory mappings directly from the master configuration file located at:
`references/metadata-model.json`

The AI will parse this JSON file to extract the `salesforceMetadata` array containing the `type`, `directory`, `extension`, and `fileType` mappings at runtime.

## Capabilities
- **Dynamic Rule Loading**: Relies completely on `references/metadata-model.json` for routing, ensuring zero code or prompt changes when metadata structures are updated.
- **Pipeline Orchestration**: Generates parallel execution statements for the `utility-request-router` and chains the `utility-parse` and `utility-graph-output` streams.
- **Recursive Dependency Discovery**: Leverages external graph solvers to incrementally crawl nested architectures without loading raw codebase states into memory.

## Execution Lifecycle (The Dependency Loop)

When a user requests an analysis (e.g., *"Analyseer Apex klasse AccountService.cls"*), the AI must strictly follow this multi-step state machine:

### Step 0: State Reset (Environment-Aware)
To ensure old analysis data does not corrupt or pollute the new graph context, the AI **must** reset the central `workspace_state.json` database to an empty graph schema before launching any parser jobs. Execute the matching command based on your current terminal environment:

```powershell
'{"nodes": [], "edges": []}' | Out-File -FilePath "workspace_state.json" -Encoding utf8
```

```bash
echo '{"nodes": [], "edges": []}' > workspace_state.json
```

### Step 1: Configuration Loading & Discovery
1. Read and load the rules inside `references/metadata-model.json`.
2. Inspect the file extension of the target input file.
3. Locate the matching metadata rule block within the loaded JSON configuration.
4. Extract the abstract `fileType` (e.g., `code`) and the metadata `type` string (e.g., `ApexClass`).

### Step 2: Formulate & Fire the Pipeline
Construct the parallel batch runner command, passing the discovered <fileType> and <type> variables directly into their respective flags. Run this concurrently for all files in the current batch:

For Windows PowerShell:

```powershell
python scripts\generic_batch_runner.py --worker "python scripts\utility_parse.py" --reducer "python scripts\utility_graph_output.py" --type "<fileType>" --metadata "<type>" --items "<comma_separated_file_paths>" --state "workspace_state.json"
```

*Example command generated for AccountService (Windows):*

```powershell
python scripts\generic_batch_runner.py --worker "python scripts\utility_parse.py" --reducer "python scripts\utility_graph_output.py" --type "code" --metadata "ApexClass" --items "force-app\main\default\classes\AccountService.cls" --state "workspace_state.json"
```

For Linux / macOS / Git Bash:

```bash
python scripts/generic_batch_runner.py --worker "python scripts/utility_parse.py" --reducer "python scripts/utility_graph_output.py" --type "<fileType>" --metadata "<type>" --items "<comma_separated_file_paths>" --state "workspace_state.json"
```

*Example command generated for AccountService (Bash):*

```bash
python scripts/generic_batch_runner.py --worker "python scripts/utility_parse.py" --reducer "python scripts/utility_graph_output.py" --type "code" --metadata "ApexClass" --items "force-app/main/default/classes/AccountService.cls" --state "workspace_state.json"
```

### Step 3: Check the Unresolved Queue
Immediately after executing the pipeline, invoke the `utility-graph-resolver` to compute the next dependency delta:

```powershell
python scripts\utility_graph_resolver.py "workspace_state.json" ".\force-app\main\default"
```

```bash
python scripts/utility_graph_resolver.py "workspace_state.json" "./force-app/main/default"
```

### Step 4: Evaluate & Recurse
Inspect the stdout JSON array returned by the resolver:
- **Scenario A (Array is NOT empty)**: The array contains outstanding downstream files (e.g., `["classes/QueryBuilder.cls"]`). Clear your current execution buffer, set this new array as your next target batch, and **immediately return to Step 1**.
- **Scenario B (Array is EMPTY `[]`)**: The dependency graph is completely mapped out. Proceed to Step 5.

### Step 5: Final Delivery
Generate a summary report for the user based *only* on the finalized tree or confirmation metrics. Inform the user that the workspace dependency graph has been successfully built.