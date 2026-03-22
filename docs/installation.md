# Installation

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

## Install from PyPI

The easiest way to install PDF Flipbook Animator:

```bash
pip install pdf-flipbook-animator
```

## Install from Source

For development or to get the latest unreleased features:

```bash
# Clone the repository
git clone https://github.com/vedanttalnikar/pdf-flipbook-animator-commercial.git
cd pdf-flipbook-animator

# Install in development mode
pip install -e ".[dev]"
```

## Verify Installation

Check that the installation was successful:

```bash
pdf-flipbook --version
```

You should see the version number (e.g., `0.2.0`).

## Dependencies

The package automatically installs these dependencies:

- **PyMuPDF** (≥1.23.0) - PDF processing
- **Pillow** (≥10.0.0) - Image manipulation
- **Click** (≥8.1.0) - CLI framework

## Virtual Environment (Recommended)

It's recommended to use a virtual environment:

=== "Windows"
    ```bash
    python -m venv venv
    venv\Scripts\activate
    pip install pdf-flipbook-animator
    ```

=== "macOS/Linux"
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install pdf-flipbook-animator
    ```

## Upgrading

To upgrade to the latest version:

```bash
pip install --upgrade pdf-flipbook-animator
```

## Troubleshooting

### Permission Errors

If you encounter permission errors on Linux/macOS:

```bash
pip install --user pdf-flipbook-animator
```

### PyMuPDF Installation Issues

If PyMuPDF fails to install, you may need to install system dependencies:

=== "Ubuntu/Debian"
    ```bash
    sudo apt-get update
    sudo apt-get install python3-dev
    ```

=== "macOS"
    ```bash
    brew install python
    ```

=== "Windows"
    Usually no additional dependencies needed. Ensure you have the latest pip:
    ```bash
    python -m pip install --upgrade pip
    ```

### Still Having Issues?

- Check the [GitHub Issues](https://github.com/vedanttalnikar/pdf-flipbook-animator-commercial/issues)
- Ask in [Discussions](https://github.com/vedanttalnikar/pdf-flipbook-animator-commercial/discussions)

## Next Steps

Now that you've installed PDF Flipbook Animator, check out the [Quick Start](quickstart.md) guide!
