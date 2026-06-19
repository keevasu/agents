import os


def create_pull_request(
    source_branch: str,
    target_branch: str,
    title: str,
    description: str,
) -> None:
    provider = os.environ.get("REPO_PROVIDER", "none").lower()

    if provider == "none":
        print("PR creation skipped. REPO_PROVIDER=none")
        print(f"Branch pushed: {source_branch}")
        return

    if provider == "harness_code":
        from providers.harness_code_provider import create_pull_request as create_harness_pr

        create_harness_pr(
            source_branch=source_branch,
            target_branch=target_branch,
            title=title,
            description=description,
        )
        return

    if provider == "gitlab":
        from providers.gitlab_provider import create_merge_request

        create_merge_request(
            source_branch=source_branch,
            target_branch=target_branch,
            title=title,
            description=description,
        )
        return

    if provider == "github":
        from providers.github_provider import create_pull_request as create_github_pr

        create_github_pr(
            source_branch=source_branch,
            target_branch=target_branch,
            title=title,
            description=description,
        )
        return

    raise ValueError(f"Unsupported REPO_PROVIDER: {provider}")