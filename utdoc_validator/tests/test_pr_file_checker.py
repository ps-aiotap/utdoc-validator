# tests/test_pr_file_checker.py
"""Tests for the PRFileChecker module."""

import pytest
from unittest.mock import patch, MagicMock
from utdoc_validator.pr_file_checker import PRFileChecker


def test_fetch_files_from_api_success():
    """Test successful API fetch."""
    checker = PRFileChecker(pr_number=123, repo="user/repo", token="token")

    mock_response = MagicMock()
    mock_response.json.return_value = [
        {"filename": "file1.py"},
        {"filename": "unit_tests.md"},
    ]

    with patch("requests.get", return_value=mock_response):
        files = checker.fetch_files_from_api()
        assert files == ["file1.py", "unit_tests.md"]


def test_fetch_files_from_api_no_token():
    """Test API fetch with no token."""
    checker = PRFileChecker(pr_number=123, repo="user/repo", token=None)

    with patch("os.getenv", return_value=None):
        files = checker.fetch_files_from_api()
        assert files is None


def test_fetch_files_from_cli_success():
    """Test successful CLI fetch."""
    checker = PRFileChecker(pr_number=123, repo="user/repo")

    mock_result = MagicMock()
    mock_result.stdout = "file1.py\nunit_tests.md\n"

    with patch("subprocess.run", return_value=mock_result):
        files = checker.fetch_files_from_cli()
        assert files == ["file1.py", "unit_tests.md"]


def test_has_file_true():
    """Test has_file when file exists."""
    checker = PRFileChecker(pr_number=123, repo="user/repo")

    with patch.object(
        checker, "get_pr_files", return_value=["file1.py", "unit_tests.md"]
    ):
        result = checker.has_file("unit_tests.md")
        assert result is True


def test_has_file_false():
    """Test has_file when file doesn't exist."""
    checker = PRFileChecker(pr_number=123, repo="user/repo")

    with patch.object(checker, "get_pr_files", return_value=["file1.py", "file2.py"]):
        result = checker.has_file("unit_tests.md")
        assert result is False
