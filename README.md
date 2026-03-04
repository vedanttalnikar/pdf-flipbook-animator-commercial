# PDF Flipbook Animator

[![Python Versions](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Source--Available%20Commercial-red.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.2.0-green.svg)](CHANGELOG.md)

> **📢 Public Repository Notice:**  
> This repository is **publicly visible for transparency and evaluation purposes only**.  
> The code is **NOT open source** - it's commercial software with a source-available license.  
> You can view and evaluate the code, but **a paid license is required for any production use**.  
> See [LICENSE](LICENSE) for details.

**Professional PDF to Flipbook Converter - Premium Animation Effects**

Transform any PDF into an interactive, web-based flipbook with stunning page-turning animations. Choose from simple transitions to realistic 3D page curl effects. Perfect for e-books, magazines, catalogs, and presentations.

[🎬 **Live Demo** →](https://vedanttalnikar.github.io/pdf-flipbook-animator-commercial/) | [💼 Buy Now](https://pdf-flipbook-animator.com/pricing) | [📖 Full Documentation](OUTPUT_USAGE_GUIDE.md) | [💬 Support](https://github.com/vedanttalnikar/pdf-flipbook-animator-commercial/issues)

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
- 🚀 **Easy CLI** - Simple command-line interface
- 🎨 **Customizable** - Control colors, quality, and layout
- 📱 **Responsive** - Works on all devices and screen sizes
- ⚡ **Optimized** - WebP images with lazy loading
- 🌐 **Static Output** - Host anywhere (GitHub Pages, Netlify, etc.)
- ⌨️ **Keyboard Navigation** - Full keyboard support
- 🖥️ **Fullscreen Mode** - Immersive reading experience
- 💾 **Position Memory** - Remembers where you left off
- 🔄 **Batch Processing** - Convert multiple PDFs at once

## 🎬 Live Demo

**[→ Try the Interactive Demo](https://vedanttalnikar.github.io/pdf-flipbook-animator-commercial/)**

Experience a real 52-page magazine flipbook with **Realistic Mode**:
- ✅ **Side panel layout** - Maximum vertical space for PDF viewing
- ✅ **200 DPI resolution** - Crystal clear text and images
- ✅ **Fully responsive** - Auto-adapts to desktop/tablet/mobile
- ✅ **Touch/swipe gestures** - Natural mobile interaction
- ✅ **Keyboard navigation** - Arrow keys, Page Up/Down, Home/End
- ✅ **Physics-based animation** - Realistic page curl with shadows
- ✅ **58 MB total size** - High quality WebP optimized images
- ✅ **Works everywhere** - Phone, tablet, desktop browsers

**Quick Start:**
```bash
pdf-flipbook convert book.pdf
# ✅ Flipbook created at: output/book/
```

## � Pricing & Licenses

### Choose Your Plan

| License Type | Users | Price | Features |
|-------------|-------|-------|----------|
| **Trial** | 1 user | Free (14 days) | All features, watermarked output |
| **Personal** | 1 user | $49/year | All animation modes, unlimited conversions |
| **Team** | 5 users | $199/year | Priority support, team collaboration |
| **Enterprise** | Unlimited | $599/year | White-label, API access, dedicated support |

[**Start Free Trial →**](https://pdf-flipbook-animator.com/trial) | [**View All Plans →**](https://pdf-flipbook-animator.com/pricing)

### 30-Day Money-Back Guarantee
Not satisfied? Get a full refund within 30 days of purchase.

---

## 📦 Installation

### Requirements

- Python 3.9+
- Valid license key (get yours at [pdf-flipbook-animator.com](https://pdf-flipbook-animator.com))

### Install via pip

```bash
pip install pdf-flipbook-animator
```

### Activate Your License

```bash
pdf-flipbook activate YOUR-LICENSE-KEY
```

## 🚀 Quick Start

### Convert a PDF

```bash
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

# High quality output
pdf-flipbook convert document.pdf --dpi 200 --quality 95

# Animation modes
pdf-flipbook convert book.pdf --animation-mode simple      # Fast (default)
pdf-flipbook convert book.pdf --animation-mode 3d-css      # 3D page fold
pdf-flipbook convert book.pdf --animation-mode realistic   # Realistic page curl

# Custom animation timing
pdf-flipbook convert book.pdf -a realistic --flip-duration 1000

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
| `--dpi` | Image resolution (72-600) | `150` |
| `--quality` | WebP quality (1-100) | `85` |
| `--jpg-quality` | JPG fallback quality | `90` |
| `--title` | Flipbook title | PDF filename |
| `--single-page` | Single page mode | `False` |
| `--no-fullscreen` | Disable fullscreen button | `False` |
| `--primary-color` | Primary UI color | `#2196F3` |
| `--animation-mode, -a` | Animation style: `simple`, `3d-css`, `realistic` | `simple` |
| `--flip-duration` | Animation duration in ms (200-2000) | `800` |
| `--enable-curl` | Enable 3D page curl (realistic mode) | `False` |

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
pdf-flipbook batch ./pdfs/ -o ./flipbooks/ --dpi 200
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
pdf-flipbook convert book.pdf --animation-mode realistic --dpi 200 --quality 95
```

**NEW Features (v0.2.0):**
- ✅ **Side Panel Layout** - Maximizes vertical space (~99vh for PDF)
- ✅ **Fully Responsive** - Auto-switches between single/two-page spread
- ✅ **Dynamic Perspective** - 1200px (mobile), 1800px (tablet), 2400px (desktop)
- ✅ **Physics-Based Animations** - Realistic page curl with dynamic shadows
- ✅ **Interactive Dragging** - Click and drag pages to flip
- ✅ **Touch Optimized** - Swipe gestures on mobile devices
- ✅ **Window Resize Handling** - Automatically reinitializes on orientation change
- ✅ **Smart Navigation** - Buttons adapt to single-page or two-page mode
- ✅ **High DPI Support** - Crisp rendering at 150-200 DPI
- ✅ **Fullscreen Mode** - Semi-transparent side panels

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

| Mode | Performance | Visual Effect | Layout | Responsive | Best For |
|------|-------------|---------------|--------|------------|----------|
| Simple | ⚡⚡⚡ 60 FPS | Basic fade | Traditional | Yes | Large PDFs, fast loading |
| 3D CSS | ⚡⚡ 60 FPS | Page fold | Traditional | Yes | Balanced visual appeal |
| Realistic | ⚡ 30-60 FPS | Realistic curl | **Side Panels** | **Fully Adaptive** | Professional publications |

**Recommended Settings:**
```bash
# Best quality for magazines/catalogs
pdf-flipbook convert magazine.pdf -a realistic --dpi 200 --quality 95

# Balanced quality/performance
pdf-flipbook convert book.pdf -a realistic --dpi 150 --quality 90

# Fast loading, good quality
pdf-flipbook convert doc.pdf -a realistic --dpi 120 --quality 85
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

## 🎨 Customization

### Colors

```bash
pdf-flipbook convert doc.pdf --primary-color "#9C27B0"
```

### Quality vs Size

| DPI | Quality | Use Case | Avg Size/Page |
|-----|---------|----------|---------------|
| 96 | Low | Preview | ~200 KB |
| 150 | **Recommended** | Web viewing | ~400 KB |
| 200 | High | Detailed docs | ~700 KB |
| 300 | Print | High detail | ~1.5 MB |

## 🛠️ Development

### Setup

```bash
git clone https://github.com/yourusername/pdf-flipbook-animator.git
cd pdf-flipbook-animator

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

## 📊 Project Status

- ✅ Core functionality complete
- ✅ CLI interface finished
- ✅ Comprehensive tests
- ✅ Documentation complete
- 🚧 Additional features planned (see [Issues](https://github.com/yourusername/pdf-flipbook-animator/issues))

## 🤝 Contributing

Contributions are welcome! Please see our [Contributing Guidelines](CONTRIBUTING.md).

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [PyMuPDF](https://pymupdf.readthedocs.io/) - Excellent PDF processing library
- [Pillow](https://python-pillow.org/) - Powerful image manipulation
- [Click](https://click.palletsprojects.com/) - Beautiful CLI framework
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) - Gorgeous documentation

## 📞 Support

**Documentation:**
- 📖 [Complete Output & Usage Guide](OUTPUT_USAGE_GUIDE.md) - Mobile, web, hosting, all API options
- 📱 [Mobile Device Testing](MOBILE_TESTING.md) - Touch/swipe testing procedures
- 💼 [Commercial Setup Guide](COMMERCIAL_SETUP.md) - Licensing and monetization
- 📝 [Changelog](CHANGELOG.md) - Version history

**Community:**
- 🐛 [Issue Tracker](https://github.com/yourusername/pdf-flipbook-animator/issues)
- 💬 [Discussions](https://github.com/yourusername/pdf-flipbook-animator/discussions)
- 📧 Email: support@pdf-flipbook-animator.com

## 🗺️ Roadmap

- [ ] PDF.js integration for client-side rendering option
- [ ] Thumbnail navigation sidebar
- [ ] Search functionality
- [ ] Annotation support
- [ ] Table of contents generation
- [ ] Custom themes/templates
- [ ] Progress statistics
- [ ] Export to EPUB/other formats

See the [open issues](https://github.com/yourusername/pdf-flipbook-animator/issues) for a full list of proposed features and known issues.

## ⭐ Star History

If you find this project useful, please consider giving it a star!

---

<p align="center">
  Made with ❤️ by the PDF Flipbook Animator community
</p>

<p align="center">
  <a href="#top">Back to top ↑</a>
</p>
