"""GitHub API and CLI clients for fetching PR information."""

import os
import subprocess
import requests
from typing import Optional, List
from utdoc_validator.constants import (
    GITHUB_API_REPOS_URL,
    GITHUB_API_AUTH_PREFIX,
    GITHUB_API_ACCEPT_HEADER,
    GH_CLI_COMMAND,
    GH_CLI_PR_SUBCOMMAND,
    GH_CLI_VIEW_SUBCOMMAND,
    GH_CLI_JSON_FLAG,
    GH_CLI_JQ_FLAG,
    MSG_API_TOKEN_NOT_PROVIDED,
    MSG_API_FAILED,
    MSG_CLI_FAILED
)


class GitHubAPIClient:
    """Client for interacting with GitHub API."""
    
    def __init__(self, token: str):
        """Initialize with GitHub API token.
        
        Args:
            token: GitHub API token
        """
        self.token = token
        
    def get_pr_files(self, repo: str, pr_number: int) -> Optional[List[str]]:
        """Get list of files in a pull request using GitHub API.
        
        Args:
            repo: Repository name in format "username/repo"
            pr_number: Pull request number
            
        Returns:
            List of filenames or None if request fails
        """
        if not self.token:
            print(MSG_API_TOKEN_NOT_PROVIDED)
            return None

        url = f"{GITHUB_API_REPOS_URL}/{repo}/pulls/{pr_number}/files"
        headers = {
            "Authorization": f"{GITHUB_API_AUTH_PREFIX}{self.token}",
            "Accept": GITHUB_API_ACCEPT_HEADER,
        }
        try:
            response = requests.get(url=url, headers=headers)
            response.raise_for_status()
            return [file["filename"] for file in response.json()]
        except requests.RequestException as e:
            print(MSG_API_FAILED.format(e))
            return None


class GitHubCLIClient:
    """Client for interacting with GitHub CLI."""
    
    def get_pr_files(self, pr_number: int) -> Optional[List[str]]:
        """Get list of files in a pull request using GitHub CLI.
        
        Args:
            pr_number: Pull request number
            
        Returns:
            List of filenames or None if command fails
        """
        try:
            result = subprocess.run(
                [
                    GH_CLI_COMMAND,
                    GH_CLI_PR_SUBCOMMAND,
                    GH_CLI_VIEW_SUBCOMMAND,
                    str(pr_number),
                    GH_CLI_JSON_FLAG,
                    "files",
                    GH_CLI_JQ_FLAG,
                    ".files[].path",
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            return result.stdout.strip().splitlines()
        except subprocess.CalledProcessError as e:
            print(MSG_CLI_FAILED.format(e.stderr))
            return None