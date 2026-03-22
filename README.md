# PDF Flipbook Animator

[![Python Versions](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.2.0-green.svg)](CHANGELOG.md)
[![Downloads](https://img.shields.io/github/downloads/vedanttalnikar/pdf-flipbook-animator-commercial/total)](https://github.com/vedanttalnikar/pdf-flipbook-animator-commercial/releases)

**Free & Open Source PDF to Flipbook Converter**

Transform any PDF into an interactive, web-based flipbook with stunning page-turning animations. Choose from simple transitions to realistic 3D page curl effects. Perfect for e-books, magazines, catalogs, and presentations.

✨ **No Python Required!** Download the Windows executable for instant use.

[🎬 **Live Demo** →](https://vedanttalnikar.github.io/pdf-flipbook-animator-commercial/) | [📥 **Windows Download** →](https://github.com/vedanttalnikar/pdf-flipbook-animator-commercial/releases/latest) | [📖 Full Documentation](OUTPUT_USAGE_GUIDE.md) | [💬 Support](https://github.com/vedanttalnikar/pdf-flipbook-animator-commercial/issues)

---

## 📚 Complete Documentation

**→ [OUTPUT_USAGE_GUIDE.md](OUTPUT_USAGE_GUIDE.md)** - **Comprehensive guide covering:**
- 🚀 **Complete API Reference** - All CLI options and Python API
- 📱 **Mobile Usage** - How to use flipbooks on phones/tablets (touch/swipe enabled)
- 🌐 **Web Hosting** - Deploy to Netlify, GitHub Pages, Vercel, or any hosting
- 🎯 **Recommended Configs** - By use case (magazine, catalog, portfolio, etc.)
- 📦 **Output Format Details** - File structure, sizes, performance benchmarks
- 🔧 **Advanced Configuration** - Custom templates, embedding, optimization

---

## ✨ Features

- 📄 **PDF to Web** - Convert any PDF to an interactive flipbook
- 🎬 **3 Animation Modes** - Simple, 3D CSS, or realistic page curl effects
- � **Clickable Links** - Preserves internal navigation and external hyperlinks (`--preserve-links`)
- 📑 **Table of Contents** - Searchable TOC sidebar extracted from PDF bookmarks (`--enable-toc`)
- 🔍 **Zoom & Pan** - Scroll-wheel zoom with click-and-drag panning
- �🚀 **Easy CLI** - Simple command-line interface
- 🎨 **Customizable** - Control colors, quality, and layout
- 📱 **Responsive** - Works on all devices and screen sizes
- ⚡ **Optimized** - WebP images with lazy loading
- 🌐 **Static Output** - Host anywhere (GitHub Pages, Netlify, etc.)
- ⌨️ **Keyboard Navigation** - Full keyboard support
- 🖥️ **Fullscreen Mode** - Immersive reading experience
- 💾 **Position Memory** - Remembers where you left off
- 🔄 **Batch Processing** - Convert multiple PDFs at once
- 💻 **Windows Executable** - No Python installation needed!

## 🎬 Live Demo

**[→ Try the Interactive Demo](https://vedanttalnikar.github.io/pdf-flipbook-animator-commercial/)**

Experience a real 583-page Marathi book flipbook with **Realistic Mode**:
- ✅ **Side panel layout** - Maximum vertical space for PDF viewing
- ✅ **300 DPI resolution** - Crystal clear text and images
- ✅ **Clickable links** - Internal page navigation and external URLs preserved
- ✅ **Table of Contents** - Searchable, collapsible TOC sidebar with H1 grouping
- ✅ **Zoom & pan** - Scroll-wheel zoom with click-and-drag panning
- ✅ **Fully responsive** - Auto-adapts to desktop/tablet/mobile
- ✅ **Touch/swipe gestures** - Natural mobile interaction
- ✅ **Keyboard navigation** - Arrow keys, Page Up/Down, Home/End
- ✅ **Physics-based animation** - Realistic page curl with shadows
- ✅ **High-DPI support** - Retina and 4K display optimization
- ✅ **Works everywhere** - Phone, tablet, desktop browsers

**Quick Start:**
```bash
pdf-flipbook convert book.pdf
# ✅ Flipbook created at: output/book/
```

## 📦 Installation

### Option 1: Windows Executable (Recommended - No Python Needed!)

Perfect for Windows users who don't have Python installed:

1. **Download**: Go to [Releases](https://github.com/vedanttalnikar/pdf-flipbook-animator-commercial/releases/latest)
2. **Extract**: Download `pdf-flipbook-windows.zip` and extract it
3. **Run**: Open Command Prompt in the extracted folder

```cmd
pdf-flipbook.exe convert your-document.pdf
```

**System Requirements:**
- Windows 10 or later
- 64-bit system
- ~70 MB disk space (includes all dependencies)

### Option 2: Install via pip (Python Users)

**Requirements:**
- Python 3.9 or higher
- pip (Python package manager)

```bash
pip install pdf-flipbook-animator
```

### Option 3: Install from Source (Developers)

```bash
git clone https://github.com/vedanttalnikar/pdf-flipbook-animator-commercial.git
cd pdf-flipbook-animator-commercial
pip install -e .
```

## 🚀 Quick Start

### Convert a PDF

```bash
# Using Windows executable
pdf-flipbook.exe convert your-document.pdf

# Using Python installation
pdf-flipbook convert your-document.pdf
```

This creates a complete interactive website in `output/your-document/`.

### View the Flipbook

Open `output/your-document/index.html` in your browser, or serve it locally:

```bash
cd output/your-document
python -m http.server 8000
```

Then visit [http://localhost:8000](http://localhost:8000)

### More Examples

```bash
# Custom title and colors
pdf-flipbook convert book.pdf --title "My Book" --primary-color "#FF5722"

# High quality output (recommended)
pdf-flipbook convert document.pdf --dpi 250 --lossless

# Animation modes
pdf-flipbook convert book.pdf --animation-mode simple      # Fast (default)
pdf-flipbook convert book.pdf --animation-mode 3d-css      # 3D page fold
pdf-flipbook convert book.pdf --animation-mode realistic   # Realistic page curl

# Custom animation timing
pdf-flipbook convert book.pdf -a realistic --flip-duration 1000

# Preserve clickable links from PDF
pdf-flipbook convert book.pdf --preserve-links

# Enable Table of Contents sidebar
pdf-flipbook convert book.pdf --enable-toc

# Full-featured conversion (recommended)
pdf-flipbook convert book.pdf -a realistic --dpi 300 --preserve-links --enable-toc

# Batch convert multiple PDFs
pdf-flipbook batch ./pdf-folder/

# Get PDF information
pdf-flipbook info document.pdf
```

## 📖 Usage

### Basic Conversion

```bash
pdf-flipbook convert INPUT.pdf [OPTIONS]
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--output-dir, -o` | Output directory | `./output/<pdf-name>` |
| `--dpi` | Image resolution (72-600) | `250` (improved!) |
| `--quality` | WebP quality (1-100) | `85` |
| `--jpg-quality` | JPG fallback quality | `90` |
| `--lossless` | Use lossless WebP (best for text) | `True` (improved!) |
| `--title` | Flipbook title | PDF filename |
| `--single-page` | Single page mode | `False` |
| `--no-fullscreen` | Disable fullscreen button | `False` |
| `--primary-color` | Primary UI color | `#2196F3` |
| `--animation-mode, -a` | Animation style: `simple`, `3d-css`, `realistic` | `simple` |
| `--flip-duration` | Animation duration in ms (200-2000) | `800` |
| `--enable-curl` | Enable 3D page curl (realistic mode) | `False` |
| `--index-page` | Jump-to-index button target page | `2` |
| `--no-index-button` | Disable jump-to-index button | `False` |
| `--preserve-links` | Preserve clickable PDF links (internal + external) | `False` |
| `--enable-toc` | Extract PDF bookmarks for TOC sidebar | `False` |

### Batch Processing

Convert multiple PDFs:

```bash
pdf-flipbook batch DIRECTORY [OPTIONS]
```

```bash
# Convert all PDFs in a folder
pdf-flipbook batch ./pdfs/

# Use a pattern
pdf-flipbook batch ./pdfs/ --pattern "chapter*.pdf"

# Custom output location
pdf-flipbook batch ./pdfs/ -o ./flipbooks/ --dpi 250 --lossless
```

### PDF Information

Get details about a PDF:

```bash
pdf-flipbook info document.pdf
```

Output:
```
📄 PDF Information: document.pdf

  Pages: 24
  Dimensions: 595 × 842 pt
  Title: Sample Document
  Estimated output size: ~12.0 MB
```

## 🎬 Animation Modes

Choose from three animation styles to match your needs:

### Simple (Default) ⚡
Fast CSS transitions with minimal resource usage. Best for large PDFs (100+ pages) and presentations where performance matters most.

```bash
pdf-flipbook convert book.pdf
# or explicitly:
pdf-flipbook convert book.pdf --animation-mode simple
```

**Features:**
- ✅ Instant page transitions
- ✅ Minimal resource usage
- ✅ 60 FPS performance
- ✅ Works on low-end devices

**Perfect for:** E-books, documentation, reports

### 3D CSS 🎨
Lightweight 3D page folding effect using CSS transforms. Smooth animations with good performance on most devices.

```bash
pdf-flipbook convert book.pdf --animation-mode 3d-css
```

**Features:**
- ✅ CSS 3D transforms
- ✅ Page fold effect
- ✅ Smooth 60 FPS animations
- ✅ No external libraries

**Perfect for:** Magazines, portfolios, catalogs

### Realistic 🎪 ⭐ RECOMMENDED
Full 3D page curl using the StPageFlip library. Physics-based animation with realistic shadows, page curl, and interactive dragging.

```bash
pdf-flipbook convert book.pdf --animation-mode realistic --dpi 250 --lossless
```

**NEW Features (v0.2.0):**
- ✅ **HTML Mode** - No canvas downscaling, perfect text quality
- ✅ **Device Pixel Ratio** - 2-3x sharper on Retina/4K displays
- ✅ **250 DPI Default** - Increased from 150 for better clarity
- ✅ **Lossless WebP** - Zero compression artifacts by default
- ✅ **Side Panel Layout** - Maximizes vertical space (~99vh for PDF)
- ✅ **Fully Responsive** - Auto-switches between single/two-page spread
- ✅ **Dynamic Perspective** - 1200px (mobile), 1800px (tablet), 2400px (desktop)
- ✅ **Physics-Based Animations** - Realistic page curl with dynamic shadows
- ✅ **Interactive Dragging** - Click and drag pages to flip
- ✅ **Touch Optimized** - Swipe gestures on mobile devices
- ✅ **Window Resize Handling** - Automatically reinitializes on orientation change
- ✅ **Smart Navigation** - Buttons adapt to single-page or two-page mode
- ✅ **Jump to Index** - Quick access button to table of contents

**Layout:**
```
┌──────────┬─────────────────────────┬──────────────┐
│  ◄ Prev  │   FULL-HEIGHT PDF      │  Title       │
│          │   (99vh viewing area)   │  Page Info   │
│          │                         │  Next ►      │
│          │                         │  Progress    │
└──────────┴─────────────────────────┴──────────────┘
  80px           Flexible                180px
```

**Responsive Breakpoints:**
- **Desktop** (≥1024px): Two-page spread, 80px + 180px side panels
- **Tablet** (768-1023px): Single page, 70px + 140px side panels  
- **Mobile** (<768px): Single page, 50px + 60px side panels

**Perfect for:** Photo books, magazines, comic books, high-end presentations

**Comparison:**

| Mode | Performance | Visual Effect | Quality | Best For |
|------|-------------|---------------|---------|----------|
| Simple | ⚡⚡⚡ 60 FPS | Basic fade | Good | Large PDFs, fast loading |
| 3D CSS | ⚡⚡ 60 FPS | Page fold | Good | Balanced visual appeal |
| Realistic | ⚡ 30-60 FPS | Realistic curl | **Excellent** | Professional publications |

**Recommended Settings:**
```bash
# Best quality for magazines/catalogs (default settings!)
pdf-flipbook convert magazine.pdf -a realistic

# Even higher quality
pdf-flipbook convert book.pdf -a realistic --dpi 300 --lossless

# Balanced quality/file size
pdf-flipbook convert doc.pdf -a realistic --dpi 200 --quality 90
```

## 📚 Output Structure

Each flipbook generates this structure:

```
output/document-name/
├── index.html          # Main viewer page
├── css/
│   └── style.css      # Styling
├── js/
│   └── flipbook.js    # Interactive logic
└── images/
    ├── page_001.webp  # Optimized page images
    ├── page_002.webp
    └── fallback/      # Browser fallbacks
        ├── page_001.jpg
        └── page_002.jpg
```

## 🌐 Hosting

The generated flipbook is a static website. Host it anywhere:

### GitHub Pages

```bash
cd output/your-document
git init
git add .
git commit -m "Add flipbook"
git branch -M main
git remote add origin https://github.com/yourusername/my-flipbook.git
git push -u origin main
```

Enable GitHub Pages in repository settings → Pages → Source: `main` branch.

### Netlify

Drag and drop the `output/your-document/` folder onto [Netlify Drop](https://app.netlify.com/drop).

### Vercel

```bash
cd output/your-document
vercel deploy
```

### Other Options

- AWS S3 + CloudFront
- Azure Storage + CDN
- Any web hosting service
- Local network share

## 🎯 Use Cases

- 📚 Digital magazines and publications
- 📖 Interactive documentation
- 🎓 Educational materials and textbooks
- 📊 Annual reports and presentations
- 🎨 Design portfolios
- 📰 Newsletters and catalogs
- 📕 E-books and novels
- 🎪 Event programs and brochures

## 🎨 Customization

### Colors

```bash
pdf-flipbook convert doc.pdf --primary-color "#9C27B0"
```

### Quality vs Size

| DPI | Quality | Use Case | Avg Size/Page |
|-----|---------|----------|---------------|
| 120 | Low | Preview/draft | ~250 KB |
| 150 | Good | Standard web | ~400 KB |
| 200 | High | Detailed docs | ~700 KB |
| **250** | **Recommended** | **Default (best balance)** | **~1.2 MB** |
| 300 | Very High | Print quality | ~1.8 MB |

## 🔨 Building Windows Executable

Want to build the executable yourself?

```bash
# Install PyInstaller
pip install pyinstaller

# Run the build script
python build_executable.py

# Test the executable
cd dist/pdf-flipbook
pdf-flipbook.exe --version
```

The build script creates:
- `dist/pdf-flipbook/pdf-flipbook.exe` - Standalone executable
- `pdf-flipbook-windows.zip` - Distribution package

## 🛠️ Development

### Setup

```bash
git clone https://github.com/vedanttalnikar/pdf-flipbook-animator-commercial.git
cd pdf-flipbook-animator-commercial

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# With coverage
pytest --cov=pdf_flipbook_animator --cov-report=html

# Run specific test file
pytest tests/unit/test_converter.py
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint
ruff check src/ tests/

# Type checking
mypy src/
```

## 📊 Recent Improvements

- ✅ **Collapsible TOC** - H1 headings with expand/collapse, search-aware hierarchy
- ✅ **Table of Contents** - `--enable-toc` extracts PDF bookmarks into a searchable sidebar
- ✅ **Clickable Links** - `--preserve-links` preserves internal page links and external URLs
- ✅ **Zoom & Pan** - Scroll-wheel zoom with click-and-drag panning, cursor states
- ✅ **Mobile Layout** - Compact responsive toolbar, fullscreen fixes
- ✅ **HTML Mode** - No canvas downscaling, perfect text quality
- ✅ **Lossless WebP** - Zero compression artifacts
- ✅ **Jump-to-Index** - Quick access button to table of contents page
- ✅ **Device Pixel Ratio** - 2-3x sharper on Retina/4K displays
- ✅ **Realistic Animation** - Physics-based page curl with StPageFlip

## 🤝 Contributing

Contributions are welcome! Please see our [Contributing Guidelines](CONTRIBUTING.md).

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Free for personal and commercial use!**

## 🙏 Acknowledgments

- [PyMuPDF](https://pymupdf.readthedocs.io/) - Excellent PDF processing library
- [Pillow](https://python-pillow.org/) - Powerful image manipulation
- [Click](https://click.palletsprojects.com/) - Beautiful CLI framework
- [StPageFlip](https://github.com/Nodlik/StPageFlip) - Realistic page flip library

## 📞 Support

**Documentation:**
- 📖 [Complete Output & Usage Guide](OUTPUT_USAGE_GUIDE.md) - Mobile, web, hosting, all API options
- 📱 [Mobile Device Testing](MOBILE_TESTING.md) - Touch/swipe testing procedures
- 📝 [Changelog](CHANGELOG.md) - Version history
- 📥 [Windows Executable Releases](https://github.com/vedanttalnikar/pdf-flipbook-animator-commercial/releases)

**Contact:**
- 📧 Email: vedanttalnikar@gmail.com

**Community:**
- 🐛 [Issue Tracker](https://github.com/vedanttalnikar/pdf-flipbook-animator-commercial/issues)
- 💬 [Discussions](https://github.com/vedanttalnikar/pdf-flipbook-animator-commercial/discussions)
- ⭐ Star this repo if you find it useful!

## 🗺️ Roadmap

- [x] HTML mode for perfect text quality
- [x] Device pixel ratio support
- [x] Jump-to-index button
- [x] Windows executable release
- [x] Clickable PDF links (internal navigation + external URLs)
- [x] Table of Contents sidebar with search
- [x] Collapsible TOC hierarchy with H1 grouping
- [x] Zoom & pan with cursor states
- [x] Mobile-optimized toolbar and layout
- [ ] PDF.js integration for client-side rendering option
- [ ] Thumbnail navigation sidebar
- [ ] Annotation support
- [ ] Custom themes/templates
- [ ] Page flip sound effects
- [ ] Night/dark reading mode
- [ ] Export to EPUB/other formats

See the [open issues](https://github.com/vedanttalnikar/pdf-flipbook-animator-commercial/issues) for a full list of proposed features and known issues.

## ⭐ Star History

If you find this project useful, please consider giving it a star!

---

<p align="center">
  Made with ❤️ by <a href="mailto:vedanttalnikar@gmail.com">Vedant Talnikar</a>
</p>

<p align="center">
  <a href="#top">Back to top ↑</a>
</p>
