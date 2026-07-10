---
name: execute-sf-data-load
description: "A live data infrastructure and sequencing skill. It enables the AI agent to query live Salesforce environments, export datasets to a local data directory as CSV files, automatically calculate the correct relational insertion order using data-load-order.py, compile transaction logs into an assets directory as success.csv and error.csv, and trigger a Python rollback handler (rollback.py) upon deployment failure."
---

# Utility Salesforce Data Load Skill

## Capabilities
- **Live Cloud Extraction**: Queries real-time sandboxes or production environments via SOQL without local storage limitations.
- **Automated CSV Dumping**: Exports targeted object datasets directly into dedicated files (e.g., `data/Account.csv`) using native CLI formatters, making them instantly available for the local `CsvParser` pipeline.
- **Dependency-Aware Sequencing**: Executes `data-load-order.py` to automatically compute the correct transactional order of operations (Topological Sort), eliminating Foreign Key insertion failures.
- **Transactional Cloud Writing & Recovery**: Pushes local data changes back to Salesforce via sequential bulk operations, writes execution artifacts (`success.csv`/`error.csv`) to a local assets folder, and triggers `rollback.py` to execute automated LIFO purges if errors occur.

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

### 2. Calculating the Safe Data Insertion Order (The Dependency Sorcerer)
Before pushing any collection of local data files to the cloud, invoke the graph load order calculator to output the exact execution queue via `stdout`:

#### PowerShell Environment (Windows)
```powershell
python scripts\data-load-order.py "workspace_state.json"
```

#### Bash Environment (Linux / macOS / Git Bash)
```bash
python scripts/data-load-order.py "workspace_state.json"
```

---

### 3. Pushing Sequenced Data to Salesforce (Upsert Preferent)
When pushing data to Salesforce, always inspect the data model configuration for an `externalIdField`.

#### Scenario A: External ID is Present (Preferred Upsert)
If defined, execute a bulk upsert command by passing the target SObject, the specific External ID API name, and the CSV file:

##### PowerShell Environment (Windows)
```powershell
sf data record upsert bulk --sobject <SObject> --external-id-id <externalIdField> --file "data\<SObject>.csv"
```

##### Bash Environment (Linux / macOS / Git Bash)
```bash
sf data record upsert bulk --sobject <SObject> --external-id-id <externalIdField> --file data/<SObject>.csv
```

*Example: Upserting CPQ Quotes using 'Quote_Number__c' on Windows:*
```powershell
sf data record upsert bulk --sobject SBQQ__Quote__c --external-id-id SBQQ__QuoteNumber__c --file data\SBQQ__Quote__c.csv
```

#### Scenario B: No External ID is Present (Fallback Insert)
If no external ID field is specified in the configuration, fall back to a traditional bulk insertion:

##### PowerShell Environment (Windows)
```powershell
sf data record insert bulk --sobject <SObject> --file "data\<SObject>.csv"
```

---

### 4. Invoking the Python State Recovery Engine (Automated Rollback)
If any partial bulk deployment failure is logged in the error asset, invoke the Python rollback utility to execute an atomic cloud purge:

#### PowerShell Environment (Windows)
```powershell
python scripts\rollback.py "skills\execute-sf-data-load\assets\error_log.json"
```

#### Bash Environment (Linux / macOS / Git Bash)
```bash
python scripts/rollback.py skills/execute-sf-data-load/assets/error_log.json
```

---

## Agent Execution Instructions

### Phase A: Data Extraction & Staging Loop
1. **Identify Strategy**: Determine if the user prompt requires a real-time cloud analysis or a persistent local download for sequential analysis.
2. **Execute CSV Dump**: If persistent data mapping is needed, construct the SOQL statement and execute the **CSV Extraction Command** (Schema 1) targeting the matching path (e.g., `data\<SObject>.csv`).
3. **Notify Orchestrator**: Once the file is written, pass control back to `analyse-sf-data` to crawl the local file.

### Phase B: Safe Data Deployment & Recovery Loop (DML / Upload)
1. **Trigger Order Calculator**: When instructed to load or sync data files back to Salesforce, execute the **Data Insertion Order Command** (Schema 2) to calculate the queue (`data-load-order.py`).
2. **Evaluate Domain Config for Upsert**: For each object in the resulting queue, inspect its entry in the active domain configuration file (e.g., `references/cpq-data-model.json`):
   - **Check for `externalIdField`**: Look for the presence of an `"externalIdField"` key.
3. **Execute Sequential DML & Log Artifacts**: Loop through the queue and execute the commands one by one. Always capture the Salesforce CLI execution result (`stdout`/`stderr`):
   - **If `externalIdField` exists**: Trigger **Scenario A (Upsert Bulk)** using that specific field name.
   - **If `externalIdField` does NOT exist**: Trigger **Scenario B (Insert Bulk)** as a fallback.
   - **Write Logs**: Convert the transaction records from the CLI responses and save them as flat files inside the specialized asset directory:
     - Save successful transactions to: `skills\execute-sf-data-load\assets\success.csv`
     - Save failure details and validation crashes to: `skills\execute-sf-data-load\assets\error.csv`
4. **Enforce Error Catching & Rollback**: Monitor the results of each batch:
   - **If `error.csv` is populated or the batch fails**: **Stop the deployment sequence immediately**. Do not proceed to the next item in the queue.
   - **Execute Python Recovery**: Construct and run the **Automated Rollback Command** (Schema 4) to fire `rollback.py`. This script will parse the logging state and execute a reverse LIFO deletion to clean dirty records from the cloud.
