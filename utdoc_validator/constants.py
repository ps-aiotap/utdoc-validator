"""Constants used throughout the utdoc-validator."""

# File names
DEFAULT_DOC_NAME = "unit_tests.md"
DEFAULT_CONFIG_FILE = ".utdocconfig"

# Required section headers
DEFAULT_REQUIRED_SECTIONS = ["## Test Cases", "## Coverage"]

# Placeholder patterns that indicate incomplete documentation
PLACEHOLDER_PATTERNS = [r"\bWIP\b", r"\bTBD\b", r"\bTo be added\b", r"\bTODO\b"]

# Default values for GitHub integration
DEFAULT_PR_NUMBER = "123"
DEFAULT_REPO = "youruser/yourrepo"

# Default configuration values
DEFAULT_STRICT_MODE = False
DEFAULT_ALLOW_WARNINGS = True
DEFAULT_IGNORE_FILES = []

# Exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# Environment variable names
ENV_PR_NUMBER = "PR_NUMBER"
ENV_GITHUB_EVENT_NUMBER = "GITHUB_EVENT_NUMBER"
ENV_GITHUB_REPO = "GITHUB_REPO"
ENV_GITHUB_REPOSITORY = "GITHUB_REPOSITORY"
ENV_GITHUB_TOKEN = "GITHUB_TOKEN"

# GitHub API constants
GITHUB_API_ACCEPT_HEADER = "application/vnd.github+json"
GITHUB_API_RAW_ACCEPT_HEADER = "application/vnd.github.v3.raw"
GITHUB_API_AUTH_PREFIX = "token "
GITHUB_API_REPOS_URL = "https://api.github.com/repos"

# GitHub CLI constants
GH_CLI_COMMAND = "gh"
GH_CLI_PR_SUBCOMMAND = "pr"
GH_CLI_VIEW_SUBCOMMAND = "view"
GH_CLI_JSON_FLAG = "--json"
GH_CLI_JQ_FLAG = "--jq"
GH_CLI_REPO_FLAG = "--repo"

# UI messages
WRONG = "❌"
RIGHT = "✅"
WARNING = "⚠️"
MSG_FILE_NOT_FOUND = WRONG + " File not found: {}"
MSG_ERROR_READING_FILE = WRONG + " Error reading file: {}"
MSG_MISSING_SECTION = WRONG + " Missing section: {}"
MSG_PLACEHOLDER_FOUND = WARNING + " Placeholder found: '{}' present in document."
MSG_VALIDATION_PASSED = RIGHT + " Unit test validation passed"
MSG_VALIDATION_FAILED = WRONG + " Unit test validation failed"
MSG_TEMPLATE_GENERATED = RIGHT + " Template generated at: {}"
MSG_NO_PR_OR_PATH = WARNING + " Please provide --pr or --path"
MSG_STRICT_MODE_WARNING = (
    WARNING + " Validation passed but warnings were found in strict mode"
)
MSG_UNEXPECTED_ERROR = WRONG + " An unexpected error occurred: {}"
MSG_NO_PR_NUMBER = WRONG + " No PR number provided"
MSG_INVALID_PR_NUMBER = WRONG + " Invalid PR number: {}"
MSG_NO_FILES_RETRIEVED = WRONG + " Could not retrieve files for PR #{}"
MSG_NO_DOC_FILE_FOUND = WRONG + " No documentation file found in PR #{}"
MSG_FAILED_GET_CONTENT = WRONG + " Failed to get file content: {}"
MSG_API_TOKEN_NOT_PROVIDED = "[API] GitHub token not provided."
MSG_API_FAILED = "[API] Failed: {}"
MSG_CLI_FAILED = "[CLI] failed: {}"
MSG_FILE_STATUS = (
    "{'✅' if found else '❌'} `{target_file}` {'found' if found else 'missing'}"
)
