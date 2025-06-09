# Unit Test Doc Validator

A Python CLI tool that validates the presence and structure of unit test documentation in software projects. It operates locally and integrates with GitHub PRs to check for the presence and completeness of unit test documentation files.

## Features

- Validates unit test documentation files for required sections
- Detects placeholder text like "WIP" or "TBD" that indicates incomplete documentation
- Integrates with GitHub PRs to check for documentation files
- Supports custom configuration via `.utdocconfig` file
- Generates template documentation files
- Available as a GitHub Action

## Installation

```bash
# Install from source
git clone https://github.com/yourusername/utdoc-validator.git
cd utdoc-validator
pip install -e .

# Or install directly from PyPI (once published)
# pip install utdoc-validator
```

## Usage

### Basic Usage

```bash
# Validate a specific file
utdoc-validator --path path/to/unit_tests.md

# Generate a template file
utdoc-validator --generate-template --path path/to/unit_tests.md

# Validate documentation in a GitHub PR
utdoc-validator --pr 123
```

### Command Line Options

- `--path`: Path to the test documentation file
- `--pr`: GitHub PR number to check
- `--doc-name`: Custom documentation filename (default: unit_tests.md)
- `--generate-template`: Generate a default template file
- `--config`: Path to config file (default: .utdocconfig)
- `--verbose`, `-v`: Enable verbose logging
- `--log-file`: Path to log file
- `--strict`: Enable strict mode (warnings are treated as errors)

### Environment Variables

When using with GitHub PRs:

- `GITHUB_TOKEN`: GitHub API token for authentication
- `GITHUB_REPO`: Repository in format "username/repo"
- `PR_NUMBER`: Pull request number

## Configuration

Create a `.utdocconfig` file in your project root to customize validation:

```json
{
  "required_sections": [
    "## Test Cases",
    "## Coverage",
    "## Mocks Used"
  ],
  "placeholder_patterns": [
    "\\bWIP\\b",
    "\\bTBD\\b",
    "\\bTo be added\\b",
    "\\bTODO\\b"
  ],
  "file_name": "unit_tests.md",
  "strict_mode": false,
  "allow_warnings": true,
  "ignore_files": [
    "vendor/",
    "node_modules/",
    "third_party/"
  ]
}
```

### Configuration Options

- `required_sections`: List of section headers that must be present in the documentation
- `placeholder_patterns`: List of regex patterns that indicate incomplete documentation
- `file_name`: Default name of the documentation file
- `strict_mode`: If true, warnings are treated as errors
- `allow_warnings`: If false, any warning will cause validation to fail
- `ignore_files`: List of directories to ignore when checking for documentation files

## GitHub Action Integration

See [GitHub Action Usage](docs/github-action-usage.md) for details on using the tool as a GitHub Action.

## Development

### Setup Development Environment

```bash
git clone https://github.com/yourusername/utdoc-validator.git
cd utdoc-validator
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

## License

MIT