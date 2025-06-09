"""Tests for the utils module."""

import os
import json
import pytest
from unittest.mock import patch, mock_open
from utdoc_validator.utils import load_config, find_placeholders, get_github_token
from utdoc_validator.constants import DEFAULT_REQUIRED_SECTIONS


def test_load_config_file_not_found():
    """Test loading config when file doesn't exist."""
    with patch('os.path.exists', return_value=False):
        config = load_config("/nonexistent/path")
        assert config == {"required_sections": DEFAULT_REQUIRED_SECTIONS}


def test_load_config_valid_file(tmp_path):
    """Test loading a valid config file."""
    config_data = {
        "required_sections": ["## Custom Section", "## Another Section"]
    }
    config_path = tmp_path / ".utdocconfig"
    
    with open(config_path, "w") as f:
        json.dump(config_data, f)
    
    config = load_config(str(config_path))
    assert config == config_data


def test_load_config_invalid_json():
    """Test loading an invalid JSON config file."""
    with patch('os.path.exists', return_value=True):
        with patch('builtins.open', mock_open(read_data="invalid json")):
            config = load_config()
            assert config == {"required_sections": DEFAULT_REQUIRED_SECTIONS}


def test_find_placeholders():
    """Test finding placeholder patterns in content."""
    content = "This is a WIP document with TBD sections."
    patterns = [r"\bWIP\b", r"\bTBD\b", r"\bTo be added\b"]
    
    found = find_placeholders(content, patterns)
    assert r"\bWIP\b" in found
    assert r"\bTBD\b" in found
    assert r"\bTo be added\b" not in found


def test_get_github_token():
    """Test getting GitHub token from environment."""
    with patch.dict(os.environ, {"GITHUB_TOKEN": "test-token"}):
        token = get_github_token()
        assert token == "test-token"
    
    with patch.dict(os.environ, {}, clear=True):
        token = get_github_token()
        assert token is None