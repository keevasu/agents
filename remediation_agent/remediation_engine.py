def _clean_code_snippet(snippet: str | None) -> str:
    if not snippet:
        return ""

    cleaned = snippet.strip()

    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        lines = [line for line in lines if not line.strip().startswith("```")]
        cleaned = "\n".join(lines).strip()

    return cleaned


def generate_fix(issue: dict) -> dict | None:
    rule = issue.get("rule", "")
    snippet = _clean_code_snippet(issue.get("snippet"))
    file_name = issue["file"].replace("/harness/", "")

    if (
        "subprocess-shell-true" in rule
        or "gitlab.bandit.B602" in rule
        or "shell=True" in snippet
    ):
        old_code = snippet or "return subprocess.check_output(user_input, shell=True)"

        new_code = old_code.replace("shell=True", "shell=False")

        # POC-specific safe improvement for user_input command string
        new_code = new_code.replace(
            "subprocess.check_output(user_input, shell=False)",
            "subprocess.check_output(user_input.split(), shell=False)"
        )

        return {
            "file": file_name,
            "old_code": old_code,
            "new_code": new_code,
            "reason": "Replaces shell=True with shell=False to reduce OS command injection risk."
        }

    return None