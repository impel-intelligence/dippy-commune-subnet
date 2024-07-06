import subprocess
import requests

from dippy_validation_api.scores import Scores, StatusEnum
from dataclasses import dataclass
from shlex import split
from importlib.metadata import version
import os
from rich.table import Table
from rich.console import Console

REPO_ROOT_DIR = "/home/ubuntu/commune-subnet"
VALIDATION_SERVER_URL = "127.0.0.1"

@dataclass
class LocalMetadata:
    """Metadata associated with the local validator instance"""

    commit: str
    commune_version: str
    uid: int = 0
    coldkey: str = ""
    hotkey: str = ""


def local_metadata() -> LocalMetadata:
    """Extract the version as current git commit hash"""
    commit_hash = ""
    try:
        result = subprocess.run(
            split("git rev-parse HEAD"),
            check=True,
            capture_output=True,
            cwd=REPO_ROOT_DIR,
        )
        commit = result.stdout.decode().strip()
        assert len(commit) == 40, f"Invalid commit hash: {commit}"
        commit_hash = commit[:8]
    except:
        commit_hash = "unkown"

    commune_version = version("communex")
    return LocalMetadata(
        commit=commit_hash,
        commune_version=commune_version,
    )

def get_model_score(
    namespace,
    name,
    hash,
    template,
    local_metadata: LocalMetadata,
    useLocal: bool = False,
) -> Scores:
    # Status:
    # QUEUED, RUNNING, FAILED, COMPLETED
    # return (score, status)
    if useLocal:
        validation_endpoint = f"http://localhost:9999/evaluate_model_commune"
    else:
        validation_endpoint = f"{VALIDATION_SERVER_URL}/evaluate_model_commune"

    # Construct the payload with the model name and chat template type
    payload = {
        "repo_namespace": namespace,
        "repo_name": name,
        "hash": hash,
        "chat_template_type": template,
    }

    headers = {
        "Git-Commit": str(local_metadata.commit),
        "Commune-Version": str(local_metadata.commune_version),
        "UID": str(local_metadata.uid),
        "Hotkey": str(local_metadata.hotkey),
        "Coldkey": str(local_metadata.coldkey),
    }
    if os.environ.get("ADMIN_KEY", None) not in [None, ""]:
        payload["admin_key"] = os.environ["ADMIN_KEY"]

    console = Console()
    console.print(f"Payload: {payload}")
    score_data = Scores()
    # Make the POST request to the validation endpoint
    try:
        response = requests.post(validation_endpoint, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        # Parse the response JSON
        result = response.json()
        console = Console()
        console.print(f"Payload: {payload}")
        status = StatusEnum.from_string(result["status"])
        score_data.status = status

        if status == StatusEnum.COMPLETED:
            score_data.total_score = result["score"]["total_score"]
            score_data.vibe_score = result["score"]["vibe_score"]
            score_data.coherence_score = result["score"]["coherence_score"]
            # score = result["score"]["total_score"]
        elif status == StatusEnum.FAILED:
            log.warning(f"Model {namespace}/{name} is in status {status}")
    except Exception as e:
        score_data.status = StatusEnum.FAILED
        log.error(e)
        log.error(f"Failed to get score and status for {namespace}/{name}")

    log.info(f"Model {namespace}/{name} has score data {score_data}")
    return score_data