"""HTML flipbook generator."""

import json
import logging
import shutil
from pathlib import Path
from typing import Dict, List, Optional

from pdf_flipbook_animator.config import Config

logger = logging.getLogger(__name__)


class FlipbookGenerator:
    """Generate HTML flipbook viewer from images."""

    def __init__(self, config: Optional[Config] = None):
        """Initialize flipbook generator with configuration.

        Args:
            config: Configuration object. Uses defaults if not provided.
        """
        self.config = config or Config()

    def generate(
        self,
        images_dir: Path,
        output_dir: Path,
        metadata: Dict[str, any],
        title: Optional[str] = None,
    ) -> Path:
        """Generate complete flipbook HTML viewer.

        Args:
            images_dir: Directory containing page images
            output_dir: Root output directory
            metadata: Conversion metadata from PDFConverter
            title: Optional title for the flipbook

        Returns:
            Path to generated index.html

        Raises:
            FileNotFoundError: If template files not found
        """
        title = title or self.config.title
        page_count = metadata["page_count"]
        images = metadata["images"]

        logger.info(f"Generating flipbook: {title}")
        logger.info(f"Pages: {page_count}, Output: {output_dir}")

        # Get template directory
        template_dir = self._get_template_dir()

        # Generate HTML
        html_content = self._generate_html(title, images, page_count, metadata)
        html_path = output_dir / "index.html"
        html_path.write_text(html_content, encoding="utf-8")
        logger.info(f"Generated: {html_path}")

        # Copy/generate CSS
        css_dir = output_dir / "css"
        css_dir.mkdir(exist_ok=True)
        css_content = self._generate_css()
        css_path = css_dir / "style.css"
        css_path.write_text(css_content, encoding="utf-8")
        logger.info(f"Generated: {css_path}")

        # Copy/generate JavaScript
        js_dir = output_dir / "js"
        js_dir.mkdir(exist_ok=True)
        js_content = self._generate_js(page_count, images)
        js_path = js_dir / "flipbook.js"
        js_path.write_text(js_content, encoding="utf-8")
        logger.info(f"Generated: {js_path}")

        # Copy PageFlip library (using CDN fallback for now)
        logger.info("Using PageFlip.js from CDN")

        logger.info(f"Flipbook generated successfully: {html_path}")
        return html_path

    def _get_template_dir(self) -> Path:
        """Get path to template directory."""
        if self.config.template_dir:
            return self.config.template_dir

        # Try to get bundled templates
        try:
            from importlib.resources import files
            return files("pdf_flipbook_animator").joinpath("templates")
        except (ImportError, AttributeError):
            # Fallback for development
            pkg_dir = Path(__file__).parent.parent
            return pkg_dir / "templates"

    def _generate_html(
        self, title: str, images: List[str], page_count: int, metadata: Dict
    ) -> str:
        """Generate HTML content."""
        # Build image list
        image_elements = []
        for i, img_path in enumerate(images):
            # Convert backslashes to forward slashes for web
            web_path = img_path.replace("\\", "/")
            image_elements.append(
                f'        <div class="page" data-page="{i + 1}">\n'
                f'            <img src="{web_path}" alt="Page {i + 1}" loading="lazy">\n'
                f"        </div>"
            )

        images_html = "\n".join(image_elements)

        # Generate full HTML
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{title} - Interactive PDF Flipbook">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="Interactive flipbook with {page_count} pages">
    <meta property="og:type" content="website">
    <title>{title} | Flipbook</title>
    <link rel="stylesheet" href="css/style.css">
    <link rel="preconnect" href="https://cdn.jsdelivr.net">
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>{title}</h1>
            <div class="header-controls">
                {'<button id="fullscreen-btn" class="control-btn" title="Fullscreen (F)">⛶</button>' if self.config.enable_fullscreen else ''}
                <span class="page-indicator">
                    Page <span id="current-page">1</span> of <span id="total-pages">{page_count}</span>
                </span>
            </div>
        </header>

        <main class="main">
            <div id="flipbook" class="flipbook">
{images_html}
            </div>
            
            <div class="loading-spinner" id="loading">
                <div class="spinner"></div>
                <p>Loading flipbook...</p>
            </div>
        </main>

        <nav class="controls">
            <button id="prev-btn" class="nav-btn" title="Previous (←)">
                <span>←</span> Previous
            </button>
            <div class="progress-bar">
                <div class="progress-fill" id="progress"></div>
            </div>
            <button id="next-btn" class="nav-btn" title="Next (→)">
                Next <span>→</span>
            </button>
        </nav>

        <footer class="footer">
            <p>Use arrow keys to navigate • Click pages to flip • Press F for fullscreen</p>
            <p class="credit">Powered by <a href="https://github.com/yourusername/pdf-flipbook-animator" target="_blank">PDF Flipbook Animator</a></p>
        </footer>
    </div>

    <script src="js/flipbook.js"></script>
</body>
</html>
"""
        return html

    def _generate_css(self) -> str:
        """Generate CSS stylesheet."""
        css = f"""/* PDF Flipbook Animator Styles */

:root {{
    --primary-color: {self.config.primary_color};
    --bg-color: {self.config.background_color};
    --text-color: #333;
    --border-color: #ddd;
    --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    --transition: all 0.3s ease;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    background: var(--bg-color);
    color: var(--text-color);
    line-height: 1.6;
    overflow-x: hidden;
}}

.container {{
    max-width: 1920px;
    margin: 0 auto;
    padding: 20px;
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}}

/* Header */
.header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 0;
    border-bottom: 2px solid var(--border-color);
    margin-bottom: 30px;
}}

.header h1 {{
    font-size: 2rem;
    color: var(--primary-color);
    font-weight: 600;
}}

.header-controls {{
    display: flex;
    gap: 15px;
    align-items: center;
}}

.control-btn {{
    background: var(--primary-color);
    color: white;
    border: none;
    padding: 10px 15px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1.2rem;
    transition: var(--transition);
}}

.control-btn:hover {{
    opacity: 0.8;
    transform: scale(1.05);
}}

.page-indicator {{
    font-size: 1rem;
    font-weight: 500;
    color: var(--text-color);
    background: white;
    padding: 10px 20px;
    border-radius: 5px;
    box-shadow: var(--shadow);
}}

/* Main Content */
.main {{
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    padding: 20px 0;
}}

.flipbook {{
    max-width: 100%;
    max-height: 80vh;
    min-height: 400px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    border-radius: 10px;
    overflow: hidden;
    background: white;
    position: relative;
}}

.page {{
    display: none;
    width: 100%;
    height: 100%;
    background: white;
    position: absolute;
    top: 0;
    left: 0;
}}

.page.active {{
    display: flex;
    justify-content: center;
    align-items: center;
    position: absolute;
}}

.page img {{
    max-width: 100%;
    max-height: 80vh;
    object-fit: contain;
    display: block;
}}

/* Loading Spinner */
.loading-spinner {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    display: none;
}}

.loading-spinner.show {{
    display: block;
}}

.spinner {{
    border: 4px solid #f3f3f3;
    border-top: 4px solid var(--primary-color);
    border-radius: 50%;
    width: 50px;
    height: 50px;
    animation: spin 1s linear infinite;
    margin: 0 auto 20px;
}}

@keyframes spin {{
    0% {{ transform: rotate(0deg); }}
    100% {{ transform: rotate(360deg); }}
}}

/* Controls */
.controls {{
    display: flex;
    gap: 20px;
    align-items: center;
    justify-content: center;
    padding: 30px 0;
    margin-top: auto;
}}

.nav-btn {{
    background: var(--primary-color);
    color: white;
    border: none;
    padding: 15px 30px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1rem;
    font-weight: 500;
    transition: var(--transition);
    display: flex;
    align-items: center;
    gap: 10px;
}}

.nav-btn:hover:not(:disabled) {{
    background: color-mix(in srgb, var(--primary-color) 80%, black);
    transform: translateY(-2px);
    box-shadow: var(--shadow);
}}

.nav-btn:disabled {{
    opacity: 0.4;
    cursor: not-allowed;
}}

.progress-bar {{
    flex: 1;
    max-width: 400px;
    height: 8px;
    background: #e0e0e0;
    border-radius: 4px;
    overflow: hidden;
}}

.progress-fill {{
    height: 100%;
    background: var(--primary-color);
    transition: width 0.3s ease;
    border-radius: 4px;
}}

/* Footer */
.footer {{
    text-align: center;
    padding: 20px 0;
    border-top: 2px solid var(--border-color);
    margin-top: 20px;
    color: #666;
    font-size: 0.9rem;
}}

.footer p {{
    margin: 5px 0;
}}

.footer a {{
    color: var(--primary-color);
    text-decoration: none;
}}

.footer a:hover {{
    text-decoration: underline;
}}

/* Responsive Design */

/* Two-page spread for desktop */
@media (min-width: 1024px) {{
    .flipbook {{
        max-width: 1400px;
        display: flex;
        justify-content: center;
        align-items: center;
    }}

    .page {{
        max-width: 50%;
        flex: 0 0 auto;
        position: relative !important;
    }}

    .page img {{
        width: 100%;
        height: auto;
        max-height: 80vh;
    }}

    /* Book spine shadow effect between pages */
    .page.active:first-child {{
        box-shadow: 3px 0 10px rgba(0,0,0,0.2);
    }}

    .page.active + .page.active {{
        box-shadow: -3px 0 10px rgba(0,0,0,0.2);
    }}
}}

/* Single page for mobile/tablet */
@media (max-width: 1023px) {{
    .flipbook {{
        max-width: 100%;
        display: block;
    }}

    .page {{
        max-width: 100%;
        width: 100%;
        position: absolute !important;
    }}
}}

@media (max-width: 768px) {{
    .header {{
        flex-direction: column;
        gap: 15px;
        text-align: center;
    }}

    .header h1 {{
        font-size: 1.5rem;
    }}

    .controls {{
        flex-direction: column;
        gap: 15px;
    }}

    .progress-bar {{
        width: 100%;
        max-width: none;
    }}

    .nav-btn {{
        width: 100%;
        justify-content: center;
    }}

    .page img {{
        max-height: 60vh;
    }}
}}

@media (max-width: 480px) {{
    .container {{
        padding: 10px;
    }}

    .header h1 {{
        font-size: 1.2rem;
    }}

    .page-indicator {{
        font-size: 0.9rem;
        padding: 8px 15px;
    }}
}}

/* Fullscreen Mode */
.container:fullscreen {{
    background: var(--bg-color);
}}

.container:fullscreen .page img {{
    max-height: 95vh;
}}

/* Dark Mode Support */
@media (prefers-color-scheme: dark) {{
    :root {{
        --bg-color: #1a1a1a;
        --text-color: #e0e0e0;
        --border-color: #444;
    }}

    body {{
        background: var(--bg-color);
        color: var(--text-color);
    }}

    .page-indicator {{
        background: #2a2a2a;
        color: var(--text-color);
    }}
}}

/* Print Styles */
@media print {{
    .header, .controls, .footer {{
        display: none !important;
    }}

    .page {{
        display: block !important;
        page-break-after: always;
    }}

    .page img {{
        max-height: 100vh;
        page-break-inside: avoid;
    }}
}}
"""
        return css

    def _generate_js(self, page_count: int, images: List[str]) -> str:
        """Generate JavaScript code based on animation mode."""
        # Select template based on animation mode
        animation_mode = self.config.animation_mode
        template_name = f"flipbook_{animation_mode.replace('-', '_')}.js"
        
        # Try to load template from templates directory
        template_dir = self._get_template_dir()
        template_path = template_dir / "js" / template_name
        
        if template_path.exists():
            logger.info(f"Using template: {template_name}")
            return template_path.read_text(encoding="utf-8")
        
        # Fallback to inline simple mode
        logger.warning(f"Template {template_name} not found, using inline simple mode")
        js = """// PDF Flipbook Animator Script

class Flipbook {
    constructor() {
        this.currentPage = 1;
        this.totalPages = parseInt(document.getElementById('total-pages').textContent);
        this.pages = document.querySelectorAll('.page');
        
        this.init();
    }

    init() {
        // Show first page
        this.showPage(1);
        
        // Hide loading spinner
        const loading = document.getElementById('loading');
        if (loading) {
            loading.classList.remove('show');
        }

        // Setup event listeners
        this.setupControls();
        this.setupKeyboard();
        this.setupFullscreen();
        
        // Restore saved position
        this.restorePosition();
        
        // Update UI
        this.updateUI();

        console.log(`Flipbook initialized with ${this.totalPages} pages`);
    }

    setupControls() {
        const prevBtn = document.getElementById('prev-btn');
        const nextBtn = document.getElementById('next-btn');

        if (prevBtn) {
            prevBtn.addEventListener('click', () => this.previousPage());
        }

        if (nextBtn) {
            nextBtn.addEventListener('click', () => this.nextPage());
        }

        // Click on page to advance
        document.querySelectorAll('.page').forEach(page => {
            page.addEventListener('click', () => this.nextPage());
        });
    }

    setupKeyboard() {
        document.addEventListener('keydown', (e) => {
            switch(e.key) {
                case 'ArrowLeft':
                case 'ArrowUp':
                case 'PageUp':
                    e.preventDefault();
                    this.previousPage();
                    break;
                case 'ArrowRight':
                case 'ArrowDown':
                case 'PageDown':
                case ' ':
                    e.preventDefault();
                    this.nextPage();
                    break;
                case 'Home':
                    e.preventDefault();
                    this.goToPage(1);
                    break;
                case 'End':
                    e.preventDefault();
                    this.goToPage(this.totalPages);
                    break;
                case 'f':
                case 'F':
                    e.preventDefault();
                    this.toggleFullscreen();
                    break;
            }
        });
    }

    setupFullscreen() {
        const fullscreenBtn = document.getElementById('fullscreen-btn');
        if (fullscreenBtn) {
            fullscreenBtn.addEventListener('click', () => this.toggleFullscreen());
        }
    }

    showPage(pageNum) {
        if (pageNum < 1 || pageNum > this.totalPages) return;

        // Hide all pages
        this.pages.forEach(page => page.classList.remove('active'));

        // Show target page
        const targetPage = this.pages[pageNum - 1];
        if (targetPage) {
            targetPage.classList.add('active');
            this.currentPage = pageNum;
            
            // Preload adjacent pages
            this.preloadPages(pageNum);
            
            // Save position
            this.savePosition();
            
            // Update UI
            this.updateUI();
        }
    }

    preloadPages(currentPage) {
        // Preload next 2 pages
        for (let i = 1; i <= 2; i++) {
            const nextPage = currentPage + i;
            if (nextPage <= this.totalPages) {
                const img = this.pages[nextPage - 1].querySelector('img');
                if (img && !img.complete) {
                    img.loading = 'eager';
                }
            }
        }
    }

    nextPage() {
        if (this.currentPage < this.totalPages) {
            this.showPage(this.currentPage + 1);
        }
    }

    previousPage() {
        if (this.currentPage > 1) {
            this.showPage(this.currentPage - 1);
        }
    }

    goToPage(pageNum) {
        this.showPage(pageNum);
    }

    updateUI() {
        // Update page indicator
        const currentPageEl = document.getElementById('current-page');
        if (currentPageEl) {
            currentPageEl.textContent = this.currentPage;
        }

        // Update buttons
        const prevBtn = document.getElementById('prev-btn');
        const nextBtn = document.getElementById('next-btn');

        if (prevBtn) {
            prevBtn.disabled = this.currentPage === 1;
        }

        if (nextBtn) {
            nextBtn.disabled = this.currentPage === this.totalPages;
        }

        // Update progress bar
        const progress = document.getElementById('progress');
        if (progress) {
            const percentage = (this.currentPage / this.totalPages) * 100;
            progress.style.width = percentage + '%';
        }
    }

    toggleFullscreen() {
        const container = document.querySelector('.container');
        
        if (!document.fullscreenElement) {
            if (container.requestFullscreen) {
                container.requestFullscreen();
            } else if (container.webkitRequestFullscreen) {
                container.webkitRequestFullscreen();
            } else if (container.msRequestFullscreen) {
                container.msRequestFullscreen();
            }
        } else {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            } else if (document.webkitExitFullscreen) {
                document.webkitExitFullscreen();
            } else if (document.msExitFullscreen) {
                document.msExitFullscreen();
            }
        }
    }

    savePosition() {
        try {
            localStorage.setItem('flipbook_current_page', this.currentPage);
        } catch (e) {
            console.warn('Could not save position:', e);
        }
    }

    restorePosition() {
        try {
            const savedPage = localStorage.getItem('flipbook_current_page');
            if (savedPage) {
                const pageNum = parseInt(savedPage);
                if (pageNum >= 1 && pageNum <= this.totalPages) {
                    this.showPage(pageNum);
                }
            }
        } catch (e) {
            console.warn('Could not restore position:', e);
        }
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new Flipbook();
    });
} else {
    new Flipbook();
}
"""
        return js
