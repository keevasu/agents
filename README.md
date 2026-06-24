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
# Autonomous Remediation Framework

## Overview

The Autonomous Remediation Framework automatically retrieves security findings, generates remediations, modifies source code, and creates Pull Requests or Merge Requests.

The framework is designed to be provider-agnostic and extensible.

Current implementation supports:

* Harness STO as the finding source.
* Rule-based remediation engine.
* Harness Code Pull Requests.
* GitLab Merge Requests.

Future support includes:

* GitLab Security
* SonarQube
* Veracode
* Snyk
* OpenAI
* Claude
* AIDA
* GitHub
* Bitbucket

---

# Architecture

```text
Finding Provider
        ↓
Remediation Provider
        ↓
File Patcher
        ↓
Git Operations
        ↓
Repository Provider
```

---

# Current End-to-End Flows

## Harness Code

```text
Harness Code Repo
        ↓
Harness CI Pipeline
        ↓
Harness STO Scan
        ↓
STO Issues API
        ↓
Rule-Based Remediation
        ↓
Update Source Code
        ↓
Git Branch
        ↓
Commit
        ↓
Push
        ↓
Harness Code Pull Request
```

---

## GitLab

```text
GitLab Repository
        ↓
Harness CI Pipeline
        ↓
Harness STO Scan
        ↓
STO Issues API
        ↓
Rule-Based Remediation
        ↓
Update Source Code
        ↓
Git Branch
        ↓
Commit
        ↓
Push
        ↓
GitLab Merge Request
```

---

# Project Structure

```text
remediation_agent/

config.py

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

## config.py

Centralized configuration layer.

All environment variable access is contained within this module.

The rest of the framework consumes an AppConfig object rather than directly reading environment variables.

---

## main.py

Workflow orchestrator.

Responsible for:

* Retrieving findings
* Generating fixes
* Applying changes
* Creating commits
* Pushing branches
* Creating PRs/MRs

---

## remediation_engine.py

Current implementation uses deterministic rules.

Supported vulnerability patterns:

* subprocess shell=True

Future engines:

* Claude
* OpenAI
* AIDA
* STO-guided engine

---

## file_patcher.py

Responsible for modifying source files.

---

## git_client.py

Handles:

* create_branch()
* commit_changes()
* push_branch()

---

## pr_client.py

Repository abstraction layer.

Routes requests to:

* Harness Code
* GitLab
* GitHub

---

## providers/

Repository-specific implementations.

### harness_code_provider.py

Creates Harness Code Pull Requests.

### gitlab_provider.py

Creates GitLab Merge Requests.

### github_provider.py

Future support.

---

# Environment Variables

## Finding Provider

```text
FINDING_PROVIDER=harness_sto
```

Future:

```text
FINDING_PROVIDER=gitlab_security
FINDING_PROVIDER=sonarqube
FINDING_PROVIDER=veracode
```

---

## Remediation Provider

```text
REMEDIATION_PROVIDER=rules
```

Future:

```text
REMEDIATION_PROVIDER=sto
REMEDIATION_PROVIDER=claude
REMEDIATION_PROVIDER=openai
REMEDIATION_PROVIDER=aida
```

---

## Repository Provider

Harness Code:

```text
REPO_PROVIDER=harness_code
```

GitLab:

```text
REPO_PROVIDER=gitlab
```

Future:

```text
REPO_PROVIDER=github
REPO_PROVIDER=bitbucket
```

---

# Current Capabilities

✅ Retrieve vulnerabilities from Harness STO

✅ Parse vulnerability metadata

✅ Generate remediations

✅ Update source code

✅ Create Git branches

✅ Commit changes

✅ Push branches

✅ Create Harness Code Pull Requests

✅ Create GitLab Merge Requests

---

# Future Architecture

```text
Harness STO
GitLab Security
SonarQube
Veracode
Snyk

        ↓

Unified Finding Model

        ↓

Rules Engine
Claude
OpenAI
AIDA

        ↓

Patch Object

        ↓

Repository Providers

Harness Code
GitLab
GitHub
Bitbucket
```

---

# Long-Term Vision

```text
Finding Provider
        ↓
Remediation Provider
        ↓
Repository Provider
```

All behavior should eventually be driven entirely by environment variables, allowing new providers to be introduced without changing the framework code.

