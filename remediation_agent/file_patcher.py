from pathlib import Path


def apply_fix(repo_dir: str, fix: dict) -> bool:
    file_path = Path(repo_dir) / fix["file"]

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    content = file_path.read_text()

    if fix["old_code"] not in content:
        print(f"Old code not found in {file_path}")
        return False

    updated = content.replace(fix["old_code"], fix["new_code"], 1)
    file_path.write_text(updated)

    return True