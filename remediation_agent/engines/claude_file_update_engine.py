import json
import os
from pathlib import Path

import requests


ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"


def _relative_file(file_name: str) -> str:
    normalized = file_name.replace("\\", "/").strip()

    if "/harness/" in normalized:
        normalized = normalized.split("/harness/", 1)[1]

    normalized = normalized.lstrip("/")

    return normalized


def _safe_repo_path(repo_dir: str, relative_path: str) -> Path:
    repo_root = Path(repo_dir).resolve()
    target_path = (repo_root / relative_path).resolve()

    if not str(target_path).startswith(str(repo_root)):
        raise ValueError(f"Unsafe file path detected: {relative_path}")

    return target_path


def _affected_files(issues: list[dict]) -> list[str]:
    files = []

    for issue in issues:
        file_name = issue.get("file")

        if not file_name:
            continue

        relative = _relative_file(file_name)

        if relative not in files:
            files.append(relative)

    return files


def _read_files(repo_dir: str, files: list[str]) -> dict:
    file_contents = {}

    for file_name in files:
        file_path = _safe_repo_path(repo_dir, file_name)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        file_contents[file_name] = file_path.read_text(encoding="utf-8")

    return file_contents


def _build_prompt(issues: list[dict], file_contents: dict) -> str:
    return f"""
You are an autonomous secure-code remediation agent.

Your task:
Update the affected source files using the Harness STO findings and remediation guidance.

Rules:
- Work for any programming language.
- Update only the affected files provided below.
- Make the smallest safe code changes.
- Preserve application behavior.
- Do not rewrite unrelated code.
- Do not add comments unless required for the fix.
- Do not create new files.
- Return ONLY valid JSON.
- Do not return markdown.
- Do not wrap JSON in triple backticks.
- If no safe fix can be made, return updated=false.

Important:
- File paths in your response must match the provided affected file paths exactly.
- Do not return absolute paths such as /harness/app.py.
- Return relative paths such as app.py.

Harness STO Findings:
{json.dumps(issues, indent=2)}

Affected File Contents:
{json.dumps(file_contents, indent=2)}

Return JSON only in this format:
{{
  "updated": true,
  "summary": "Short summary of what was changed",
  "files": [
    {{
      "path": "relative/path/to/file",
      "content": "full updated file content",
      "reason": "why this file was changed"
    }}
  ]
}}
"""


def _extract_text(response_json: dict) -> str:
    content = response_json.get("content", [])

    text_parts = []

    for item in content:
        if item.get("type") == "text":
            text_parts.append(item.get("text", ""))

    return "\n".join(text_parts).strip()


def _parse_json_response(text: str) -> dict:
    cleaned = text.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`").strip()

        if cleaned.startswith("json"):
            cleaned = cleaned[4:].strip()

    if not cleaned.startswith("{"):
        start = cleaned.find("{")
        end = cleaned.rfind("}")

        if start == -1 or end == -1:
            raise ValueError(f"Claude response did not contain valid JSON:\n{cleaned}")

        cleaned = cleaned[start : end + 1]

    return json.loads(cleaned)


def _print_claude_usage(response_json: dict) -> None:
    usage = response_json.get("usage", {})

    print("Claude response metadata:")
    print(f"- Message ID    : {response_json.get('id')}")
    print(f"- Model         : {response_json.get('model')}")
    print(f"- Stop Reason   : {response_json.get('stop_reason')}")
    print(f"- Input Tokens  : {usage.get('input_tokens')}")
    print(f"- Output Tokens : {usage.get('output_tokens')}")


def _call_claude(prompt: str) -> dict:
    api_key = os.environ["ANTHROPIC_API_KEY"]

    model = os.environ.get(
        "ANTHROPIC_MODEL",
        "claude-sonnet-4-5-20250929",
    )

    response = requests.post(
        ANTHROPIC_API_URL,
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": model,
            "max_tokens": 6000,
            "temperature": 0,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        },
        timeout=120,
    )

    print(f"Claude API status: {response.status_code}")

    if response.status_code >= 400:
        print(response.text)

    response.raise_for_status()

    response_json = response.json()

    _print_claude_usage(response_json)

    text = _extract_text(response_json)

    return _parse_json_response(text)


def update_files(config, issues: list[dict]) -> list[dict]:
    files = _affected_files(issues)

    if not files:
        print("No affected files found for Claude remediation.")
        return []

    print("Affected files for Claude remediation:")
    for file_name in files:
        print(f"- {file_name}")

    file_contents = _read_files(config.local_repo_dir, files)

    prompt = _build_prompt(
        issues=issues,
        file_contents=file_contents,
    )

    result = _call_claude(prompt)

    if not result.get("updated"):
        print("Claude did not update files.")
        print(result.get("summary", "No summary returned."))
        return []

    updated_files = result.get("files", [])

    if not updated_files:
        print("Claude returned updated=true but no files were returned.")
        return []

    applied_fixes = []

    for file_update in updated_files:
        relative_path = _relative_file(file_update["path"])
        updated_content = file_update["content"]
        reason = file_update.get(
            "reason",
            "Claude updated file based on STO findings.",
        )

        if relative_path not in files:
            raise ValueError(
                f"Claude attempted to update an unexpected file: {relative_path}"
            )

        target_path = _safe_repo_path(config.local_repo_dir, relative_path)
        target_path.write_text(updated_content, encoding="utf-8")

        applied_fixes.append(
            {
                "file": relative_path,
                "reason": reason,
                "old_code": "__CLAUDE_FULL_FILE_UPDATE__",
                "new_code": "__CLAUDE_FULL_FILE_UPDATE__",
                "direct_edit": True,
            }
        )

    print("Claude remediation summary:")
    print(result.get("summary", ""))

    return applied_fixes