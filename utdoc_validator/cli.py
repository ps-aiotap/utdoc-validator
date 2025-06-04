# Placeholder for CLI logic
# utdoc_validator/cli.py

import argparse
from .core import validate_unit_test_doc


def main():
    parser = argparse.ArgumentParser(description="Validate PR unit test docs.")
    parser.add_argument("--pr", help="GitHub PR number")
    parser.add_argument("--path", help="Path to unit test doc (e.g., unit_tests.md)")
    args = parser.parse_args()

    # Delegate to core logic
    result = validate_unit_test_doc(pr=args.pr, path=args.path)
    print(result)


if __name__ == "__main__":
    main()
