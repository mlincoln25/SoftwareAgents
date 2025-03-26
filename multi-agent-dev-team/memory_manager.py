# memory_manager.py

import os
import base64
import requests

class MemoryManager:
    def __init__(self):
        """
        Initializes the MemoryManager with an in-memory storage dictionary.
        """
        self.memory = {}

    def save_to_memory(self, file_name, content):
        """
        Saves the given content to the in-memory storage with the specified file name.

        Args:
            file_name (str): The name of the file to be used as the key.
            content (str): The content to be stored.
        """
        self.memory[file_name] = content

    def retrieve_from_memory(self, file_name):
        """
        Retrieves the content stored in memory for the given file name.

        Args:
            file_name (str): The name of the file whose content is to be retrieved.

        Returns:
            str: The content stored in memory, or None if the file does not exist.
        """
        return self.memory.get(file_name)

    def load_repository_into_memory(self, owner, repo, branch="main"):
        """
        Loads all files from the specified GitHub repository into memory.

        Args:
            owner (str): The GitHub username or organization name.
            repo (str): The name of the repository.
            branch (str): The branch to pull the files from. Defaults to 'main'.

        Raises:
            ValueError: If the GITHUB_TOKEN is not set in the environment variables.
            RuntimeError: If there's an error fetching files from GitHub.
        """
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            raise ValueError("No GITHUB_TOKEN found in environment.")

        # Fetch the repository contents
        url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json",
        }

        response = requests.get(url, headers=headers)
        if not response.ok:
            raise RuntimeError(f"Failed to fetch repository contents: {response.status_code}\n{response.text}")

        tree = response.json().get("tree", [])
        for item in tree:
            if item["type"] == "blob":  # It's a file
                file_path = item["path"]
                file_content = self._fetch_file_content(owner, repo, file_path, branch, headers)
                self.save_to_memory(file_path, file_content)

    def _fetch_file_content(self, owner, repo, file_path, branch, headers):
        """
        Fetches the content of a specific file from the GitHub repository.

        Args:
            owner (str): The GitHub username or organization name.
            repo (str): The name of the repository.
            file_path (str): The path to the file in the repository.
            branch (str): The branch to pull the file from.
            headers (dict): The headers for the GitHub API request.

        Returns:
            str: The content of the file.

        Raises:
            RuntimeError: If there's an error fetching the file content from GitHub.
        """
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}?ref={branch}"
        response = requests.get(url, headers=headers)
        if not response.ok:
            raise RuntimeError(f"Failed to fetch file {file_path}: {response.status_code}\n{response.text}")

        data = response.json()
        content_bytes = base64.b64decode(data["content"])
        return content_bytes.decode("utf-8")
