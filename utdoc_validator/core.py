import os


class UnitTestValidator:
    def __init__(self, pr, path):
        self.pr = pr
        self.path = path

    def validate(self) -> int:
        if self.path:
            try:
                with open(self.path, "r") as f:
                    filename = os.path.basename(self.path)
                    content = f.read()
                    if filename == "unit_tests.md" and content.strip():
                        return 0  # Success
            except FileNotFoundError:
                pass
        return 1  # Failure

    def validate_from_pr(self) -> int:
        # TODO: GitHub API Logic
        print(f"🔧 Would validate PR # {self.pr} (not implemented)")
        return 1
