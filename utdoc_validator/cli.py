import argparse
import sys
import os
from .core import UnitTestValidator
from pr_file_checker import PRFileChecker


def check_pr_file():
    pr_number = int(os.getenv("PR_NUMBER", "123"))
    repo = os.getenv("GITHUB_REPO", "youruser/yourrepo")
    token = os.getenv("GITHUB_TOKEN", "")
    checker = PRFileChecker(pr_number=pr_number, repo=repo, token=token)
    checker.has_file("unit_tests.md")


def check_cli_file():
    parser = argparse.ArgumentParser(description="Validate PR unit test docs.")
    parser.add_argument("--pr", required=True, help="GitHub PR number")
    parser.add_argument(
        "--path", required=True, help="Path to unit test doc (e.g., unit_tests.md)"
    )
    args = parser.parse_args()
    validator = UnitTestValidator(pr=args.pr, path=args.path)

    if args.path:
        result = validator.validate()
    elif args.pr:
        result = validator.validate_from_pr()
    else:
        print("⚠️Please provide --pr or --path")
        sys.exit(1)

    if result == 0:
        print(f"✅  Unit test validation passed")
    else:
        print(f"❌  Unit test validation failed")
    sys.exit(result)


def main():
    if len(sys.argv) > 1:
        check_cli_file()
    else:
        check_pr_file()


if __name__ == "__main__":
    main()
