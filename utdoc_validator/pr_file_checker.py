import os, subprocess, requests
from typing import Optional, List


class PRFileChecker:
    def __init__(self, pr_number: int, repo: str, token: Optional[str] = None):
        self.pr_number = pr_number
        self.repo = repo
        self.token = token or os.getenv("GITHUB_TOKEN")

    def fetch_files_from_api(self) -> Optional[List[str]]:
        if not self.token:
            print("[API] GitHub token not provided.")
            return None

        url = f"https://api.github.com/repos/{self.repo}/pulls/{self.pr_number}/files"
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": f"application/vnd.github+json",
        }
        try:
            response = requests.get(url=url, headers=headers)
            response.raise_for_status()
            return [file["filename"] for file in response.json()]
        except requests.RequestException as e:
            print(f"[API] Failed: {e}")
            return None

    def fetch_files_from_cli(self) -> Optional[List[str]]:
        try:
            result = subprocess.run(
                [
                    "gh",
                    "pr",
                    str(self.pr_number),
                    "--json",
                    "files",
                    "--jq",
                    ".files[].path",
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            return result.stdout.strip().splitlines()
        except subprocess.CalledProcessError as e:
            print(f"[CLI] failed: {e.stderr}")
            return None

    def get_pr_files(self) -> Optional[List[str]]:
        return self.fetch_files_from_api() or self.fetch_files_from_cli()

    def has_file(self, target_file: str = "unit_tests.md") -> bool:
        files = self.get_pr_files()

        if not files:
            print(f"❌ Could not retrieve file list.")
            return False

        found = any(f.endswith(target_file) for f in files)

        print(
            f"{'✅' if found else '❌'} `{target_file}` {'found' if found else 'missing'}"
        )

        return found
