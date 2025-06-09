"""Tests for the PRFileChecker module."""

import pytest
from unittest.mock import patch, MagicMock
from utdoc_validator.pr_file_checker import PRFileChecker
from utdoc_validator.constants import DEFAULT_DOC_NAME


@patch('utdoc_validator.pr_file_checker.GitHubAPIClient')
@patch('utdoc_validator.pr_file_checker.GitHubCLIClient')
def test_get_pr_files_api_success(mock_cli_client, mock_api_client):
    """Test getting PR files with successful API call."""
    mock_api_instance = MagicMock()
    mock_api_client.return_value = mock_api_instance
    mock_api_instance.get_pr_files.return_value = ["file1.py", DEFAULT_DOC_NAME]
    
    mock_cli_instance = MagicMock()
    mock_cli_client.return_value = mock_cli_instance
    
    checker = PRFileChecker(pr_number=123, repo="user/repo", token="token")
    files = checker.get_pr_files()
    
    assert files == ["file1.py", DEFAULT_DOC_NAME]
    mock_api_instance.get_pr_files.assert_called_once_with("user/repo", 123)
    mock_cli_instance.get_pr_files.assert_not_called()


@patch('utdoc_validator.pr_file_checker.GitHubAPIClient')
@patch('utdoc_validator.pr_file_checker.GitHubCLIClient')
def test_get_pr_files_api_failure_cli_success(mock_cli_client, mock_api_client):
    """Test getting PR files with API failure but CLI success."""
    mock_api_instance = MagicMock()
    mock_api_client.return_value = mock_api_instance
    mock_api_instance.get_pr_files.return_value = None
    
    mock_cli_instance = MagicMock()
    mock_cli_client.return_value = mock_cli_instance
    mock_cli_instance.get_pr_files.return_value = ["file1.py", DEFAULT_DOC_NAME]
    
    checker = PRFileChecker(pr_number=123, repo="user/repo", token="token")
    files = checker.get_pr_files()
    
    assert files == ["file1.py", DEFAULT_DOC_NAME]
    mock_api_instance.get_pr_files.assert_called_once()
    mock_cli_instance.get_pr_files.assert_called_once_with(123)


@patch('utdoc_validator.pr_file_checker.GitHubAPIClient', return_value=None)
@patch('utdoc_validator.pr_file_checker.GitHubCLIClient')
def test_get_pr_files_no_token_cli_success(mock_cli_client, _):
    """Test getting PR files with no token but CLI success."""
    mock_cli_instance = MagicMock()
    mock_cli_client.return_value = mock_cli_instance
    mock_cli_instance.get_pr_files.return_value = ["file1.py", DEFAULT_DOC_NAME]
    
    checker = PRFileChecker(pr_number=123, repo="user/repo", token=None)
    files = checker.get_pr_files()
    
    assert files == ["file1.py", DEFAULT_DOC_NAME]
    mock_cli_instance.get_pr_files.assert_called_once_with(123)


def test_has_file_true():
    """Test has_file when file exists."""
    checker = PRFileChecker(pr_number=123, repo="user/repo")
    
    with patch.object(checker, 'get_pr_files', return_value=["file1.py", DEFAULT_DOC_NAME]):
        result = checker.has_file(DEFAULT_DOC_NAME)
        assert result is True


def test_has_file_false():
    """Test has_file when file doesn't exist."""
    checker = PRFileChecker(pr_number=123, repo="user/repo")
    
    with patch.object(checker, 'get_pr_files', return_value=["file1.py", "file2.py"]):
        result = checker.has_file(DEFAULT_DOC_NAME)
        assert result is False


def test_has_file_no_files():
    """Test has_file when no files can be retrieved."""
    checker = PRFileChecker(pr_number=123, repo="user/repo")
    
    with patch.object(checker, 'get_pr_files', return_value=None):
        result = checker.has_file(DEFAULT_DOC_NAME)
        assert result is False