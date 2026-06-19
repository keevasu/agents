import os
import requests


HARNESS_BASE_URL = "https://app.harness.io"


def create_pull_request(
    source_branch: str,
    target_branch: str,
    title: str,
    description: str,
) -> dict:
    account_id = os.environ["HARNESS_ACCOUNT_ID"]
    org_id = os.environ["HARNESS_ORG_ID"]
    project_id = os.environ["HARNESS_PROJECT_ID"]
    repo_identifier = os.environ["HARNESS_REPO_IDENTIFIER"]
    api_key = os.environ["HARNESS_API_KEY"]

    url = f"{HARNESS_BASE_URL}/code/api/v1/repos/{repo_identifier}/pullreq"

    params = {
        "accountIdentifier": account_id,
        "orgIdentifier": org_id,
        "projectIdentifier": project_id,
    }

    headers = {
        "X-Api-Key": api_key,
        "Content-Type": "application/json",
    }

    payload = {
        "source_branch": source_branch,
        "target_branch": target_branch,
        "title": title,
        "description": description,
    }

    response = requests.post(
        url,
        params=params,
        headers=headers,
        json=payload,
        timeout=30,
    )

    print(f"Harness Code PR API status: {response.status_code}")
    print(response.text)

    response.raise_for_status()
    return response.json()