"""Build Windows executable for PDF Flipbook Animator."""

import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

def clean_build():
    """Clean previous build artifacts."""
    dirs_to_remove = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            print(f"Removing {dir_name}/...")
            shutil.rmtree(dir_name)
    
    # Remove .spec files
    for spec_file in Path('.').glob('*.spec'):
        if spec_file.name != 'build_windows.spec':
            spec_file.unlink()

def install_pyinstaller():
    """Install PyInstaller if not already installed."""
    try:
        import PyInstaller
        print(f"PyInstaller {PyInstaller.__version__} is already installed")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])

def build_executable():
    """Build the Windows executable."""
    print("\n" + "="*60)
    print("Building PDF Flipbook Animator Windows Executable")
    print("="*60 + "\n")
    
    # Run PyInstaller
    print("Running PyInstaller...")
    result = subprocess.run(
        [sys.executable, '-m', 'PyInstaller', 'build_windows.spec', '--clean'],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("ERROR: PyInstaller failed!")
        print(result.stderr)
        return False
    
    print("✓ Executable built successfully!")
    return True

def create_distribution():
    """Create distribution package."""
    dist_dir = Path('dist/pdf-flipbook')
    if not dist_dir.exists():
        print("ERROR: Distribution directory not found!")
        return False
    
    # Create README for distribution
    readme_content = """# PDF Flipbook Animator - Windows Edition

## Quick Start

1. Open Command Prompt or PowerShell
2. Navigate to this folder
3. Run: pdf-flipbook.exe convert your-document.pdf

## Examples

```cmd
REM Basic conversion
pdf-flipbook.exe convert document.pdf

REM High quality
pdf-flipbook.exe convert magazine.pdf --dpi 250 --lossless --animation-mode realistic

REM Custom output
pdf-flipbook.exe convert book.pdf -o ./my-flipbook --title "My Book"

REM Get help
pdf-flipbook.exe --help
pdf-flipbook.exe convert --help
```

## Requirements

- Windows 10 or later
- No Python installation required!

## Documentation

Full documentation: https://github.com/vedanttalnikar/pdf-flipbook-animator-commercial

## License

MIT License - Free to use for personal and commercial projects

"""
    
    readme_path = dist_dir / 'README.txt'
    readme_path.write_text(readme_content)
    print(f"✓ Created {readme_path}")
    
    # Create ZIP archive
    zip_name = 'pdf-flipbook-windows.zip'
    print(f"\nCreating {zip_name}...")
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in dist_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(dist_dir.parent)
                zipf.write(file_path, arcname)
                print(f"  Added: {arcname}")
    
    file_size = os.path.getsize(zip_name) / (1024 * 1024)
    print(f"\n✓ Created {zip_name} ({file_size:.2f} MB)")
    
    return True

def main():
    """Main build process."""
    try:
        print("Step 1: Cleaning previous builds...")
        clean_build()
        
        print("\nStep 2: Installing PyInstaller...")
        install_pyinstaller()
        
        print("\nStep 3: Building executable...")
        if not build_executable():
            sys.exit(1)
        
        print("\nStep 4: Creating distribution package...")
        if not create_distribution():
            sys.exit(1)
        
        print("\n" + "="*60)
        print("BUILD SUCCESSFUL!")
        print("="*60)
        print(f"\nExecutable location: dist/pdf-flipbook/pdf-flipbook.exe")
        print(f"Distribution package: pdf-flipbook-windows.zip")
        print("\nTo test:")
        print("  cd dist/pdf-flipbook")
        print("  pdf-flipbook.exe --version")
        print("\n")
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
