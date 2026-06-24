For Strands SDK and to connect to Bedrock 

*  export AWS_ACCESS_KEY_ID=xxxxx
*  export AWS_SECRET_ACCESS_KEY=yyyy
 Optionally, set the region
* export AWS_DEFAULT_REGION=

For Strands SDK and to connect to anthropic claude
* Get the API-Key from claude console 

***********************************************

Setting up your python env

* python3 -m venv .myenv

* source myenv/bin/activate

* pip3 install -r requirements.txt

* deactivate (To deactivate your virtual environment)

***********************************************
For setting up your claude Agent SDK

* export ANTHROPIC_API_KEY="fffffff"
* curl -fsSL https://claude.ai/install.sh | bash - This is to install Claude CLI for ClaudeSDKClient - This is useful when you are using streaming and query options

*****************************************************************************************************************************************
agents/
│
├── README.md          ← Put it here
│
├── requirements.txt
│
├── remediation_agent/
│     main.py
│     remediation_engine.py
│     file_patcher.py
│     git_client.py
│     pr_client.py
│
│     providers/
│         harness_code_provider.py
│         gitlab_provider.py
│         github_provider.py
│
└── ...
# Autonomous Remediation Framework

## Overview

The Autonomous Remediation Framework automatically retrieves security findings, generates remediations, modifies source code, and creates Pull Requests.

The framework is intentionally designed to support multiple security scanners and multiple repository providers.

Current implementation supports:

* Harness STO as the finding source.
* Harness Code as the repository provider.

The architecture is designed to support:

* GitLab Security
* SonarQube
* Veracode
* Snyk
* GitHub
* GitLab
* Bitbucket

---

# End-to-End Workflow

```text
Security Findings
        ↓
Finding Source Adapter
        ↓
Remediation Engine
        ↓
File Patcher
        ↓
Git Operations
        ↓
Repository Provider
        ↓
Pull Request
```

Current flow:

```text
Harness STO
        ↓
Retrieve Findings
        ↓
Generate Remediation
        ↓
Modify Source Code
        ↓
Create Branch
        ↓
Commit Changes
        ↓
Push Branch
        ↓
Create Pull Request
```

---

# Project Structure

```text
agents/

requirements.txt

README.md

remediation_agent/

    main.py

    remediation_engine.py

    file_patcher.py

    git_client.py

    pr_client.py

    providers/

        harness_code_provider.py

        gitlab_provider.py

        github_provider.py
```

---

# Components

## main.py

Acts as the workflow orchestrator.

Responsibilities:

* Retrieve findings.
* Parse vulnerabilities.
* Generate fixes.
* Apply code changes.
* Commit changes.
* Push branch.
* Create Pull Request.

---

## remediation_engine.py

Generates remediations.

Current implementation uses deterministic rules.

Future engines:

* Claude
* OpenAI
* AIDA
* Strands Agent

---

## file_patcher.py

Updates source files.

Responsibilities:

* Open files.
* Find vulnerable code.
* Replace with remediated code.
* Save changes.

---

## git_client.py

Handles Git operations.

Functions:

* create_branch()
* commit_changes()
* push_branch()

These operations are repository-provider independent.

---

## pr_client.py

Acts as the provider abstraction layer.

Environment variable:

```text
REPO_PROVIDER
```

Supported values:

```text
none
harness_code
gitlab
github
```

Routes Pull Request creation to the appropriate provider.

---

## providers/

Contains repository-specific implementations.

### harness_code_provider.py

Creates Pull Requests in Harness Code.

### gitlab_provider.py

Future GitLab Merge Request implementation.

### github_provider.py

Future GitHub Pull Request implementation.

---

# Environment Variables

## Harness STO

```text
HARNESS_ACCOUNT_ID

HARNESS_API_KEY

HARNESS_SCAN_ID
```

## Repository

```text
LOCAL_REPO_DIR

BASE_BRANCH
```

## Repository Provider

```text
REPO_PROVIDER
```

Examples:

```text
REPO_PROVIDER=harness_code

REPO_PROVIDER=gitlab

REPO_PROVIDER=github
```

## Harness Code

```text
HARNESS_ORG_ID

HARNESS_PROJECT_ID

HARNESS_REPO_IDENTIFIER
```

---

# Current Capabilities

✅ Retrieve vulnerabilities from Harness STO

✅ Parse findings

✅ Generate remediations

✅ Modify source code

✅ Create branch

✅ Commit changes

✅ Push branch

✅ Create Pull Request in Harness Code

---

# Architecture

```text
Harness STO
        ↓
Finding Parser
        ↓
Remediation Engine
        ↓
File Patcher
        ↓
Git Client
        ↓
Repository Provider
        ↓
Pull Request
```

---

# Future Enhancements

## Finding Providers

* Harness STO
* GitLab Security
* SonarQube
* Veracode
* Snyk
* Trivy

---

## Remediation Engines

* Rules Engine
* Claude
* OpenAI
* AIDA
* Strands Agent

---

## Repository Providers

* Harness Code
* GitLab
* GitHub
* Bitbucket

---

# Long-Term Vision

```text
Security Scanner
        ↓
Unified Finding Model
        ↓
AI Agent
        ↓
File Patcher
        ↓
Git Operations
        ↓
Repository Provider
        ↓
Pull Request
```

The framework is being designed as a provider-agnostic, extensible autonomous remediation platform.
