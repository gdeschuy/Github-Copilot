---
name: execute-sf-data-load
description: "A live data infrastructure skill. It enables the AI agent to execute high-speed SOQL queries directly against a live Salesforce environment and push data updates (inserts, updates, upserts) back to the cloud using the native Salesforce CLI (`sf`). It streams live cloud records straight into the graph pipeline via standard output (`stdout`)."
---

# Utility Salesforce Data Load Skill

## Description

## Capabilities
- **Live Cloud Extraction**: Bypasses local data file limits by querying live sandboxes or production environments in real-time.
- **Unified Pipeline Piping**: Returns query data as standardized JSON objects via `stdout`, allowing immediate integration into `utility-graph-output`.
- **Transactional Cloud Writing**: Supports both single-record patches and multi-core bulk inserts/updates using local JSON/CSV files.

## Usage Schema (Windows PowerShell & Bash Commands)

### 1. Querying Live Data via SOQL (Piped straight into the Graph)
To extract live records, construct a SOQL query, enforce the `--json` flag, and pipe it directly into the graph reducer:

```powershell
sf data query --query "SELECT Id, Name, <lookup_field> FROM <SObject> WHERE <Condition>" --json | python scripts\utility_graph_output.py "workspace_state.json" "<SObject>"
```

*Example: Live query for CPQ Quote Lines on Windows:*
```powershell
sf data query --query "SELECT Id, Name, SBQQ__Quote__c, SBQQ__Product__c FROM SBQQ__QuoteLine__c WHERE SBQQ__Quote__c = 'a0Q8000000Eg123'" --json | python scripts\utility_graph_output.py "workspace_state.json" "SBQQ__QuoteLine__c"
```

### 2. Updating Live Data using local JSON files
To push architectural updates or data corrections back to Salesforce from a local JSON payload, trigger the bulk insertion worker:

```powershell
sf data record insert bulk --sobject <SObject> --file <local_file_path>
```

*Example: Pushing updated FSL Work Orders to Salesforce:*
```powershell
sf data record insert bulk --sobject WorkOrder --file data\fsl_work_orders.json
```

## Agent Execution Instructions
1. **Identify Source Preference**: Check if the user prompt requires a "live cloud analysis" or a "local repository analysis".
2. **Execute Extract Loop**: If live, use the **SOQL Query Command** above instead of `utility_parse.py`. Pipe the resulting live stream directly into `utility_graph_output.py`.
3. **Execute Load Action**: If the user approves an architectural or data update, compile the required fields into a clean JSON/CSV format and execute the **Bulk Update Command** to sync the repository back to the Salesforce cloud.