# Development Scripts

Helpful scripts for development and testing.

## Setup Development Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -e ".[dev]"
pre-commit install
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
pre-commit install
```

## Run Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=pdf_flipbook_animator --cov-report=html

# Specific test
pytest tests/unit/test_converter.py

# Watch mode (requires pytest-watch)
ptw
```

## Code Quality

```bash
# Format code
black src/ tests/

# Check formatting
black --check src/ tests/

# Lint
ruff check src/ tests/

# Auto-fix linting issues
ruff check --fix src/ tests/

# Type checking
mypy src/

# Run all checks
pre-commit run --all-files
```

## Build Package

```bash
# Build distributions
python -m build

# Check build
twine check dist/*
```

## Build Documentation

```bash
# Serve docs locally
mkdocs serve

# Build docs
mkdocs build

# Deploy to GitHub Pages
mkdocs gh-deploy
```

## Test Installation

```bash
# Install in development mode
pip install -e .

# Test CLI
pdf-flipbook --version
pdf-flipbook --help

# Test with example
pdf-flipbook convert examples/January_2026_patrabhet.pdf

# Clean test outputs
rmdir /s /q output  # Windows
rm -rf output/      # macOS/Linux
```

## Release Process

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Commit changes:
   ```bash
   git add .
   git commit -m "Release v0.2.0"
   ```
4. Create and push tag:
   ```bash
   git tag -a v0.2.0 -m "Release v0.2.0"
   git push origin main --tags
   ```
5. GitHub Actions will automatically publish to PyPI

## Clean Project

```bash
# Remove build artifacts
rmdir /s /q build dist *.egg-info  # Windows
rm -rf build/ dist/ *.egg-info/    # macOS/Linux

# Remove Python cache
Get-ChildItem -Recurse -Filter __pycache__ | Remove-Item -Recurse -Force  # Windows
find . -type d -name __pycache__ -exec rm -rf {} +  # macOS/Linux

# Remove test cache
rmdir /s /q .pytest_cache htmlcov .coverage  # Windows
rm -rf .pytest_cache/ htmlcov/ .coverage     # macOS/Linux
```

## Useful Commands

```bash
# Count lines of code
Get-ChildItem -Recurse -Include *.py | Get-Content | Measure-Object -Line  # Windows
find src tests -name "*.py" | xargs wc -l  # macOS/Linux

# Find TODO comments
Select-String -Pattern "TODO" -Path src/*.py,tests/*.py -Recurse  # Windows
grep -r "TODO" src/ tests/  # macOS/Linux
```
