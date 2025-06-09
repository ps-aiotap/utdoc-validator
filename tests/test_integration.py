"""Integration tests for the utdoc-validator."""

import os
import pytest
import tempfile
from unittest.mock import patch
import subprocess
from utdoc_validator.constants import EXIT_SUCCESS, EXIT_FAILURE


def test_cli_validate_file_success():
    """Test CLI validation with a valid file."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp:
        temp.write("## Test Cases\nTest case 1\n\n## Coverage\n100%\n")
        temp_path = temp.name
    
    try:
        result = subprocess.run(
            ["python", "-m", "utdoc_validator.cli", "--path", temp_path],
            capture_output=True,
            text=True
        )
        assert result.returncode == EXIT_SUCCESS
        assert "✅ Unit test validation passed" in result.stdout
    finally:
        os.unlink(temp_path)


def test_cli_validate_file_missing_section():
    """Test CLI validation with a file missing required sections."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp:
        temp.write("# Some content without required sections")
        temp_path = temp.name
    
    try:
        result = subprocess.run(
            ["python", "-m", "utdoc_validator.cli", "--path", temp_path],
            capture_output=True,
            text=True
        )
        assert result.returncode == EXIT_FAILURE
        assert "❌ Missing section: ## Test Cases" in result.stdout
    finally:
        os.unlink(temp_path)


def test_cli_generate_template():
    """Test CLI template generation."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = os.path.join(temp_dir, "unit_tests.md")
        
        result = subprocess.run(
            ["python", "-m", "utdoc_validator.cli", "--generate-template", "--path", temp_path],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == EXIT_SUCCESS
        assert "✅ Template generated" in result.stdout
        assert os.path.exists(temp_path)
        
        with open(temp_path, 'r') as f:
            content = f.read()
            assert "## Test Cases" in content
            assert "## Coverage" in content


@patch.dict('os.environ', {"PR_NUMBER": "123", "GITHUB_REPO": "user/repo"})
def test_cli_no_args_uses_env_vars():
    """Test CLI with no args uses environment variables."""
    with patch('utdoc_validator.pr_file_checker.PRFileChecker') as mock_checker:
        mock_instance = mock_checker.return_value
        mock_instance.has_file.return_value = True
        
        result = subprocess.run(
            ["python", "-m", "utdoc_validator.cli"],
            capture_output=True,
            text=True
        )
        
        mock_checker.assert_called_once_with(pr_number=123, repo="user/repo", token="")
        mock_instance.has_file.assert_called_once()