import os
from dataclasses import dataclass


@dataclass
class AppConfig:
    harness_base_url: str
    harness_account_id: str
    harness_api_key: str
    harness_scan_id: str

    finding_provider: str
    remediation_provider: str
    repo_provider: str

    local_repo_dir: str
    base_branch: str
    remediation_branch: str
    pr_title: str

    harness_org_id: str | None
    harness_project_id: str | None
    harness_repo_identifier: str | None

    gitlab_base_url: str | None
    gitlab_project_id: str | None
    gitlab_token: str | None


def load_config() -> AppConfig:
    harness_scan_id = os.environ["HARNESS_SCAN_ID"]

    return AppConfig(
        harness_base_url=os.environ.get("HARNESS_BASE_URL", "https://app.harness.io"),
        harness_account_id=os.environ["HARNESS_ACCOUNT_ID"],
        harness_api_key=os.environ["HARNESS_API_KEY"],
        harness_scan_id=harness_scan_id,

        finding_provider=os.environ.get("FINDING_PROVIDER", "harness_sto"),
        remediation_provider=os.environ.get("REMEDIATION_PROVIDER", "rules"),
        repo_provider=os.environ.get("REPO_PROVIDER", "none"),

        local_repo_dir=os.environ["LOCAL_REPO_DIR"],
        base_branch=os.environ.get("BASE_BRANCH", "main"),
        remediation_branch=os.environ.get(
            "REMEDIATION_BRANCH",
            f"auto-remediate-{harness_scan_id}",
        ),
        pr_title=os.environ.get(
            "PR_TITLE",
            "Auto-remediation for STO findings",
        ),

        harness_org_id=os.environ.get("HARNESS_ORG_ID"),
        harness_project_id=os.environ.get("HARNESS_PROJECT_ID"),
        harness_repo_identifier=os.environ.get("HARNESS_REPO_IDENTIFIER"),

        gitlab_base_url=os.environ.get("GITLAB_BASE_URL", "https://gitlab.com"),
        gitlab_project_id=os.environ.get("GITLAB_PROJECT_ID"),
        gitlab_token=os.environ.get("GITLAB_TOKEN"),
    )