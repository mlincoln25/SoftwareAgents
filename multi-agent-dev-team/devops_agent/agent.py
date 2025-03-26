# devops_agent/agent.py

import os
import base64
import requests
from agents import Agent

GITHUB_API_BASE = "https://api.github.com"

def read_file_from_github(owner, repo, file_path, branch="main"):
    """
    Fetches the contents of a file from a GitHub repository.
    """
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("No GITHUB_TOKEN found in environment.")

    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/contents/{file_path}?ref={branch}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    response = requests.get(url, headers=headers)
    if not response.ok:
        raise RuntimeError(f"Failed to fetch file: {response.status_code}\n{response.text}")

    data = response.json()
    content_bytes = base64.b64decode(data["content"])
    return content_bytes.decode("utf-8")

def update_file_on_github(owner, repo, file_path, new_content, commit_message, branch="main"):
    """
    Updates or creates a file in a GitHub repository with new content.
    """
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("No GITHUB_TOKEN found in environment.")

    # Get the file's current SHA if it exists
    get_url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/contents/{file_path}?ref={branch}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    sha = None
    get_res = requests.get(get_url, headers=headers)
    if get_res.ok:
        sha = get_res.json()["sha"]

    # Encode new content and prepare payload
    encoded_content = base64.b64encode(new_content.encode("utf-8")).decode("utf-8")
    payload = {
        "message": commit_message,
        "content": encoded_content,
        "branch": branch,
    }
    if sha:
        payload["sha"] = sha

    # Update the file on GitHub
    put_url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/contents/{file_path}"
    put_res = requests.put(put_url, headers=headers, json=payload)
    if not put_res.ok:
        raise RuntimeError(f"Failed to update file: {put_res.status_code}\n{put_res.text}")

    return put_res.json()

devops_agent = Agent(
    name="DevOps Agent",
    instructions=(
        "You manage interactions with GitHub repositories, including reading from and writing to them. "
        "Ensure that all operations are performed securely and accurately."
    ),
    handoff_description="Handles GitHub repository interactions."
)
