---
name: utility-request-router
description: A reusable framework utility skill that scales execution. Use this tool whenever a task involves processing a large collection of items (files, endpoints, metadata items) that can be handled simultaneously in parallel. It runs the workers in isolation and executes a reducer script to safely compile their structured outputs back into a central state database.
---
# Concurrent Task Executor & State Reducer

## Capabilities
- **Parallel Spawning**: Maps individual batch items across local machine CPU cores.
- **Isolate & Collect**: Forces concurrent scripts to output single standalone transaction records to a staging area, completely eliminating file locks.
- **State Reduction**: Automatically merges, deduplicates, and commits data entries into a target `.json` file schema.

## Usage Schema (CLI command)
To invoke a generic batch job, pass the worker target script, the file list parameter, the temporary staging folder, and the final state file location:

```powershell
python scripts\generic_batch_runner.py `
  --worker "python scripts\utility_parse.py" `
  --reducer "python scripts\utility_graph_output.py" `
  --items "force-app\main\default\classes\AccountService.cls,force-app\main\default\classes\QueryBuilder.cls" `
  --staging ".github\task_staging\" `
  --state "workspace_state.json"
```

```bash
python scripts/generic_batch_runner.py \
  --worker "python scripts/my_parser_worker.py" \
  --items "file1.cls,file2.cls,file3.cls" \
  --staging ".github/task_staging/" \
  --state "workspace_state.json"
```