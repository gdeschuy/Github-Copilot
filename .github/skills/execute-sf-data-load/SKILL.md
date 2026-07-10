---
name: execute-sf-data-load
description: "A live data infrastructure skill. It enables the AI agent to execute high-speed SOQL queries directly against a live Salesforce environment, export object-specific data into a local data directory as CSV files, and push data updates (inserts, updates, upserts) back to the cloud using the native Salesforce CLI (`sf`)."
---

# Utility Salesforce Data Load Skill

## Capabilities
- **Live Cloud Extraction**: Queries real-time sandboxes or production environments via SOQL without local storage limitations.
- **Automated CSV Dumping**: Exports targeted object datasets directly into dedicated files (e.g., `data/Account.csv`) using native CLI formatters, making them instantly available for the local `CsvParser` pipeline.
- **Transactional Cloud Writing**: Pushes local architectural or data changes back to Salesforce via single-record updates or multi-core bulk operations.

## Usage Schema (Windows PowerShell & Bash Commands)

### 1. Extracting Live Data to Object-Specific CSV Files (For Offline Graph Analysis)
To pull live records and store them for the local `analyse-sf-data` skill, execute a SOQL query using the CSV result format and redirect the output to the dedicated `data/` directory:

#### PowerShell Environment (Windows)
```powershell
sf data query --query "SELECT Id, Name, AccountId FROM Contact WHERE CreatedDate = THIS_MONTH" --result-format csv | Out-File -FilePath "data\Contact.csv" -Encoding utf8
```

#### Bash Environment (Linux / macOS / Git Bash)
```bash
sf data query --query "SELECT Id, Name, AccountId FROM Contact WHERE CreatedDate = THIS_MONTH" --result-format csv > data/Contact.csv
```

---

### 2. Querying Live Data directly into the Graph (Streaming In-Memory)
To pipe raw query data straight into the graph reducer without saving a local CSV file, force the `--json` flag:

#### PowerShell Environment (Windows)
```powershell
sf data query --query "SELECT Id, Name, AccountId FROM Contact" --json | python scripts\utility_graph_output.py "workspace_state.json" "Contact"
```

#### Bash Environment (Linux / macOS / Git Bash)
```bash
sf data query --query "SELECT Id, Name, AccountId FROM Contact" --json | python scripts/utility_graph_output.py "workspace_state.json" "Contact"
```

---

### 3. Updating Live Data using local CSV files
To push architectural updates or data corrections back to Salesforce from your local staging directory, trigger the bulk insertion worker:

#### PowerShell Environment (Windows)
```powershell
sf data record insert bulk --sobject <SObject> --file "data\<SObject>.csv"
```

*Example: Pushing updated Accounts to Salesforce on Windows:*
```powershell
sf data record insert bulk --sobject Account --file data\Account.csv
```

#### Bash Environment (Linux / macOS / Git Bash)
```bash
sf data record insert bulk --sobject <SObject> --file data/<SObject>.csv
```

---

## Agent Execution Instructions
1. **Identify Strategy**: Determine if the task requires a live, in-memory graph stream (Use Schema 2) or a persistent local dump for continuous repository analysis (Use Schema 1).
2. **Execute CSV Dump**: If persistent data mapping is required, locate the object name, construct the SOQL statement, and execute the **CSV Extraction Command** (Schema 1) targeting the `data\<SObject>.csv` file path.
3. **Notify Orchestrator**: Once the CSV file is written to the disk, update the corresponding `references/*-data-model.json` configuration entry to match the new file target, and hand execution back to `analyse-sf-data` to crawl the local file.
4. **Execute Cloud Sync**: If data modifications are verified and approved, use the **Bulk Data Command** (Schema 3) to upload the corrected data back to Salesforce.
