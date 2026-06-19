import os
import requests


def create_merge_request(
    source_branch: str,
    target_branch: str,
    title: str,
    description: str,
) -> dict:
    gitlab_base_url = os.environ["GITLAB_BASE_URL"].rstrip("/")
    project_id = os.environ["GITLAB_PROJECT_ID"]
    token = os.environ["GITLAB_TOKEN"]

    url = f"{gitlab_base_url}/api/v4/projects/{project_id}/merge_requests"

    headers = {
        "PRIVATE-TOKEN": token,
        "Content-Type": "application/json",
    }

    payload = {
        "source_branch": source_branch,
        "target_branch": target_branch,
        "title": title,
        "description": description,
        "remove_source_branch": False,
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)

    print(f"GitLab MR API status: {response.status_code}")
    print(response.text)

    response.raise_for_status()
    return response.json()