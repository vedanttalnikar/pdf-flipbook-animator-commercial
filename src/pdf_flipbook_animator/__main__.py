"""
PDF Flipbook Animator - Entry Point for Windows Executable

This module serves as the main entry point for the PyInstaller-built
Windows executable. It imports and runs the CLI main function.
"""

from pdf_flipbook_animator.cli import main

if __name__ == "__main__":
    main()
