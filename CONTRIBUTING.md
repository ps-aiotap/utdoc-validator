# Contributing to utdoc-validator

Thank you for considering contributing to utdoc-validator! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## Setting Up Development Environment

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/utdoc-validator.git
   cd utdoc-validator
   ```

3. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

5. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Development Workflow

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature-or-fix-name
   ```

2. Make your changes and commit them:
   ```bash
   git add .
   git commit -m "Description of changes"
   ```

3. Push your branch to GitHub:
   ```bash
   git push origin feature-or-fix-name
   ```

4. Open a pull request on GitHub

## Running Tests

Run the test suite with pytest:

```bash
pytest
```

To run tests with coverage:

```bash
pytest --cov=utdoc_validator
```

## Code Formatting and Linting

This project uses:
- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

These tools are configured as pre-commit hooks, but you can also run them manually:

```bash
# Format code with Black
black utdoc_validator tests

# Sort imports with isort
isort utdoc_validator tests

# Lint with flake8
flake8 utdoc_validator tests

# Type check with mypy
mypy utdoc_validator
```

## Pull Request Guidelines

1. Include tests for any new features or bug fixes
2. Update documentation if necessary
3. Follow the existing code style
4. Write clear commit messages
5. Make sure all tests pass before submitting

## Release Process

1. Update version in `setup.py`
2. Update CHANGELOG.md
3. Create a new tag following semantic versioning:
   ```bash
   git tag -a v0.1.0 -m "Release v0.1.0"
   git push origin v0.1.0
   ```

## Questions?

If you have any questions, feel free to open an issue or reach out to the maintainers.