"""Tests for the GitHub clients module."""

import pytest
from unittest.mock import patch, MagicMock
from utdoc_validator.github_clients import GitHubAPIClient, GitHubCLIClient


def test_github_api_client_get_pr_files_success():
    """Test successful API fetch."""
    client = GitHubAPIClient(token="test-token")
    
    mock_response = MagicMock()
    mock_response.json.return_value = [{"filename": "file1.py"}, {"filename": "unit_tests.md"}]
    
    with patch('requests.get', return_value=mock_response):
        files = client.get_pr_files("user/repo", 123)
        assert files == ["file1.py", "unit_tests.md"]


def test_github_api_client_get_pr_files_no_token():
    """Test API fetch with no token."""
    client = GitHubAPIClient(token="")
    files = client.get_pr_files("user/repo", 123)
    assert files is None


def test_github_api_client_get_pr_files_request_error():
    """Test API fetch with request error."""
    client = GitHubAPIClient(token="test-token")
    
    with patch('requests.get', side_effect=requests.RequestException("Error")):
        files = client.get_pr_files("user/repo", 123)
        assert files is None


def test_github_cli_client_get_pr_files_success():
    """Test successful CLI fetch."""
    client = GitHubCLIClient()
    
    mock_result = MagicMock()
    mock_result.stdout = "file1.py\nunit_tests.md\n"
    
    with patch('subprocess.run', return_value=mock_result):
        files = client.get_pr_files(123)
        assert files == ["file1.py", "unit_tests.md"]


def test_github_cli_client_get_pr_files_error():
    """Test CLI fetch with error."""
    client = GitHubCLIClient()
    
    with patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, "gh", stderr="Error")):
        files = client.get_pr_files(123)
        assert files is None