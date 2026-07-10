---
name: utility-graph-output
description: A framework data-reduction utility skill. It acts as the final step (the Reducer) in the metadata processing pipeline. This skill consumes normalized parser JSON payloads directly from standard input (`stdin`), transforms them into standardized graph network components (Nodes and Edges), and commits them atomically to a centralized workspace database.
---

# Utility Graph Output Skill

## Capabilities
- **Piped Stream Consumption**: Reads data directly from `sys.stdin`, allowing it to be chained directly to the output of `utility-parse` via terminal piping (`|`).
- **Deterministic Edge Hashing**: Enforces a process-independent MD5 hashing mechanism on relationships to prevent duplicate entries, regardless of execution order.
- **Atomic Operations**: Writes changes to a temporary file before swapping it with the master database, completely eliminating data loss or file corruption risks during high-frequency parallel updates.

## Graph Database Schema (`workspace_state.json`)
The committed data will always adhere to this structure, which can be easily inspected by the orchestrator skill to detect unresolved dependencies:

```json
{
  "nodes": [
    {
      "id": "force-app/main/default/classes/AccountService.cls",
      "name": "AccountService.cls",
      "type": "ApexClass",
      "parser": "java"
    }
  ],
  "edges": [
    {
      "id": "e4d9b4b0e51322fa1d5966c5d9f00171",
      "source": "force-app/main/default/classes/AccountService.cls",
      "target": "QueryBuilder",
      "relationship": "instantiation"
    }
  ]
}
```

## Usage Schema (CLI Command via Pipeline)
To integrate data, execute this script by providing the path to the central graph file and the explicit `metadata_type` provided by the orchestrator. Always chain this command right after the parser utility using a pipe (`|`):

```powershell
python scripts\utility_parse.py <file_type> <file_path> | python scripts\utility_graph_output.py <state_file_path> <metadata_type>
```

```bash
python scripts/utility_parse.py <file_type> <file_path> | python scripts/utility_graph_output.py <state_file_path> <metadata_type>
```

### Examples

**1. Processing and Integrating an Apex Class**
```powershell
python scripts\utility_parse.py "code" "force-app\main\default\classes\AccountService.cls" | python scripts\utility_graph_output.py "workspace_state.json" "ApexClass"
```

```bash
python scripts/utility_parse.py "code" "force-app/main/default/classes/AccountService.cls" | python scripts/utility_graph_output.py "workspace_state.json" "ApexClass"
```

**2. Processing and Integrating a Custom Object Configuration**
```powershell
python scripts\utility_parse.py "xml" "force-app\main\default\objects\Account.object" | python scripts\utility_graph_output.py "workspace_state.json" "CustomObject"
```

```bash
python scripts/utility_parse.py "xml" "force-app/main/default/objects/Account.object" | python scripts/utility_graph_output.py "workspace_state.json" "CustomObject"
```

## Agent Execution Instructions
1. **Combine Utilities**: Do not run the parser and the graph manager as two separate isolated steps. Always chain them into a single command using the terminal pipe (`|`) character.
2. **Inject Context**: Pass the `<metadata_type>` parameter (e.g., `ApexClass`, `CustomObject`) exactly as instructed by the `analyse-sf-metadata` orchestrator.
3. **Verify Commit**: Once the pipeline command returns a success log, consider the node and its immediate dependencies safely updated in the central state file.