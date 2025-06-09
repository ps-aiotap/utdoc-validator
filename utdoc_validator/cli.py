"""Command-line interface for the utdoc-validator."""

import argparse
import sys
import os
import logging
from typing import List
from utdoc_validator.unit_test_validator import UnitTestValidator
from utdoc_validator.generate_default_template import GenerateDefaultTemplate
from utdoc_validator.pr_file_checker import PRFileChecker
from utdoc_validator.utils import load_config
from utdoc_validator.logging_config import setup_logging
from utdoc_validator.constants import (
    DEFAULT_DOC_NAME,
    DEFAULT_CONFIG_FILE,
    DEFAULT_REQUIRED_SECTIONS,
    DEFAULT_PR_NUMBER,
    DEFAULT_REPO,
    EXIT_SUCCESS,
    EXIT_FAILURE,
    ENV_GITHUB_EVENT_NUMBER,
    ENV_GITHUB_REPO,
    ENV_GITHUB_REPOSITORY,
    ENV_GITHUB_TOKEN,
    ENV_PR_NUMBER,
    MSG_TEMPLATE_GENERATED,
    MSG_NO_PR_OR_PATH,
    MSG_STRICT_MODE_WARNING,
    MSG_VALIDATION_PASSED,
    MSG_VALIDATION_FAILED,
    MSG_UNEXPECTED_ERROR
)

# Set up logger
logger = logging.getLogger(__name__)


def load_required_sections(config_path: str) -> List[str]:
    """Load required section headers from config file if available.

    Args:
        config_path: Path to the configuration file

    Returns:
        List of required section headers
    """
    config = load_config(config_path)
    required = config.get("required_sections", DEFAULT_REQUIRED_SECTIONS)

    if not required or not isinstance(required, list):
        logger.warning(f"Invalid 'required_sections' in config file: {config_path}")
        return DEFAULT_REQUIRED_SECTIONS

    return required


def check_pr_file():
    """Default path when called without args – used in CI to check PRs."""
    pr_number = int(
        os.getenv(ENV_GITHUB_EVENT_NUMBER, os.getenv(ENV_PR_NUMBER, DEFAULT_PR_NUMBER))
    )
    repo = os.getenv(ENV_GITHUB_REPOSITORY, os.getenv(ENV_GITHUB_REPO, DEFAULT_REPO))
    token = os.getenv(ENV_GITHUB_TOKEN, "")

    # Load config
    config = load_config()
    doc_name = config.get("file_name", DEFAULT_DOC_NAME)

    logger.info(f"Checking PR #{pr_number} in repository {repo}")
    checker = PRFileChecker(pr_number=pr_number, repo=repo, token=token)
    result = checker.has_file(doc_name)
    sys.exit(EXIT_SUCCESS if result else EXIT_FAILURE)


def check_cli_file():
    """Process command line arguments and run the appropriate validation."""
    parser = argparse.ArgumentParser(
        description="Validate unit test documentation for PRs."
    )
    parser.add_argument("--pr", help="GitHub PR number")
    parser.add_argument("--path", help="Path to the test doc (e.g., unit_tests.md)")
    parser.add_argument(
        "--doc-name",
        help=f"Name of the doc file (defaults to {DEFAULT_DOC_NAME})",
        default=DEFAULT_DOC_NAME,
    )
    parser.add_argument(
        "--generate-template",
        action="store_true",
        help="Generate a default template and exit",
    )
    parser.add_argument(
        "--config",
        help=f"Path to config file ({DEFAULT_CONFIG_FILE})",
        default=DEFAULT_CONFIG_FILE,
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging",
    )
    parser.add_argument(
        "--log-file",
        help="Path to log file",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Enable strict mode (warnings are treated as errors)",
    )

    args = parser.parse_args()

    # Set up logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    setup_logging(level=log_level, log_file=args.log_file)

    # Load config
    config = load_config(args.config)

    # Override config with command line arguments
    if args.strict:
        config["strict_mode"] = True

    doc_path = args.path or args.doc_name
    logger.info(f"Using document path: {doc_path}")

    # Template generation mode
    if args.generate_template:
        logger.info(f"Generating template at {doc_path}")
        GenerateDefaultTemplate(doc_path)
        logger.info("Template generated successfully")
        print(MSG_TEMPLATE_GENERATED.format(doc_path))
        sys.exit(EXIT_SUCCESS)

    validator = UnitTestValidator(pr=args.pr, path=doc_path)
    validator.required_sections = config.get(
        "required_sections", DEFAULT_REQUIRED_SECTIONS
    )
    validator.placeholder_patterns = config.get(
        "placeholder_patterns", validator.placeholder_patterns
    )

    if args.path:
        logger.info(f"Validating file: {args.path}")
        result = validator.validate()
    elif args.pr:
        logger.info(f"Validating PR #{args.pr}")
        result = validator.validate_from_pr()
    else:
        logger.error("No path or PR number provided")
        print(MSG_NO_PR_OR_PATH)
        sys.exit(EXIT_FAILURE)

    # Handle warnings in strict mode
    if (
        result == EXIT_SUCCESS
        and config.get("strict_mode", False)
        and validator.warnings
        and not config.get("allow_warnings", True)
    ):
        logger.warning("Validation passed but warnings were found in strict mode")
        print(MSG_STRICT_MODE_WARNING)
        sys.exit(EXIT_FAILURE)

    if result == EXIT_SUCCESS:
        logger.info("Validation passed")
        print(MSG_VALIDATION_PASSED)
    else:
        logger.error("Validation failed")
        print(MSG_VALIDATION_FAILED)
    sys.exit(result)


def main():
    """Main entry point for the CLI."""
    try:
        if len(sys.argv) > 1:
            check_cli_file()
        else:
            check_pr_file()
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        print(MSG_UNEXPECTED_ERROR.format(e))
        sys.exit(EXIT_FAILURE)


if __name__ == "__main__":
    main()