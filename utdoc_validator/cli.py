import argparse
import sys
from .core import UnitTestValidator


def main():
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


if __name__ == "__main__":
    main()
