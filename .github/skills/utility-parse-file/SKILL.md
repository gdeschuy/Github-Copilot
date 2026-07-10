---
name: utility-parse-file
description: A low-level framework utility skill that parses files based on their type and outputs a normalized structure. Use when you need to extract structured data from various file formats.
---

# Utility Parse Skill

## Description
A low-level framework utility skill that acts as a deterministic worker. It takes a file and an abstract file type specification directly from an orchestrator skill, routes the file to the correct internal parsing engine, and dumps the normalized structure to standard output (`stdout`).

## Capabilities
- **Blind Routing**: Does not contain any domain or Salesforce-specific knowledge. It relies entirely on the parameters provided by the calling orchestrator.
- **AST & Dynamic Extraction**: Automatically extracts structural code hooks (`extends`, `implements`, `new` instantiations) when executed with the `code` type.
- **Streaming Output**: Guarantees a clean JSON object returned via `stdout`, allowing concurrent request routers to capture the stream in-memory without disk contention.

## Usage Schema (CLI Command)
To execute a parse job, pass the abstract `file_type` and the relative `file_path` exactly as dictated by the orchestrator skill:

```powershell
python scripts\utility_parse.py <file_type> <file_path>
```

```bash
python scripts/utility_parse.py <file_type> <file_path>
```

### Supported File Types
* `code` -> Activates the Tree-Sitter AST parser engine.
* `xml` -> Activates the normalized XML element parser engine.
* `json` -> Activates the flattened key-indexing JSON parser engine.

### Examples

**1. Executing a Code Parse Task**

```powershell
python scripts\utility_parse.py "code" "force-app\main\default\classes\AccountService.cls"
```

```bash
python scripts/utility_parse.py "code" "force-app/main/default/classes/AccountService.cls"
```

**2. Executing an XML Parse Task**
```powershell
python scripts\utility_parse.py "xml" "force-app\main\default\objects\Account.object"
```

```bash
python scripts/utility_parse.py "xml" "force-app/main/default/objects/Account.object"
```

## Agent Execution Instructions
1. **Receive Parameters**: Do not attempt to guess or discover the file type from the repository structure. Wait for the `analyse-sf-metadata` skill to provide the exact `file_type`.
2. **Execute Command**: Construct the CLI command using the provided `<file_type>` and `<file_path>`.
3. **Pipe Output**: Capture the standard output (`stdout`) stream and immediately hand it over to the next pipeline skill (`utility-graph-output`) for graph integration.
