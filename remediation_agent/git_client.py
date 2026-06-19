from git import Repo, GitCommandError


def create_branch(repo_dir: str, branch_name: str, base_branch: str = "main") -> None:
    repo = Repo(repo_dir)

    repo.git.fetch("origin")
    repo.git.checkout(base_branch)
    repo.git.reset("--hard", f"origin/{base_branch}")

    if branch_name in [head.name for head in repo.heads]:
        repo.git.branch("-D", branch_name)

    repo.git.checkout("-b", branch_name)

    print(f"Created branch: {branch_name}")


def commit_changes(repo_dir: str, message: str) -> bool:
    repo = Repo(repo_dir)
    repo.git.add(A=True)

    if not repo.is_dirty(untracked_files=True):
        print("No changes to commit.")
        return False

    repo.index.commit(message)
    print("Committed changes.")
    return True


def push_branch(repo_dir: str, branch_name: str) -> None:
    repo = Repo(repo_dir)

    try:
        repo.git.push("--set-upstream", "origin", branch_name, "--force")
        print(f"Pushed branch: {branch_name}")
    except GitCommandError as error:
        print("Failed to push branch.")
        raise error