# Unit Test Doc Validator

[![Tests](https://github.com/yourusername/utdoc-validator/actions/workflows/tests.yml/badge.svg)](https://github.com/yourusername/utdoc-validator/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/yourusername/utdoc-validator/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/utdoc-validator)
[![PyPI version](https://badge.fury.io/py/utdoc-validator.svg)](https://badge.fury.io/py/utdoc-validator)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python CLI tool that validates the presence and structure of unit test documentation in software projects. It operates locally and integrates with GitHub PRs to check for the presence and completeness of unit test documentation files.

## Features

- **Documentation Validation**: Validates unit test documentation files for required sections
- **Placeholder Detection**: Identifies placeholder text like "WIP" or "TBD" that indicates incomplete documentation
- **GitHub PR Integration**: Integrates with GitHub PRs to check for documentation files
- **Custom Configuration**: Supports extensive customization via `.utdocconfig` file
- **Template Generation**: Creates template documentation files with required sections
- **GitHub Action**: Available as a GitHub Action for CI/CD integration
- **Multiple Encoding Support**: Handles files with different encodings (UTF-8, UTF-16, etc.)
- **Strict Mode**: Option to treat warnings as errors for stricter validation
- **Comprehensive Logging**: Detailed logging with configurable verbosity

## Installation

```bash
# Install from PyPI
pip install utdoc-validator

# Install from source
git clone https://github.com/yourusername/utdoc-validator.git
cd utdoc-validator
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"
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

Add to your workflow:

```yaml
name: Validate Unit Test Docs

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  validate-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Validate Unit Test Documentation
        uses: yourusername/utdoc-validator@main
        with:
          pr_number: ${{ github.event.pull_request.number }}
          doc_name: unit_tests.md
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

See [GitHub Action Usage](docs/github-action-usage.md) for more details.

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for information on how to contribute to this project.

### Running Tests

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=utdoc_validator
```

### Code Formatting and Linting

This project uses pre-commit hooks for code formatting and linting:

```bash
# Install pre-commit hooks
pre-commit install

# Run pre-commit hooks manually
pre-commit run --all-files
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.