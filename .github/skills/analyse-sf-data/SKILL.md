---
name: analyse-sf-data
description: The primary domain-expert and orchestration skill for Salesforce record data-lineage and entity relationship analysis. It dynamically loads database schema rules from a central data model configuration, maps Foreign Key relationships (Parent/Child lookups) across local data exports, and manages the execution loop required to build transactional data graphs without exhausting the AI context-window.
---

# Analyse Salesforce Data Orchestrator Skill

## Description

## Configuration & Domain Mapping Matrix
When executing an analysis, the AI must inspect the requested target object, match it to its respective functional domain in the table below, and load that specific configuration file from the `references/` directory:

| Salesforce Domain | Target Configuration File | Core Object Examples |
| :--- | :--- | :--- |
| **Sales** | `references/sales-data-model.json` | `Account`, `Contact`, `Lead`, `Opportunity` |
| **Service** | `references/service-data-model.json` | `Case`, `KnowledgeArticle`, `WorkOrder` |
| **CPQ** | `references/cpq-data-model.json` | `SBQQ__Quote__c`, `SBQQ__QuoteLine__c`, `SBQQ__ProductOption__c` |
| **Field Service (FSL)** | `references/fsl-data-model.json` | `ServiceAppointment`, `AssignedResource`, `OperatingHours` |
| **Revenue (RLM)** | `references/rlm-data-model.json` | `SalesOrder`, `Pricebook`, `RevenueTransaction` |

The AI will parse this JSON file to extract the `salesforceDataModel` array containing the target objects, their physical `sourceFile` paths, and their relational foreign keys at runtime.

---

## Capabilities
- **Data Schema Mapping**: Resolves lookups, Master-Detail properties, and Parent-to-Child data paths automatically at runtime.
- **Incremental Data Crawling**: Chains the `JsonParser` and graph reduction tools to capture records and their specific relationship edges dynamically.
- **Context Protection**: Isolates massive raw database records within deterministic python workers, returning only refined network state deltas back to the orchestrator.

---

## Execution Lifecycle (The Data Dependency Loop)

When a user requests a data analysis session (e.g., *"Breng de data-graph in kaart voor Account record ACC_123"*), the AI must strictly follow this multi-step state machine:

### Step 0: State Reset (Environment-Aware)
To ensure old data graphs do not pollute the new record analysis session, the AI **must** reset the central `workspace_state.json` database to an empty graph schema before launching any data parsing jobs. Execute the matching command based on your current terminal environment:

#### PowerShell Environment (Windows)
```powershell
'{"nodes": [], "edges": []}' | Out-File -FilePath "workspace_state.json" -Encoding utf8
```

#### Bash Environment (Linux / macOS / Git Bash)
```bash
echo '{"nodes": [], "edges": []}' > workspace_state.json
```

### Step 1: Dynamic Domain Selection & Rule Loading
1. Look at the object name requested by the user (or detected in the unresolved queue).
2. Scan the **Domain Mapping Matrix** above to find which domain configuration file owns this object.
3. Dynamically replace the `<sourceFile>` logic and read only that targeted file (e.g., `references/cpq-data-model.json`).
4. Extract the object's `sourceFile` data path (e.g., `data/cpq_quotes.json`) and its specific relational foreign keys.

### Step 2: Formulate & Fire the Pipeline
Construct the parallel batch runner command, passing the discovered <fileType> and <type> variables directly into their respective flags. Run this concurrently for all files in the current batch:

For Windows PowerShell:

```powershell
python scripts\generic_batch_runner.py --worker "python scripts\utility_parse.py" --reducer "python scripts\utility_graph_output.py" --type "<fileType>" --metadata "<type>" --items "<comma_separated_file_paths>" --state "workspace_state.json"
```

*Example command generated for CPQ Quotes (Windows):*

```powershell
python scripts\generic_batch_runner.py --worker "python scripts\utility_parse.py" --reducer "python scripts\utility_graph_output.py" --type "json" --metadata "SBQQ__Quote__c" --items "data\cpq_quotes.json" --state "workspace_state.json"
```

For Linux / macOS / Git Bash:

```bash
python scripts/generic_batch_runner.py --worker "python scripts/utility_parse.py" --reducer "python scripts/utility_graph_output.py" --type "<fileType>" --metadata "<type>" --items "<comma_separated_file_paths>" --state "workspace_state.json"
```

*Example command generated for CPQ Quotes (Bash):*

```bash
python scripts/generic_batch_runner.py --worker "python scripts/utility_parse.py" --reducer "python scripts/utility_graph_output.py" --type "json" --metadata "SBQQ__Quote__c" --items "data/cpq_quotes.json" --state "workspace_state.json"
```
### Step 3: Check the Unresolved Record Queue
Immediately after running the parser pipeline, invoke the `utility-graph-resolver` to compute which Foreign Keys or child record lookups have been discovered but are not yet integrated into the master graph:

#### PowerShell Environment (Windows)
```powershell
python scripts\utility_graph_resolver.py "workspace_state.json" ".\data"
```

#### Bash Environment (Linux / macOS / Git Bash)
```bash
python scripts/utility_graph_resolver.py "workspace_state.json" "./data"
```

### Step 4: Evaluate & Recurse Data Nodes
Inspect the stdout JSON array returned by the resolver:
- **Scenario A (Array is NOT empty)**: The array contains outstanding linked record paths (e.g., `["data/contacts.json"]` because child contacts with matching `AccountId` values were discovered). Set this new data target array as your next batch and **immediately return to Step 1** (skipping Step 0).
- **Scenario B (Array is EMPTY `[]`)**: The complete transactional data network has been successfully traversed. Proceed to Step 5.

### Step 5: Final Delivery
Generate a summary lineage report for the user based *only* on the finalized dataset metrics. Inform the user that the workspace record graph has been successfully built and is ready for data quality or privacy-masking evaluation.
