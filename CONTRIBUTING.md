# Contributing to PDF Flipbook Animator

Thank you for your interest in contributing to PDF Flipbook Animator! We welcome contributions from the community.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Release Process](#release-process)

## Code of Conduct

This project adheres to the Contributor Covenant [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Create a new branch for your feature or bug fix
4. Make your changes
5. Submit a pull request

## Development Setup

### Prerequisites

- Python 3.9 or higher
- Git
- pip

### Setup Steps

1. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/pdf-flipbook-animator.git
   cd pdf-flipbook-animator
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the package in development mode with dev dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

4. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

5. Verify installation:
   ```bash
   pdf-flipbook --version
   pytest
   ```

## How to Contribute

### Reporting Bugs

- Use the GitHub issue tracker
- Use the bug report template
- Include detailed reproduction steps
- Provide system information and PDF details
- Include error messages and logs

### Suggesting Features

- Use the GitHub issue tracker
- Use the feature request template
- Explain the use case and benefits
- Provide examples if possible

### Contributing Code

1. Check existing issues or create a new one
2. Discuss your approach before starting large changes
3. Write tests for new functionality
4. Ensure all tests pass
5. Update documentation as needed
6. Submit a pull request

## Coding Standards

### Python Style

We follow PEP 8 with some modifications:

- Line length: 88 characters (enforced by Black)
- Use type hints where appropriate
- Write docstrings for all public functions/classes

### Code Formatting

We use automated tools to maintain code quality:

- **Black**: Code formatting
  ```bash
  black src/ tests/
  ```

- **Ruff**: Linting
  ```bash
  ruff check src/ tests/
  ruff check --fix src/ tests/  # Auto-fix issues
  ```

- **mypy**: Type checking
  ```bash
  mypy src/
  ```

### Pre-commit Hooks

Pre-commit hooks run automatically on `git commit`:
- Trailing whitespace removal
- End-of-file fixing
- YAML/JSON validation
- Black formatting
- Ruff linting
- mypy type checking

Run manually on all files:
```bash
pre-commit run --all-files
```

### Commit Messages

Write clear, descriptive commit messages:

```
Add feature to export flipbooks as standalone HTML

- Implement self-contained HTML export option
- Bundle all assets inline using base64
- Update documentation with new CLI flag
- Add tests for export functionality

Fixes #123
```

Format:
- First line: Brief summary (50 chars or less)
- Blank line
- Detailed description (wrap at 72 chars)
- Reference related issues

## Testing

### Running Tests

Run all tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=pdf_flipbook_animator --cov-report=html
```

Run specific test file:
```bash
pytest tests/unit/test_converter.py
```

Run specific test:
```bash
pytest tests/unit/test_converter.py::test_convert_basic_pdf
```

### Writing Tests

- Place unit tests in `tests/unit/`
- Place integration tests in `tests/integration/`
- Use pytest fixtures for common setup
- Mock external dependencies
- Aim for >80% code coverage
- Test edge cases and error conditions

Example:
```python
def test_convert_pdf_to_images(sample_pdf, tmp_path):
    """Test PDF conversion creates correct number of images."""
    converter = PDFConverter()
    metadata = converter.convert_to_images(sample_pdf, tmp_path)
    
    assert metadata["page_count"] == 5
    assert len(metadata["images"]) == 5
    assert (tmp_path / "images" / "page_001.webp").exists()
```

### Test Data

- Add small test PDFs to `tests/fixtures/`
- Keep test files under 100 KB when possible
- Document what each test file contains

## Submitting Changes

### Pull Request Process

1. **Update your fork**:
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/pdf-flipbook-animator.git
   git fetch upstream
   git merge upstream/main
   ```

2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**:
   - Write/update code
   - Add/update tests
   - Update documentation
   - Run tests and linters

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Your descriptive commit message"
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**:
   - Go to GitHub and create a PR
   - Fill out the PR template completely
   - Link related issues
   - Wait for review and address feedback

### PR Requirements

- [ ] All tests pass
- [ ] Code follows style guidelines (Black, Ruff, mypy)
- [ ] New tests added for new functionality
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Commits are clear and descriptive
- [ ] PR description explains changes

### Review Process

- Maintainers will review your PR
- Address requested changes promptly
- Be respectful and patient
- CI must pass before merging
- At least one approval required

## Release Process

For maintainers only:

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md` with release notes
3. Commit changes: `git commit -m "Release v0.2.0"`
4. Create tag: `git tag -a v0.2.0 -m "Release v0.2.0"`
5. Push: `git push origin main --tags`
6. GitHub Actions will automatically build and publish to PyPI

## Questions?

- Open a [Discussion](https://github.com/yourusername/pdf-flipbook-animator/discussions)
- Check the [Documentation](https://yourusername.github.io/pdf-flipbook-animator)
- Contact maintainers via GitHub issues

Thank you for contributing! 🎉
