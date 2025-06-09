"""Tests for the GenerateDefaultTemplate module."""

import os
import pytest
from unittest.mock import patch, mock_open
from utdoc_validator.generate_default_template import GenerateDefaultTemplate


def test_generate_default_template():
    """Test template generation."""
    mock_open_file = mock_open()
    
    with patch('builtins.open', mock_open_file):
        GenerateDefaultTemplate("test.md")
    
    mock_open_file.assert_called_once_with("test.md", "w")
    written_content = mock_open_file().write.call_args[0][0]
    
    assert "## Test Cases" in written_content
    assert "## Coverage" in written_content
    assert "## Edge Cases" in written_content