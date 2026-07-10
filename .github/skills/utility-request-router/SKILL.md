---
name: utility-request-router
description: A reusable framework utility skill that scales execution. Use this tool whenever a task involves processing a large collection of items (files, endpoints, metadata items) that can be handled simultaneously in parallel. It runs the workers in isolation and executes a reducer script to safely compile their structured outputs back into a central state database.
---
# Concurrent Task Executor & State Reducer

## Capabilities
- **Parallel Spawning**: Maps individual batch items across local machine CPU cores.
- **Isolate & Collect**: Forces concurrent scripts to output single standalone transaction records to a staging area, completely eliminating file locks.
- **State Reduction**: Automatically merges, deduplicates, and commits data entries into a target `.json` file schema.

## Usage Schema (CLI Command Matrix)
To spin up a parallel batch parsing job, pass the worker wrapper, the graph reducer, the abstract file type, the explicit metadata type, and the target file list into the runner. Choose the exact multi-line command syntax that matches your current operating system shell:

### 1. PowerShell Environment (Windows)

```powershell
python scripts\generic_batch_runner.py `
  --worker "python scripts\utility_parse.py" `
  --reducer "python scripts\utility_graph_output.py" `
  --type "<fileType>" `
  --metadata "<metadata_or_object_type>" `
  --items "<comma_separated_file_paths>" `
  --state "workspace_state.json"
```

*Example for CPQ Quotes on Windows:*

```powershell
python scripts\generic_batch_runner.py `
  --worker "python scripts\utility_parse.py" `
  --reducer "python scripts\utility_graph_output.py" `
  --type "json" `
  --metadata "SBQQ__Quote__c" `
  --items "data\cpq_quotes_1.json,data\cpq_quotes_2.json" `
  --state "workspace_state.json"
```

### 2. Bash Environment (Linux / macOS / Git Bash)

```bash
python scripts/generic_batch_runner.py \
  --worker "python scripts/utility_parse.py" \
  --reducer "python scripts/utility_graph_output.py" \
  --type "<fileType>" \
  --metadata "<metadata_or_object_type>" \
  --items "<comma_separated_file_paths>" \
  --state "workspace_state.json"
```