import os
import re


class UnitTestValidator:
    def __init__(self, pr: str, path: str):
        self.pr = pr
        self.path = path
        self.placeholder_patterns = [r"\bWIP\b", r"\bTBD\b", r"\bTo be added\b"]
        self.required_header = ["## Test Cases", "## Coverage"]
        self.errors = []
        self.warnings = []

    def validate(self) -> int:
        if not os.path.exists(self.path):
            print(f"❌ File not found: {self.path}")
            return 1

        with open(self.path, "r") as f:
            content = f.read()

        success = True

        for header in self.required_header:
            if header not in content:
                print(f"❌ Missing section: {header}")
                success = False

        if any(x in content for x in self.placeholder_patterns):
            print(
                "⚠️ Placeholder found:  'WIP' or 'TBD' or 'To be added' present in document."
            )

        return 0 if success else 1

    def validate_from_pr(self) -> int:
        # TODO: GitHub API Logic
        print(f"🔧 Would validate PR # {self.pr} (not implemented)")
        return 1
