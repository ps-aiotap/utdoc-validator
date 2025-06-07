import argparse
import sys
import os
import json
from typing import List
from unit_test_validator import UnitTestValidator
from generate_default_template import GenerateDefaultTemplate
from pr_file_checker import PRFileChecker


DEFAULT_DOC_NAME = "unit_tests.md"
DEFAULT_CONFIG_FILE = ".utdocconfig"
DEFAULT_REQUIRED_SECTIONS = ["## Test Cases", "## Coverage"]


def load_required_sections(config_path: str) -> List[str]:
    """Load required section headers from config file if available."""
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
                required = config.get("required_sections", DEFAULT_REQUIRED_SECTIONS)
                if required and isinstance(required, list):
                    return required

                print(f"⚠️ Invalid 'required_sections' in config file: {config_path}")
        except Exception as e:
            print(f"⚠️ Failed to load config from {config_path}: {e}")
    return DEFAULT_REQUIRED_SECTIONS


def check_pr_file():
    """Default path when called without args – used in CI to check PRs."""
    pr_number = int(os.getenv("PR_NUMBER", "123"))
    repo = os.getenv("GITHUB_REPO", "youruser/yourrepo")
    token = os.getenv("GITHUB_TOKEN", "")
    checker = PRFileChecker(pr_number=pr_number, repo=repo, token=token)
    checker.has_file(DEFAULT_DOC_NAME)


def check_cli_file():
    parser = argparse.ArgumentParser(
        description="Validate unit test documentation for PRs."
    )
    parser.add_argument("--pr", help="GitHub PR number")
    parser.add_argument("--path", help="Path to the test doc (e.g., unit_tests.md)")
    parser.add_argument(
        "--doc-name",
        help="Name of the doc file (defaults to unit_tests.md)",
        default=DEFAULT_DOC_NAME,
    )
    parser.add_argument(
        "--generate-template",
        action="store_true",
        help="Generate a default template and exit",
    )
    parser.add_argument(
        "--config",
        help="Path to config file (.utdocconfig)",
        default=DEFAULT_CONFIG_FILE,
    )

    args = parser.parse_args()

    doc_path = args.path or args.doc_name

    # Template generation mode
    if args.generate_template:
        GenerateDefaultTemplate(doc_path)
        print(f"✅ Template generated at: {doc_path}")
        sys.exit(0)

    validator = UnitTestValidator(pr=args.pr, path=doc_path)
    validator.required_sections = load_required_sections(args.config)

    if args.path:
        result = validator.validate()
    elif args.pr:
        result = validator.validate_from_pr()
    else:
        print("⚠️ Please provide --pr or --path")
        sys.exit(1)

    if result == 0:
        print("✅ Unit test validation passed")
    else:
        print("❌ Unit test validation failed")
    sys.exit(result)


def main():
    if len(sys.argv) > 1:
        check_cli_file()
    else:
        check_pr_file()


if __name__ == "__main__":
    main()
