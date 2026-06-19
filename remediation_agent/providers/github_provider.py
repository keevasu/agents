import os
import requests


def create_pull_request(
    source_branch: str,
    target_branch: str,
    title: str,
    description: str,
) -> dict:
    github_owner = os.environ["GITHUB_OWNER"]
    github_repo = os.environ["GITHUB_REPO"]
    token = os.environ["GITHUB_TOKEN"]

    url = f"https://api.github.com/repos/{github_owner}/{github_repo}/pulls"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }

    payload = {
        "head": source_branch,
        "base": target_branch,
        "title": title,
        "body": description,
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)

    print(f"GitHub PR API status: {response.status_code}")
    print(response.text)

    response.raise_for_status()
    return response.json()