def generate_fix(issue: dict) -> dict | None:
    rule = issue.get("rule", "")
    snippet = issue.get("snippet", "")

    if "subprocess-shell-true" in rule or "gitlab.bandit.B602" in rule:
        return {
            "file": issue["file"].replace("/harness/", ""),
            "old_code": "return subprocess.check_output(user_input, shell=True)",
            "new_code": "return subprocess.check_output(user_input.split(), shell=False)",
            "reason": "Replaces shell=True with shell=False to reduce OS command injection risk."
        }

    return None