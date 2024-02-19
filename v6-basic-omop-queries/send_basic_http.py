import os
import requests

from typing import Any
from time import sleep

from vantage6.algorithm.tools.util import get_env_var, error, info
from vantage6.algorithm.tools.decorators import _get_user_database_labels


def send_http_person_count() -> Any:

    labels = _get_user_database_labels()
    if len(labels) > 1:
        error("Multiple databases found, but only one expected")
        exit(1)
    label = labels[0]
    uri = get_env_var(f"{label.upper()}_DATABASE_URI")

    if not uri:
        error(f"Database URI for {label} not found")
        exit(1)

    # kick of the celery count task
    info(f"Connecting to: {uri}")
    task = requests.get(f"{uri}/celery")
    if task.status_code != 200:
        error(f"Failed to start the celery task: {task.text}")
        exit(1)
    task_id = task.json()["id"]

    # wait for the result
    retries = 0
    while _get_state(uri, task_id) != "SUCCESS" and retries < 120:
        info(f"Task {task_id} is still running")
        sleep(1)
        retries += 1

    return {'count': _get_result(uri, task_id)}

def _get_result(uri: str, task_id: str) -> Any:
    body_ = requests.get(f"{uri}/result/{task_id}").json()
    return body_.get("value")

def _get_state(uri: str, task_id: str) -> Any:
    body_ = requests.get(f"{uri}/result/{task_id}").json()
    return body_.get("state")
