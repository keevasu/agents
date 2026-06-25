import requests


def discover_scan_id(config) -> str:
    if config.harness_scan_id:
        print(f"Using provided HARNESS_SCAN_ID: {config.harness_scan_id}")
        return config.harness_scan_id

    if not config.harness_execution_id:
        raise ValueError(
            "Either HARNESS_SCAN_ID or HARNESS_EXECUTION_ID must be provided."
        )

    print(f"Discovering STO scan for execution ID: {config.harness_execution_id}")

    url = f"{config.harness_base_url}/sto/api/v2/scans"

    headers = {
        "X-Api-Key": config.harness_api_key,
    }

    params = {
        "accountId": config.harness_account_id,
        "page": 0,
        "pageSize": 100,
    }

    response = requests.get(url, headers=headers, params=params, timeout=30)
    response.raise_for_status()

    scans = response.json().get("results", [])

    matches = [
        scan
        for scan in scans
        if scan.get("executionId") == config.harness_execution_id
        and scan.get("status") == "Succeeded"
    ]

    matches.sort(key=lambda scan: scan.get("created", 0), reverse=True)

    if not matches:
        raise ValueError(
            f"No successful STO scan found for execution ID: {config.harness_execution_id}"
        )

    scan_id = matches[0]["id"]

    print(f"Discovered STO Scan ID: {scan_id}")

    return scan_id


def get_scan_issues(config, scan_id: str) -> list[dict]:
    url = f"{config.harness_base_url}/sto/api/v2/scans/{scan_id}/issues"

    headers = {
        "X-Api-Key": config.harness_api_key,
    }

    params = {
        "accountId": config.harness_account_id,
    }

    response = requests.get(url, headers=headers, params=params, timeout=30)
    response.raise_for_status()

    return response.json().get("issues", [])