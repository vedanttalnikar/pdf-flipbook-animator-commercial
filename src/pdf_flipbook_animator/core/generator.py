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
        links_data: Optional[Dict[int, List[Dict]]] = None,
        toc_data: Optional[List[Dict]] = None,
    ) -> Path:
        """Generate complete flipbook HTML viewer.

        Args:
            images_dir: Directory containing page images
            output_dir: Root output directory
            metadata: Conversion metadata from PDFConverter
            title: Optional title for the flipbook
            links_data: Optional dictionary of clickable links per page
            toc_data: Optional list of TOC entries for sidebar navigation

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
        
        # Export links data if provided
        if links_data:
            links_json_path = output_dir / "links_data.json"
            links_json_path.write_text(
                json.dumps(links_data, indent=2),
                encoding="utf-8"
            )
            logger.info(f"Exported links data: {len(links_data)} pages with links")

        # Export TOC data if provided
        if toc_data:
            toc_json_path = output_dir / "toc_data.json"
            toc_json_path.write_text(
                json.dumps(toc_data, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )
            logger.info(f"Exported TOC data: {len(toc_data)} entries")

        # Generate HTML
        html_content = self._generate_html(title, images, page_count, metadata, links_data, toc_data)
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
        self, title: str, images: List[str], page_count: int, metadata: Dict, links_data: Optional[Dict] = None, toc_data: Optional[List[Dict]] = None
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
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes, maximum-scale=5.0, minimum-scale=1.0">
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
            </button>
        </aside>

        <!-- Center: Full-height Flipbook -->
        <main class="main">
            <div id="flipbook" class="flipbook">
{images_html}
            </div>
            
            <!-- Link overlay for clickable PDF links -->
            <div id="link-overlay"></div>
            
            <div class="loading-spinner" id="loading">
                <div class="spinner"></div>
                <p>Loading flipbook...</p>
            </div>
        </main>

        <!-- Right Panel: Next Navigation & Info -->
        <aside class="right-panel">
            <div class="panel-header">
                <h1 class="title">{title}</h1>
                {'<button id="toc-btn" class="icon-btn" title="Table of Contents">📋</button>' if toc_data else ''}
                {'<button id="index-btn" class="icon-btn" title="Jump to Index (Page ' + str(self.config.index_page) + ')" data-index-page="' + str(self.config.index_page) + '">📑</button>' if self.config.enable_index_button and page_count >= self.config.index_page else ''}
                {'<button id="fullscreen-btn" class="icon-btn" title="Toggle Fullscreen (F)">⛶</button>' if self.config.enable_fullscreen else ''}
            </div>
            
            <div class="zoom-controls">
                <button id="zoom-out-btn" class="zoom-btn" title="Zoom Out (Ctrl+-)">
                    <span>−</span>
                </button>
                <span id="zoom-level" class="zoom-level">100%</span>
                <button id="zoom-in-btn" class="zoom-btn" title="Zoom In (Ctrl++)">
                    <span>+</span>
                </button>
                <button id="zoom-reset-btn" class="zoom-btn" title="Reset Zoom (Ctrl+0)">
                    <span>⟲</span>
                </button>
            </div>
            
            <div class="page-info">
                <span class="page-indicator">
                    <span id="current-page">1</span> / <span id="total-pages">{page_count}</span>
                </span>
            </div>
            
            <button id="next-btn" class="side-nav-btn" title="Next Page (→ or ↓)">
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

    <!-- TOC Drawer -->
    {'<div id="toc-backdrop" class="toc-backdrop"></div>' if toc_data else ''}
    {'<div id="toc-drawer" class="toc-drawer"><div class="toc-header"><h2>📋 Table of Contents</h2><button id="toc-close-btn" class="toc-close-btn">&times;</button></div><div class="toc-search"><input type="text" id="toc-search-input" placeholder="Search chapters..." autocomplete="off"></div><ul id="toc-list" class="toc-list"></ul></div>' if toc_data else ''}

    <!-- Load links data if available -->
    <script>
        // Load links data asynchronously
        window.linksDataPromise = fetch('links_data.json')
            .then(response => response.ok ? response.json() : null)
            .then(data => {{ window.linksData = data; return data; }})
            .catch(() => null);
        
        // Load TOC data asynchronously
        window.tocDataPromise = fetch('toc_data.json')
            .then(response => response.ok ? response.json() : null)
            .then(data => {{ window.tocData = data; return data; }})
            .catch(() => null);
    </script>
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
    padding: 20px;
    border-radius: 8px;
    cursor: pointer;
    transition: var(--transition);
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    min-height: 60px;
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
    font-size: 2rem;
    line-height: 1;
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

.main.zoomed {{
    cursor: grab;
}}

.main.panning {{
    cursor: grabbing;
}}

.flipbook {{
    width: auto;
    height: auto;
    max-width: 100%;
    max-height: 100%;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    overflow: visible;
    background: white;
    position: relative;
    transform: translateZ(0);
    backface-visibility: hidden;
}}

#stpageflip-container {{
    transform: translateZ(0);
    backface-visibility: hidden;
    /* High-quality image rendering for smooth text */
    image-rendering: auto;
    image-rendering: -webkit-optimize-legibility;
    image-rendering: high-quality;
    -ms-interpolation-mode: bicubic;
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
    
    /* High-quality image rendering for sharp text */
    image-rendering: auto;
    image-rendering: -webkit-optimize-legibility;
    image-rendering: high-quality;
    -ms-interpolation-mode: bicubic;
    
    /* Font smoothing for text in images */
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}}

/* Link Overlay - Clickable PDF Links */
#link-overlay {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 1000;
}}

.pdf-link {{
    position: absolute;
    cursor: {self.config.link_cursor};
    pointer-events: auto;
    transition: background-color 0.2s ease;
    border-radius: 2px;
}}

.pdf-link:hover {{
    background-color: {self.config.link_hover_color};
}}

.pdf-link:active {{
    background-color: rgba(33, 150, 243, 0.3);
}}

/* Hide links during page flip animation */
#link-overlay.hidden {{
    opacity: 0;
    pointer-events: none;
}}

/* TOC Drawer */
.toc-backdrop {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    z-index: 2000;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.3s ease;
}}

.toc-backdrop.visible {{
    opacity: 1;
    pointer-events: auto;
}}

.toc-drawer {{
    position: fixed;
    top: 0;
    left: 0;
    width: 360px;
    max-width: 85vw;
    height: 100vh;
    background: #1a1a2e;
    color: #e0e0e0;
    z-index: 2001;
    transform: translateX(-100%);
    transition: transform 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    display: flex;
    flex-direction: column;
    box-shadow: 4px 0 20px rgba(0, 0, 0, 0.4);
}}

.toc-drawer.visible {{
    transform: translateX(0);
}}

.toc-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 20px;
    background: #16213e;
    border-bottom: 2px solid var(--primary-color);
    flex-shrink: 0;
}}

.toc-header h2 {{
    font-size: 1rem;
    font-weight: 700;
    color: white;
    margin: 0;
}}

.toc-close-btn {{
    background: none;
    border: none;
    color: #aaa;
    font-size: 1.6rem;
    cursor: pointer;
    padding: 2px 8px;
    border-radius: 4px;
    transition: all 0.2s;
    line-height: 1;
}}

.toc-close-btn:hover {{
    color: white;
    background: rgba(255, 255, 255, 0.1);
}}

.toc-search {{
    padding: 12px 16px;
    flex-shrink: 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}}

.toc-search input {{
    width: 100%;
    padding: 8px 12px;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 6px;
    color: #e0e0e0;
    font-size: 0.85rem;
    outline: none;
    transition: border-color 0.2s;
}}

.toc-search input::placeholder {{
    color: #777;
}}

.toc-search input:focus {{
    border-color: var(--primary-color);
}}

.toc-list {{
    list-style: none;
    padding: 8px 0;
    margin: 0;
    overflow-y: auto;
    flex: 1;
    scrollbar-width: thin;
    scrollbar-color: rgba(255,255,255,0.2) transparent;
}}

.toc-list::-webkit-scrollbar {{
    width: 6px;
}}

.toc-list::-webkit-scrollbar-track {{
    background: transparent;
}}

.toc-list::-webkit-scrollbar-thumb {{
    background: rgba(255, 255, 255, 0.2);
    border-radius: 3px;
}}

.toc-item {{
    padding: 10px 20px;
    cursor: pointer;
    transition: all 0.2s;
    border-left: 3px solid transparent;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 10px;
}}

.toc-item:hover {{
    background: rgba(255, 255, 255, 0.06);
    border-left-color: var(--primary-color);
}}

.toc-item.active {{
    background: rgba(33, 150, 243, 0.15);
    border-left-color: var(--primary-color);
    color: white;
}}

.toc-item.hidden {{
    display: none;
}}

.toc-item-title {{
    flex: 1;
    font-size: 0.85rem;
    line-height: 1.4;
    word-break: break-word;
}}

.toc-item-page {{
    font-size: 0.75rem;
    color: #888;
    flex-shrink: 0;
    padding-top: 2px;
}}

.toc-item.active .toc-item-page {{
    color: var(--primary-color);
}}

/* TOC level indentation */
.toc-item[data-level="1"] {{
    padding-left: 20px;
    font-weight: 700;
    font-size: 0.9rem;
}}

.toc-item[data-level="2"] {{
    padding-left: 32px;
    font-weight: 600;
}}

.toc-item[data-level="3"] {{
    padding-left: 44px;
    font-weight: 400;
    color: #bbb;
}}

.toc-item[data-level="4"] {{
    padding-left: 56px;
    font-weight: 400;
    color: #999;
    font-size: 0.8rem;
}}

.toc-no-results {{
    padding: 20px;
    text-align: center;
    color: #777;
    font-size: 0.85rem;
}}

/* Zoom Controls */
.zoom-controls {{
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px;
    background: rgba(255, 255, 255, 0.9);
    border-radius: 8px;
    border: 1px solid var(--border-color);
    margin-top: 10px;
}}

.zoom-btn {{
    background: white;
    border: 1px solid var(--border-color);
    border-radius: 4px;
    padding: 8px 12px;
    cursor: pointer;
    font-size: 18px;
    transition: var(--transition);
    min-width: 36px;
}}

.zoom-btn:hover {{
    background: var(--primary-color);
    color: white;
    transform: scale(1.05);
}}

.zoom-btn:active {{
    transform: scale(0.95);
}}

.zoom-level {{
    font-size: 14px;
    font-weight: 600;
    min-width: 50px;
    text-align: center;
    color: var(--text-color);
}}

.flipbook.zoomed {{
    cursor: grab;
}}

.flipbook.panning {{
    cursor: grabbing;
    pointer-events: none;
}}

.page {{
    touch-action: pan-x pan-y pinch-zoom;
    user-select: none;
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
        padding: 6px 10px;
        border-right: none;
        border-bottom: 1px solid var(--border-color);
        gap: 8px;
        align-items: center;
    }}
    
    /* Right panel becomes FOOTER at bottom */
    .right-panel {{
        order: 3;
        width: 100%;
        height: auto;
        flex-direction: row;
        flex-wrap: wrap;
        padding: 6px 10px;
        border-left: none;
        border-top: 1px solid var(--border-color);
        gap: 6px;
        justify-content: center;
        align-items: center;
    }}
    
    /* Header/Footer button styling */
    .side-nav-btn {{
        flex-direction: row;
        min-height: auto;
        padding: 8px 14px;
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
    
    /* Hide title on mobile to save space */
    .panel-header .title {{
        display: none;
    }}
    
    /* Panel header becomes a compact button row */
    .panel-header {{
        flex-direction: row;
        border-bottom: none;
        border-right: none;
        padding: 0;
        margin: 0;
        gap: 6px;
        flex: 0 0 auto;
        min-width: 0;
    }}
    
    .icon-btn {{
        width: 36px;
        height: 36px;
        font-size: 1rem;
        padding: 6px;
    }}
    
    /* Compact zoom controls inline */
    .zoom-controls {{
        margin-top: 0;
        padding: 4px 6px;
        gap: 4px;
        flex: 0 0 auto;
        border: 1px solid var(--border-color);
        border-radius: 6px;
    }}
    
    .zoom-btn {{
        padding: 4px 8px;
        font-size: 14px;
        min-width: 28px;
    }}
    
    .zoom-level {{
        font-size: 11px;
        min-width: 36px;
    }}
    
    /* Page info horizontal */
    .page-info {{
        padding: 0;
        flex: 0 0 auto;
    }}
    
    .page-indicator {{
        font-size: 0.9rem;
        writing-mode: horizontal-tb;
    }}
    
    /* Progress bar spans full width at bottom of footer */
    .progress-container {{
        padding: 0;
        flex: 1 1 100%;
        max-width: 100%;
        order: 10;
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
        max-width: 100%;
        width: auto;
        height: auto;
        object-fit: contain;
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
        padding: 5px 8px;
        gap: 5px;
    }}
    
    .side-nav-btn {{
        padding: 6px 10px;
        font-size: 0.75rem;
    }}
    
    .side-nav-btn .arrow {{
        font-size: 1rem;
    }}
    
    .side-nav-btn .label {{
        font-size: 0.75rem;
    }}
    
    .icon-btn {{
        width: 32px;
        height: 32px;
        font-size: 0.9rem;
        padding: 4px;
    }}
    
    .zoom-controls {{
        padding: 3px 4px;
        gap: 3px;
    }}
    
    .zoom-btn {{
        padding: 3px 6px;
        font-size: 12px;
        min-width: 24px;
    }}
    
    .zoom-level {{
        font-size: 10px;
        min-width: 30px;
    }}
    
    .page-indicator {{
        font-size: 0.8rem;
    }}
    
    .progress-container {{
        max-width: 100%;
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
