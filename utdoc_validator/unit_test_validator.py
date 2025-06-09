"""Unit test documentation validator module."""

import os
import re
import logging
import tempfile
from typing import List, Optional
from utdoc_validator.utils import find_placeholders
from utdoc_validator.constants import (
    DEFAULT_REQUIRED_SECTIONS,
    PLACEHOLDER_PATTERNS,
    EXIT_SUCCESS,
    EXIT_FAILURE,
    DEFAULT_REPO,
    ENV_GITHUB_REPO,
    ENV_GITHUB_TOKEN,
    GITHUB_API_REPOS_URL,
    GITHUB_API_AUTH_PREFIX,
    GITHUB_API_RAW_ACCEPT_HEADER,
    GH_CLI_COMMAND,
    GH_CLI_PR_SUBCOMMAND,
    GH_CLI_VIEW_SUBCOMMAND,
    GH_CLI_JSON_FLAG,
    GH_CLI_JQ_FLAG,
    GH_CLI_REPO_FLAG,
    MSG_FILE_NOT_FOUND,
    MSG_ERROR_READING_FILE,
    MSG_MISSING_SECTION,
    MSG_PLACEHOLDER_FOUND,
    MSG_NO_PR_NUMBER,
    MSG_INVALID_PR_NUMBER,
    MSG_NO_FILES_RETRIEVED,
    MSG_NO_DOC_FILE_FOUND,
    MSG_FAILED_GET_CONTENT
)
from utdoc_validator.pr_file_checker import PRFileChecker

# Set up logger
logger = logging.getLogger(__name__)


class UnitTestValidator:
    """Validates unit test documentation files for required sections and placeholders."""
    
    def __init__(self, pr: Optional[str], path: str):
        """Initialize the validator.
        
        Args:
            pr: Pull request number (optional)
            path: Path to the documentation file
        """
        self.pr = pr
        self.path = path
        self.placeholder_patterns = PLACEHOLDER_PATTERNS
        self.required_sections = DEFAULT_REQUIRED_SECTIONS
        self.errors = []
        self.warnings = []

    def validate(self) -> int:
        """Validate the documentation file.
        
        Returns:
            EXIT_SUCCESS if validation passes, EXIT_FAILURE otherwise
        """
        if not os.path.exists(self.path):
            logger.error(f"File not found: {self.path}")
            print(MSG_FILE_NOT_FOUND.format(self.path))
            return EXIT_FAILURE

        try:
            with open(self.path, "r") as f:
                content = f.read()
            logger.info(f"Successfully read file: {self.path}")
        except IOError as e:
            logger.error(f"Error reading file: {e}")
            print(MSG_ERROR_READING_FILE.format(e))
            return EXIT_FAILURE

        success = self._validate_required_sections(content)
        self._check_placeholders(content)

        return EXIT_SUCCESS if success else EXIT_FAILURE

    def _validate_required_sections(self, content: str) -> bool:
        """Check if all required sections are present in the content.
        
        Args:
            content: Documentation file content
            
        Returns:
            True if all required sections are present, False otherwise
        """
        success = True
        for section in self.required_sections:
            if section not in content:
                logger.warning(f"Missing section: {section}")
                print(MSG_MISSING_SECTION.format(section))
                self.errors.append(f"Missing section: {section}")
                success = False
            else:
                logger.info(f"Found required section: {section}")
        return success

    def _check_placeholders(self, content: str) -> None:
        """Check for placeholder text in the content.
        
        Args:
            content: Documentation file content
        """
        found_placeholders = find_placeholders(content, self.placeholder_patterns)
        for placeholder in found_placeholders:
            logger.warning(f"Placeholder found: '{placeholder}' present in document")
            print(MSG_PLACEHOLDER_FOUND.format(placeholder))
            self.warnings.append(f"Placeholder found: {placeholder}")

    def validate_from_pr(self) -> int:
        """Validate documentation from a pull request.
        
        Returns:
            EXIT_SUCCESS if validation passes, EXIT_FAILURE otherwise
        """
        if not self.pr:
            logger.error("No PR number provided")
            print(MSG_NO_PR_NUMBER)
            return EXIT_FAILURE
            
        try:
            pr_number = int(self.pr)
        except ValueError:
            logger.error(f"Invalid PR number: {self.pr}")
            print(MSG_INVALID_PR_NUMBER.format(self.pr))
            return EXIT_FAILURE
            
        logger.info(f"Validating PR #{pr_number}")
        
        # Get repo from environment or use default
        repo = os.getenv(ENV_GITHUB_REPO, DEFAULT_REPO)
        token = os.getenv(ENV_GITHUB_TOKEN, "")
        
        # Create PR file checker
        checker = PRFileChecker(pr_number=pr_number, repo=repo, token=token)
        
        # Get files from PR
        files = checker.get_pr_files()
        if not files:
            logger.error(f"Could not retrieve files for PR #{pr_number}")
            print(MSG_NO_FILES_RETRIEVED.format(pr_number))
            return EXIT_FAILURE
            
        # Look for unit test documentation file
        doc_file = None
        for file in files:
            if file.endswith(self.path):
                doc_file = file
                break
                
        if not doc_file:
            logger.error(f"No documentation file found in PR #{pr_number}")
            print(MSG_NO_DOC_FILE_FOUND.format(pr_number))
            return EXIT_FAILURE
            
        # Download the file content
        content = self._get_file_content(pr_number, repo, doc_file, token)
        if not content:
            return EXIT_FAILURE
            
        # Create a temporary file with the content
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp:
            temp.write(content)
            temp_path = temp.name
            
        try:
            # Save the original path
            original_path = self.path
            # Set the path to the temporary file
            self.path = temp_path
            # Validate the file
            result = self.validate()
            # Restore the original path
            self.path = original_path
            
            return result
        finally:
            # Clean up the temporary file
            os.unlink(temp_path)
    
    def _get_file_content(self, pr_number: int, repo: str, file_path: str, token: str) -> Optional[str]:
        """Get file content from a PR.
        
        Args:
            pr_number: Pull request number
            repo: Repository name
            file_path: Path to the file
            token: GitHub token
            
        Returns:
            File content or None if retrieval fails
        """
        # Try to get content via GitHub API
        if token:
            try:
                import requests
                url = f"{GITHUB_API_REPOS_URL}/{repo}/contents/{file_path}?ref=refs/pull/{pr_number}/head"
                headers = {
                    "Authorization": f"{GITHUB_API_AUTH_PREFIX}{token}",
                    "Accept": GITHUB_API_RAW_ACCEPT_HEADER,
                }
                response = requests.get(url=url, headers=headers)
                response.raise_for_status()
                logger.info(f"Successfully retrieved file content via API: {file_path}")
                return response.text
            except Exception as e:
                logger.warning(f"Failed to get file content via API: {e}")
        
        # Fallback to GitHub CLI
        try:
            import subprocess
            result = subprocess.run(
                [
                    GH_CLI_COMMAND, GH_CLI_PR_SUBCOMMAND, GH_CLI_VIEW_SUBCOMMAND,
                    str(pr_number),
                    GH_CLI_REPO_FLAG, repo,
                    GH_CLI_JSON_FLAG, "files",
                    GH_CLI_JQ_FLAG, f".files[] | select(.path == \"{file_path}\") | .contents"
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            logger.info(f"Successfully retrieved file content via CLI: {file_path}")
            return result.stdout
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to get file content via CLI: {e.stderr}")
            print(MSG_FAILED_GET_CONTENT.format(e.stderr))
            return None