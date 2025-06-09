"""Pull request file checker module."""

import os
from typing import Optional, List
from utdoc_validator.constants import (
    DEFAULT_DOC_NAME,
    ENV_GITHUB_TOKEN,
    MSG_NO_FILES_RETRIEVED
)
from utdoc_validator.github_clients import GitHubAPIClient, GitHubCLIClient


class PRFileChecker:
    """Checks for the presence of specific files in a GitHub pull request."""
    
    def __init__(self, pr_number: int, repo: str, token: Optional[str] = None):
        """Initialize the PR file checker.
        
        Args:
            pr_number: Pull request number
            repo: Repository name in format "username/repo"
            token: GitHub API token (optional)
        """
        self.pr_number = pr_number
        self.repo = repo
        self.token = token or os.getenv(ENV_GITHUB_TOKEN)
        self.api_client = GitHubAPIClient(self.token) if self.token else None
        self.cli_client = GitHubCLIClient()

    def get_pr_files(self) -> Optional[List[str]]:
        """Get list of files in the pull request.
        
        Returns:
            List of filenames or None if both API and CLI methods fail
        """
        files = None
        if self.api_client:
            files = self.api_client.get_pr_files(self.repo, self.pr_number)
        
        if not files:
            files = self.cli_client.get_pr_files(self.pr_number)
            
        return files

    def has_file(self, target_file: str = DEFAULT_DOC_NAME) -> bool:
        """Check if the pull request contains a specific file.
        
        Args:
            target_file: Filename to look for
            
        Returns:
            True if file is found, False otherwise
        """
        files = self.get_pr_files()

        if not files:
            print(MSG_NO_FILES_RETRIEVED)
            return False

        found = any(f.endswith(target_file) for f in files)

        print(
            f"{'✅' if found else '❌'} `{target_file}` {'found' if found else 'missing'}"
        )

        return found