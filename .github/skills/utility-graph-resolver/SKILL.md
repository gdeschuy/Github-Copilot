---
name: utility-graph-resolver
description: A framework optimization utility skill designed to prevent LLM context-window exhaustion in large repositories. It acts as an inspector for the central graph database (`workspace_state.json`), executing high-speed local graph-diffs to compute a list of discovered dependencies that have not yet been processed by the parser pipeline.
---

# Utility Graph Resolver Skill

## Capabilities
- **Context-Window Protection**: Abstractly filters megabytes of graph data down to a tiny, high-utility JSON array containing only the filenames that require processing.
- **Repository Path Matching**: Automatically scans the physical file system (`rglob`) to resolve loose dependency names (e.g., `QueryBuilder`) into exact relative file paths (e.g., `classes/QueryBuilder.cls`).
- **State Delta Calculation**: Identifies "Unresolved Edges"—relationships where a target file is referenced in code but does not yet exist as a completed Node in the state database.

## Usage Schema (CLI Command)
To request the current batch of unprocessed dependencies, invoke the resolver script with the path to the central state file and the root directory of the repository:

```bash
python scripts/utility_graph_resolver.py <state_file_path> [source_root]
```

### Example
```bash
python scripts/utility_graph_resolver.py "workspace_state.json" "./force-app/main/default"
```

### Expected Output Payload (`stdout`)
The tool will always return a clean, deduplicated JSON array of file paths. If the graph is fully resolved and complete, it returns an empty array:

```json
[
  "force-app/main/default/classes/QueryBuilder.cls",
  "force-app/main/default/classes/AccountTriggerHandler.cls"
]
```

## Agent Execution Instructions
1. **Call Post-Reduction**: Always invoke this skill *after* a parallel batch runner job has completed and the graph reducer has successfully committed its updates.
2. **Evaluate Wachtrij**: 
   - If the returned array contains file paths, immediately feed these paths back to the `analyse-sf-metadata` orchestrator to kick off the next parallel parsing batch.
   - If the returned array is empty (`[]`), the dependency tree is 100% complete. Stop the execution loop and present the final architectural analysis to the user.
