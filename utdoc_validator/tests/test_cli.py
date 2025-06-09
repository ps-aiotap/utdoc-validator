# tests/test_cli.py
"""Tests for the CLI module."""

import os
import sys
import pytest
from unittest.mock import patch, MagicMock
from utdoc_validator.cli import check_cli_file, load_required_sections
from utdoc_validator.constants import DEFAULT_REQUIRED_SECTIONS


def test_load_required_sections_with_valid_config(tmp_path):
    """Test loading required sections from a valid config file."""
    config_path = tmp_path / ".utdocconfig"
    with open(config_path, "w") as f:
        f.write('{"required_sections": ["## Custom Section", "## Another Section"]}')

    sections = load_required_sections(str(config_path))
    assert sections == ["## Custom Section", "## Another Section"]


def test_load_required_sections_with_invalid_config(tmp_path):
    """Test loading required sections from an invalid config file."""
    config_path = tmp_path / ".utdocconfig"
    with open(config_path, "w") as f:
        f.write('{"required_sections": "not a list"}')

    sections = load_required_sections(str(config_path))
    assert sections == DEFAULT_REQUIRED_SECTIONS


def test_load_required_sections_with_nonexistent_config():
    """Test loading required sections when config file doesn't exist."""
    sections = load_required_sections("/nonexistent/path")
    assert sections == DEFAULT_REQUIRED_SECTIONS


@patch("utdoc_validator.cli.UnitTestValidator")
def test_check_cli_file_with_path(mock_validator):
    """Test CLI with --path argument."""
    mock_instance = MagicMock()
    mock_validator.return_value = mock_instance
    mock_instance.validate.return_value = 0

    with patch.object(sys, "argv", ["utdoc_validator", "--path", "test.md"]):
        with patch("sys.exit") as mock_exit:
            check_cli_file()
            mock_exit.assert_called_once_with(0)

    mock_validator.assert_called_once()
    mock_instance.validate.assert_called_once()
