"""Tests for the UnitTestValidator module."""

import os
import pytest
from unittest.mock import patch, mock_open
from utdoc_validator.unit_test_validator import UnitTestValidator
from utdoc_validator.constants import EXIT_SUCCESS, EXIT_FAILURE


def test_validate_file_not_found():
    """Test validation when file doesn't exist."""
    validator = UnitTestValidator(pr=None, path="/nonexistent/path")
    
    with patch('os.path.exists', return_value=False):
        result = validator.validate()
        assert result == EXIT_FAILURE


def test_validate_missing_sections():
    """Test validation when required sections are missing."""
    validator = UnitTestValidator(pr=None, path="test.md")
    validator.required_sections = ["## Test Cases", "## Coverage"]
    
    with patch('os.path.exists', return_value=True):
        with patch('builtins.open', mock_open(read_data="# Some other content")):
            result = validator.validate()
            assert result == EXIT_FAILURE


def test_validate_with_placeholders():
    """Test validation when placeholders are present."""
    validator = UnitTestValidator(pr=None, path="test.md")
    validator.required_sections = ["## Test Cases"]
    
    with patch('os.path.exists', return_value=True):
        with patch('builtins.open', mock_open(read_data="## Test Cases\nThis is WIP")):
            with patch('builtins.print') as mock_print:
                result = validator.validate()
                assert result == EXIT_SUCCESS
                mock_print.assert_any_call("⚠️ Placeholder found: '\\bWIP\\b' present in document.")


def test_validate_success():
    """Test successful validation."""
    validator = UnitTestValidator(pr=None, path="test.md")
    validator.required_sections = ["## Test Cases", "## Coverage"]
    
    with patch('os.path.exists', return_value=True):
        with patch('builtins.open', mock_open(read_data="## Test Cases\nSome tests\n## Coverage\n100%")):
            result = validator.validate()
            assert result == EXIT_SUCCESS