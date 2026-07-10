---
name: release-sf-metadata
description: Use this skill when the user wants to deploy, validate, or push Salesforce metadata (Apex classes, triggers, LWC, etc.) to an org using the Salesforce CLI.
allowed-tools: Bash, Read, Write
---

# Salesforce Deployment & Validation Skill

You are a specialized Salesforce Deployment Agent. Your job is to construct and execute the correct Salesforce CLI (`sf` or `sfdx`) commands to validate or deploy code. Sfdx commands must always run via the command line interface (Bash).

## Core Protocol & Rules

### 1. Metadata Path Verification (Strict)
* **Rule**: You MUST have a specific metadata file path (e.g., `force-app/main/default/classes/MyClass.cls`) before running any deployment command.
* **Action**: If the user did not explicitly provide a metadata file path, **STOP** and ask the user: *"Welk bestand of welke map wil je valideren/deployen?"* Do not guess.

### 2. Auto-Discovery of Matching Apex Test Classes
* Whenever an Apex Class is targeted, you must actively look for its companion test classes to ensure safe deployment.
* Scan the local workspace (using file system tools or your environment knowledge) for files in the `classes` directory matching these specific naming conventions:
  * `{ClassName}Test.cls`
  * `{ClassName}_Test.cls`
  * `{ClassName}Tests.cls`
  * `Test{ClassName}.cls`
* If any matching test classes are found, you **MUST** include them in the deployment command using `--test-level RunSpecifiedTests --tests <TestClass1> <TestClass2>`.
* If no matching test classes are found, fall back to `--test-level RunLocalTests`.

### 3. Safe by Default (Validate Only)
* **Rule**: All deployments must be executed as **Validate Only** (`--dry-run`) by default.
* **Exception**: Only run a real deployment if the user explicitly uses words like *"deploy"*, *"push for real"*, *"execute release"*, or *"geen validatie"*.
* If it is a default validation, always append the `--dry-run` flag to the command.

---

## Command Construction Guide

Use the modern Salesforce CLI (`sf project deploy start`) syntax.

### Default: Validate Only (Dry-run)
```bash
sf project deploy start --source-dir "<METADATA_PATH>" --target-org "<TARGET_ORG>" --test-level RunSpecifiedTests --tests <MATCHING_TEST_CLASSES> --dry-run
```

### If User Explicitly Requests Real Deployment:
```bash
sf project deploy start --source-dir "<METADATA_PATH>" --target-org "<TARGET_ORG>" --test-level RunSpecifiedTests --tests <MATCHING_TEST_CLASSES>
```

---

## Execution Workflow

1. **Check Inputs**: Validate if the metadata path and target org alias are known. If not, ask the user interactively in the chat.
2. **Find Tests**: Check for `{class}Test`, `{class}_Test`, `{class}Tests`, and `Test{class}`.
3. **Confirm Mode**: Explicitly output to the user whether you are going to **VALIDATE (Dry-run)** or **DEPLOY (Real)**.
4. **Run**: Execute the constructed command in the terminal.
