---
name: execute-sf-data-load
description: "A live data infrastructure and sequencing skill. It enables the AI agent to query live Salesforce environments, export datasets to a local data directory as CSV files, automatically calculate the correct relational insertion order using data-load-order.py, and safely push updates back to the cloud."
---

# Utility Salesforce Data Load Skill

## Capabilities
- **Live Cloud Extraction**: Queries real-time sandboxes or production environments via SOQL without local storage limitations.
- **Automated CSV Dumping**: Exports targeted object datasets directly into dedicated files (e.g., `data/Account.csv`) using native CLI formatters, making them instantly available for the local `CsvParser` pipeline.
- **Dependency-Aware Sequencing**: Executes `data-load-order.py` to automatically compute the correct transactional order of operations (Topological Sort), eliminating Foreign Key insertion failures.
- **Transactional Cloud Writing**: Pushes local architectural or data changes back to Salesforce via single-record updates or sequential multi-core bulk operations.

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

### 3. Pushing Sequenced Data to Salesforce via Bulk CLI
Always execute these bulk commands sequentially, strictly following the array indices returned by the data-load-order utility (Schema 2):

#### PowerShell Environment (Windows)
```powershell
sf data record insert bulk --sobject <SObject> --file "data\<SObject>.csv"
```

*Example: Pushing a sequenced Account batch on Windows:*
```powershell
sf data record insert bulk --sobject Account --file data\Account.csv
```

#### Bash Environment (Linux / macOS / Git Bash)
```bash
sf data record insert bulk --sobject <SObject> --file data/<SObject>.csv
```

---

## Agent Execution Instructions

### Phase A: Data Extraction & Analysis Loop
1. **Identify Strategy**: Determine if the task requires a live, in-memory graph stream or a persistent local dump for continuous repository analysis.
2. **Execute CSV Dump**: If persistent data mapping is required, locate the object name, construct the SOQL statement, and execute the **CSV Extraction Command** (Schema 1) targeting the `data\<SObject>.csv` file path.
3. **Notify Orchestrator**: Once the CSV file is written to the disk, update the corresponding `references/*-data-model.json` configuration entry to match the new file target, and hand execution back to `analyse-sf-data` to crawl the local file.

### Phase B: Safe Data Deployment Loop (DML / Upload)
1. **Trigger Order Calculator**: When instructed to load or sync a collection of data files back to Salesforce, **do not fire commands simultaneously**. First, execute the **Data Insertion Order Command** (Schema 2).
2. **Evaluate the Queue**: Parse the resulting JSON array from `stdout`. The array lists the objects from least-dependent (Parents) to most-dependent (Children).
3. **Execute Sequential DML**: Loop through the generated list and trigger the **Bulk Insertion Command** (Schema 3) one by one. Always wait for the current bulk job to be 100% completed and verified before starting the next item in the queue.
