# GitHub Action Usage

The utdoc-validator can be used as a GitHub Action to automatically validate unit test documentation in pull requests.

## Basic Usage

Add the following workflow to your repository at `.github/workflows/validate-docs.yml`:

```yaml
name: Validate Unit Test Docs

on:
  pull_request:
    types: [opened, synchronize]
    paths:
      - '**.md'
      - '.utdocconfig'

jobs:
  validate-docs:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
        
      - name: Validate Unit Test Documentation
        uses: yourusername/utdoc-validator@main
        with:
          pr_number: ${{ github.event.pull_request.number }}
          doc_name: unit_tests.md
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `pr_number` | Pull Request number | No | - |
| `path` | Path to the test doc | No | - |
| `doc_name` | Name of the doc file | No | `unit_tests.md` |
| `config` | Path to config file | No | `.utdocconfig` |
| `github_token` | GitHub token for API access | No | `${{ github.token }}` |

## Configuration

Create a `.utdocconfig` file in your repository root to customize validation:

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

## Advanced Usage

### Adding PR Comments

You can configure the action to comment on PRs with validation results:

```yaml
- name: Comment on PR
  if: always()
  uses: actions/github-script@v6
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
    script: |
      const { owner, repo } = context.repo;
      const run_id = context.runId;
      const run_url = `https://github.com/${owner}/${repo}/actions/runs/${run_id}`;
      
      const jobStatus = '${{ job.status }}';
      const icon = jobStatus === 'success' ? '✅' : '❌';
      const message = jobStatus === 'success' 
        ? 'Unit test documentation validation passed!'
        : 'Unit test documentation validation failed. Please check the logs for details.';
      
      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: owner,
        repo: repo,
        body: `${icon} **Unit Test Documentation Validation**\n\n${message}\n\n[View Logs](${run_url})`
      });
```

### Custom Validation Rules

You can create custom validation rules by extending the configuration file and implementing custom checks in your fork of the repository.