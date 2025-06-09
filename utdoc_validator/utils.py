"""Utility functions for the utdoc-validator."""

import os
import re
from typing import List, Optional, Dict, Any
import json
from utdoc_validator.constants import (
    DEFAULT_CONFIG_FILE,
    DEFAULT_REQUIRED_SECTIONS,
    ENV_GITHUB_TOKEN,
    PLACEHOLDER_PATTERNS,
    DEFAULT_DOC_NAME,
    DEFAULT_STRICT_MODE,
    DEFAULT_ALLOW_WARNINGS,
    DEFAULT_IGNORE_FILES,
)


def load_config(config_path: str = DEFAULT_CONFIG_FILE) -> Dict[str, Any]:
    """Load configuration from a JSON file.

    Args:
        config_path: Path to the configuration file

    Returns:
        Dictionary containing configuration values
    """

    default_config = {
        "required_sections": DEFAULT_REQUIRED_SECTIONS,
        "placeholder_patterns": PLACEHOLDER_PATTERNS,
        "file_name": DEFAULT_DOC_NAME,
        "strict_mode": DEFAULT_STRICT_MODE,
        "allow_warnings": DEFAULT_ALLOW_WARNINGS,
        "ignore_files": DEFAULT_IGNORE_FILES,
    }
    if not os.path.exists(config_path):
        return default_config

    try:
        with open(config_path, "r") as f:
            config = json.load(f)

        # Merge with defaults for any missing keys
        for key, value in default_config.items():
            if key not in config:
                config[key] = value

        return config
    except (json.JSONDecodeError, IOError) as e:
        print(f"⚠️ Error loading config file: {e}")
        return default_config


def find_placeholders(content: str, patterns: List[str]) -> List[str]:
    """Find placeholder patterns in content.

    Args:
        content: Text content to search
        patterns: List of regex patterns to search for

    Returns:
        List of found placeholder matches
    """
    found = []
    for pattern in patterns:
        if re.search(pattern, content):
            found.append(pattern)
    return found


def get_github_token() -> Optional[str]:
    """Get GitHub token from environment variables.

    Returns:
        GitHub token if available, None otherwise
    """
    return os.getenv(ENV_GITHUB_TOKEN)
