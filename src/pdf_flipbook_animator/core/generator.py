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
        <!-- Left Panel: Previous Navigation -->
        <aside class="left-panel">
            <button id="prev-btn" class="side-nav-btn" title="Previous Page (← or ↑)">
                <span class="arrow">←</span>
                <span class="label">Previous</span>
            </button>
        </aside>

        <!-- Center: Full-height Flipbook -->
        <main class="main">
            <div id="flipbook" class="flipbook">
{images_html}
            </div>
            
            <div class="loading-spinner" id="loading">
                <div class="spinner"></div>
                <p>Loading flipbook...</p>
            </div>
        </main>

        <!-- Right Panel: Next Navigation & Info -->
        <aside class="right-panel">
            <div class="panel-header">
                <h1 class="title">{title}</h1>
                {'<button id="fullscreen-btn" class="icon-btn" title="Toggle Fullscreen (F)">⛶</button>' if self.config.enable_fullscreen else ''}
            </div>
            
            <div class="page-info">
                <span class="page-indicator">
                    <span id="current-page">1</span> / <span id="total-pages">{page_count}</span>
                </span>
            </div>
            
            <button id="next-btn" class="side-nav-btn" title="Next Page (→ or ↓)">
                <span class="label">Next</span>
                <span class="arrow">→</span>
            </button>
            
            <div class="progress-container">
                <div class="progress-bar">
                    <div class="progress-fill" id="progress"></div>
                </div>
            </div>
            
            <div class="help-text">
                <p>🎯 Click or drag pages</p>
                <p>⌨️ Arrow keys to navigate</p>
                <p>🖱️ Press F for fullscreen</p>
            </div>
        </aside>
    </div>

    <script src="js/flipbook.js"></script>
</body>
</html>
"""
        return html

    def _generate_css(self) -> str:
        """Generate CSS stylesheet."""
        css = f"""/* PDF Flipbook Animator Styles - Fully Responsive */

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
    width: 100vw;
    height: 100vh;
    overflow: hidden;
}}

.container {{
    width: 100%;
    height: 100vh;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: row;
}}

/* Side Panels Layout (Desktop/Tablet Default) */
.left-panel,
.right-panel {{
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.98);
    border-right: 1px solid var(--border-color);
    padding: 15px 10px;
    gap: 20px;
}}

.left-panel {{
    width: 80px;
    border-right: 1px solid var(--border-color);
}}

.right-panel {{
    width: 180px;
    border-left: 1px solid var(--border-color);
    border-right: none;
    justify-content: flex-start;
    padding: 20px 15px;
}}

/* Side Navigation Buttons (Base Styles) */
.side-nav-btn {{
    background: var(--primary-color);
    color: white;
    border: none;
    padding: 12px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.85rem;
    font-weight: 600;
    transition: var(--transition);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    min-height: 80px;
    width: 100%;
}}

.side-nav-btn:hover:not(:disabled) {{
    background: color-mix(in srgb, var(--primary-color) 85%, black);
    transform: scale(1.05);
    box-shadow: var(--shadow);
}}

.side-nav-btn:disabled {{
    opacity: 0.4;
    cursor: not-allowed;
}}

.side-nav-btn .arrow {{
    font-size: 1.5rem;
    line-height: 1;
}}

.side-nav-btn .label {{
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

/* Panel Header */
.panel-header {{
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    margin-bottom: 15px;
    padding-bottom: 15px;
    border-bottom: 2px solid var(--primary-color);
}}

.panel-header .title {{
    font-size: 0.95rem;
    color: var(--primary-color);
    font-weight: 700;
    text-align: center;
    margin: 0;
    line-height: 1.3;
    word-break: break-word;
}}

.icon-btn {{
    background: var(--primary-color);
    color: white;
    border: none;
    padding: 8px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 1.1rem;
    transition: var(--transition);
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.icon-btn:hover {{
    background: color-mix(in srgb, var(--primary-color) 85%, black);
    transform: scale(1.05);
}}

/* Main Content - Full Height */
.main {{
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    padding: 0;
    width: 100%;
    height: 100vh;
    perspective: 2400px;
    perspective-origin: center center;
    overflow: hidden;
}}

.flipbook {{
    width: 100%;
    height: 100%;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    overflow: visible;
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
    max-height: 100%;
    width: auto;
    height: auto;
    object-fit: contain;
    display: block;
    image-rendering: -webkit-optimize-contrast;
    image-rendering: crisp-edges;
    -ms-interpolation-mode: nearest-neighbor;
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

/* Controls - Compact */
.controls {{
    flex-shrink: 0;
    display: flex;
    gap: 15px;
    align-items: center;
    justify-content: center;
    padding: 8px 15px;
    background: rgba(255, 255, 255, 0.95);
}}

.nav-btn {{
    background: var(--primary-color);
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 0.9rem;
    font-weight: 500;
    transition: var(--transition);
    display: flex;
    align-items: center;
    gap: 6px;
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

/* Page Info */
.page-info {{
    text-align: center;
    width: 100%;
    padding: 15px 0;
}}

.page-indicator {{
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--primary-color);
    display: block;
}}

/* Progress Bar */
.progress-container {{
    width: 100%;
    padding: 15px 0;
}}

.progress-bar {{
    width: 100%;
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

/* Help Text */
.help-text {{
    margin-top: auto;
    padding-top: 20px;
    text-align: center;
    color: #666;
    font-size: 0.7rem;
    line-height: 1.6;
    border-top: 1px solid var(--border-color);
}}

.help-text p {{
    margin: 4px 0;
}}

/* Responsive Design with Dynamic Perspective */

/* Mobile: VERTICAL LAYOUT (Header/Footer instead of Side Panels) */
@media (max-width: 767px) {{
    /* Switch to vertical column layout */
    .container {{
        flex-direction: column;
    }}
    
    .main {{
        perspective: 1200px;
        order: 2;
        flex: 1;
    }}
    
    /* Left panel becomes HEADER at top */
    .left-panel {{
        order: 1;
        width: 100%;
        height: auto;
        flex-direction: row;
        padding: 10px 15px;
        border-right: none;
        border-bottom: 1px solid var(--border-color);
        gap: 15px;
    }}
    
    /* Right panel becomes FOOTER at bottom */
    .right-panel {{
        order: 3;
        width: 100%;
        height: auto;
        flex-direction: row;
        padding: 10px 15px;
        border-left: none;
        border-top: 1px solid var(--border-color);
        gap: 15px;
        justify-content: space-between;
        align-items: center;
    }}
    
    /* Header/Footer button styling */
    .side-nav-btn {{
        flex-direction: row;
        min-height: auto;
        padding: 10px 20px;
        gap: 8px;
        width: auto;
        flex: 0 0 auto;
    }}
    
    .side-nav-btn .arrow {{
        font-size: 1.2rem;
    }}
    
    .side-nav-btn .label {{
        display: inline;
        font-size: 0.85rem;
    }}
    
    /* Panel header becomes horizontal */
    .panel-header {{
        flex-direction: row;
        border-bottom: none;
        border-right: 1px solid var(--border-color);
        padding: 0 15px 0 0;
        margin: 0;
        gap: 10px;
        flex: 1;
    }}
    
    .panel-header .title {{
        font-size: 0.9rem;
        text-align: left;
        writing-mode: horizontal-tb;
    }}
    
    .icon-btn {{
        width: 36px;
        height: 36px;
        font-size: 1rem;
        padding: 6px;
    }}
    
    /* Page info horizontal */
    .page-info {{
        padding: 0;
        flex: 0 0 auto;
    }}
    
    .page-indicator {{
        font-size: 0.95rem;
        writing-mode: horizontal-tb;
    }}
    
    /* Progress bar in footer */
    .progress-container {{
        padding: 0;
        flex: 1;
        max-width: 200px;
    }}
    
    .help-text {{
        display: none;
    }}
}}

/* Tablet: Adjusted side panels */
@media (min-width: 768px) and (max-width: 1023px) {{
    .main {{
        perspective: 1800px;
    }}
    
    .left-panel {{
        width: 70px;
    }}
    
    .right-panel {{
        width: 140px;
    }}
    
    .panel-header .title {{
        font-size: 0.85rem;
    }}
}}

/* Desktop: Two-page spread, full perspective */
@media (min-width: 1024px) {{
    .main {{
        perspective: 2400px;
    }}

    .flipbook {{
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
    }}

    /* Book spine shadow effect between pages */
    .page.active:first-child {{
        box-shadow: 3px 0 10px rgba(0,0,0,0.2);
    }}

    .page.active + .page.active {{
        box-shadow: -3px 0 10px rgba(0,0,0,0.2);
    }}
}}

/* Extra small mobile devices - Compact header/footer */
@media (max-width: 480px) {{
    .left-panel,
    .right-panel {{
        padding: 8px 10px;
        gap: 10px;
    }}
    
    .side-nav-btn {{
        padding: 8px 15px;
        font-size: 0.75rem;
    }}
    
    .side-nav-btn .arrow {{
        font-size: 1rem;
    }}
    
    .side-nav-btn .label {{
        font-size: 0.75rem;
    }}
    
    .panel-header .title {{
        font-size: 0.8rem;
    }}
    
    .page-indicator {{
        font-size: 0.85rem;
    }}
    
    .progress-container {{
        max-width: 120px;
    }}
}}

/* Fullscreen Mode - Semi-transparent side panels */
.container:fullscreen {{
    background: var(--bg-color);
    width: 100vw;
    height: 100vh;
}}

.container:fullscreen .left-panel,
.container:fullscreen .right-panel {{
    background: rgba(255, 255, 255, 0.85);
    opacity: 0.7;
    transition: opacity 0.3s;
}}

.container:fullscreen .left-panel:hover,
.container:fullscreen .right-panel:hover {{
    opacity: 1;
}}

.container:fullscreen .help-text {{
    opacity: 0.6;
}}

.container:fullscreen .main {{
    height: 100vh;
}}

.container:fullscreen .flipbook {{
    width: 100%;
    height: 100%;
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
