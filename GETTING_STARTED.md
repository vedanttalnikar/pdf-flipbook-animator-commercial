# Getting Started with Development

Welcome to PDF Flipbook Animator development!

## Quick Setup

### 1. Install Dependencies

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install package in development mode
pip install -e ".[dev]"

# Install pre-commit hooks (optional but recommended)
pre-commit install
```

### 2. Verify Installation

```powershell
# Check CLI is available
pdf-flipbook --version

# Should output: pdf-flipbook, version 0.2.0
```

### 3. Test with Sample PDF

```powershell
# Convert the sample PDF
pdf-flipbook convert examples\January_2026_patrabhet.pdf

# Open the result
start output\January_2026_patrabhet\index.html
```

### 4. Run Tests

```powershell
# Run all tests
pytest

# Run with coverage
pytest --cov=pdf_flipbook_animator
```

## Next Steps

1. **Read the Documentation**: Check `docs/` for detailed guides
2. **Explore Examples**: See `examples/README.md` for usage examples
3. **Contributing**: Read `CONTRIBUTING.md` for development guidelines
4. **Report Issues**: Use GitHub Issues for bugs or feature requests

## Common Tasks

### Adding a New Feature

1. Create a new branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Add tests in `tests/`
4. Run tests: `pytest`
5. Format code: `black src/ tests/`
6. Check linting: `ruff check src/ tests/`
7. Commit and push
8. Create a Pull Request

### Running Code Quality Checks

```powershell
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/ --fix

# Type checking
mypy src/

# Or run all checks at once
pre-commit run --all-files
```

### Building Documentation

```powershell
# Install docs dependencies
pip install -e ".[docs]"

# Serve documentation locally
mkdocs serve

# View at http://127.0.0.1:8000
```

### Making a Release (Maintainers)

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Commit: `git commit -m "Release v0.2.0"`
4. Tag: `git tag -a v0.2.0 -m "Release v0.2.0"`
5. Push: `git push origin main --tags`
6. GitHub Actions will automatically publish to PyPI

## Troubleshooting

### Virtual Environment Not Activating

Make sure you're running PowerShell and execution policy allows scripts:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Import Errors

Make sure the package is installed in development mode:
```powershell
pip install -e .
```

### Tests Failing

Ensure all dependencies are installed:
```powershell
pip install -e ".[dev]"
```

## Project Structure

```
pdf_flipbook_animator/
├── src/pdf_flipbook_animator/   # Main package code
│   ├── cli.py                   # CLI interface
│   ├── config.py                # Configuration
│   ├── core/                    # Core functionality
│   │   ├── converter.py         # PDF → Images
│   │   └── generator.py         # HTML generator
│   └── utils/                   # Utilities
│       └── image.py             # Image processing
├── tests/                       # Test suite
│   ├── unit/                    # Unit tests
│   └── integration/             # Integration tests
├── docs/                        # Documentation
├── examples/                    # Example PDFs
└── scripts/                     # Development scripts
```

## Need Help?

- � Email: vedanttalnikar@gmail.com
- �📖 [Full Documentation](https://vedanttalnikar.github.io/pdf-flipbook-animator-commercial)
- 💬 [GitHub Discussions](https://github.com/vedanttalnikar/pdf-flipbook-animator-commercial/discussions)
- 🐛 [Issue Tracker](https://github.com/vedanttalnikar/pdf-flipbook-animator-commercial/issues)

Happy coding! 🚀
