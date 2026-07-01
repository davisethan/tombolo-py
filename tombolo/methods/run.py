import json
import os
import subprocess


_image = os.getenv("TOMBOLO", "ethandavisecd/tombolo:latest")


def _run(method: str, data: list[dict], greater_is_better: bool) -> dict:
    request = {
        "jsonrpc": "2.0",
        "method": method,
        "params": {
            "data": data,
            "greater_is_better": greater_is_better,
        },
        "id": 1,
    }
    proc = subprocess.run(
        ["docker", "run", "--rm", "-i", _image],
        input=json.dumps(request).encode(),
        capture_output=True,
        check=True,
    )
    response = json.loads(proc.stdout)
    if "error" in response:
        raise RuntimeError(response["error"]["message"])
    return response["result"]
