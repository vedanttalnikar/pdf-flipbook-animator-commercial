"""PDF conversion functionality using PyMuPDF."""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import fitz  # PyMuPDF
from PIL import Image

from pdf_flipbook_animator.config import Config
from pdf_flipbook_animator.utils.image import convert_to_webp, create_jpg_fallback

logger = logging.getLogger(__name__)


class PDFConverter:
    """Convert PDF pages to images for flipbook animation."""

    def __init__(self, config: Optional[Config] = None):
        """Initialize PDF converter with configuration.

        Args:
            config: Configuration object. Uses defaults if not provided.
        """
        self.config = config or Config()

    def convert_to_images(
        self, pdf_path: Path, output_dir: Path
    ) -> Dict[str, any]:
        """Convert PDF pages to images.

        Args:
            pdf_path: Path to input PDF file
            output_dir: Directory to save output images

        Returns:
            Dictionary with conversion metadata:
                - page_count: Number of pages converted
                - images: List of image paths
                - dimensions: (width, height) of first page
                - file_sizes: Total size of generated images

        Raises:
            FileNotFoundError: If PDF file doesn't exist
            ValueError: If PDF is corrupted or invalid
            PermissionError: If cannot write to output directory
        """
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        # Create output directories
        images_dir = output_dir / "images"
        images_dir.mkdir(parents=True, exist_ok=True)

        if self.config.output_format == "webp":
            fallback_dir = images_dir / "fallback"
            fallback_dir.mkdir(exist_ok=True)

        logger.info(f"Converting PDF: {pdf_path}")
        logger.info(f"Output directory: {output_dir}")
        logger.info(f"DPI: {self.config.dpi}, Quality: {self.config.quality}")

        try:
            doc = fitz.open(pdf_path)
        except Exception as e:
            raise ValueError(f"Failed to open PDF: {e}")

        if doc.page_count == 0:
            raise ValueError("PDF has no pages")

        images = []
        total_size = 0
        dimensions = None

        # Calculate zoom factor for desired DPI
        # PyMuPDF default is 72 DPI
        zoom = self.config.dpi / 72.0
        mat = fitz.Matrix(zoom, zoom)

        for page_num in range(doc.page_count):
            try:
                page = doc[page_num]
                # Enhanced rendering with explicit colorspace and annotations
                pix = page.get_pixmap(
                    matrix=mat,
                    alpha=False,
                    colorspace=fitz.csRGB,  # Explicit RGB for consistent quality
                    annots=True  # Render annotations for better text
                )

                # Convert to PIL Image
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

                # Store dimensions from first page
                if dimensions is None:
                    dimensions = (pix.width, pix.height)

                # Save as WebP
                page_filename = f"page_{page_num + 1:03d}"
                webp_path = images_dir / f"{page_filename}.webp"

                img_size = convert_to_webp(
                    img, webp_path, quality=self.config.quality, lossless=self.config.lossless_webp
                )
                total_size += img_size

                images.append(str(webp_path.relative_to(output_dir)))

                # Create JPG fallback
                jpg_path = fallback_dir / f"{page_filename}.jpg"
                jpg_size = create_jpg_fallback(
                    img, jpg_path, quality=self.config.jpg_quality
                )
                total_size += jpg_size

                logger.info(
                    f"Converted page {page_num + 1}/{doc.page_count}: "
                    f"{webp_path.name} ({img_size // 1024} KB)"
                )

            except Exception as e:
                logger.error(f"Failed to convert page {page_num + 1}: {e}")
                raise

        doc.close()

        metadata = {
            "page_count": len(images),
            "images": images,
            "dimensions": dimensions,
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "dpi": self.config.dpi,
            "average_page_size_kb": round(total_size / len(images) / 1024, 2),
        }

        logger.info(
            f"Conversion complete: {len(images)} pages, "
            f"{metadata['total_size_mb']} MB total"
        )

        return metadata

    def extract_links(self, pdf_path: Path) -> Dict[int, List[Dict[str, any]]]:
        """Extract internal page links and external URL links from PDF.
        
        Args:
            pdf_path: Path to input PDF file
            
        Returns:
            Dictionary mapping page numbers (1-based) to lists of link objects:
            {
                1: [
                    {
                        'type': 'internal',
                        'target_page': 5,
                        'rect': {...}
                    },
                    {
                        'type': 'external',
                        'url': 'https://example.com',
                        'rect': {...}
                    }
                ]
            }
        """
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        logger.info(f"Extracting links from: {pdf_path}")
        
        try:
            doc = fitz.open(pdf_path)
        except Exception as e:
            raise ValueError(f"Failed to open PDF: {e}")
        
        links_data = {}
        total_links = 0
        internal_links = 0
        external_links = 0
        
        for page_num in range(doc.page_count):
            page = doc[page_num]
            page_links = page.get_links()
            
            if not page_links:
                continue
            
            extracted_links = []
            
            for link in page_links:
                link_kind = link.get('kind')
                
                # Process internal page navigation links
                if link_kind == fitz.LINK_GOTO:
                    total_links += 1
                    internal_links += 1
                    
                    dest_page = link.get('page', -1)
                    if dest_page < 0:
                        continue  # Skip invalid destinations
                    
                    # Get link rectangle
                    link_rect = link['from']
                    
                    # Convert to percentages for responsive positioning
                    rect_data = {
                        'x': (link_rect.x0 / page.rect.width) * 100,
                        'y': (link_rect.y0 / page.rect.height) * 100,
                        'width': ((link_rect.x1 - link_rect.x0) / page.rect.width) * 100,
                        'height': ((link_rect.y1 - link_rect.y0) / page.rect.height) * 100,
                    }
                    
                    link_data = {
                        'type': 'internal',
                        'target_page': dest_page + 1,  # Convert to 1-based
                        'rect': rect_data,
                    }
                    
                    extracted_links.append(link_data)
                
                # Process external URL links
                elif link_kind == fitz.LINK_URI:
                    total_links += 1
                    external_links += 1
                    
                    url = link.get('uri', '')
                    if not url:
                        continue  # Skip empty URLs
                    
                    # Get link rectangle
                    link_rect = link['from']
                    
                    # Convert to percentages for responsive positioning
                    rect_data = {
                        'x': (link_rect.x0 / page.rect.width) * 100,
                        'y': (link_rect.y0 / page.rect.height) * 100,
                        'width': ((link_rect.x1 - link_rect.x0) / page.rect.width) * 100,
                        'height': ((link_rect.y1 - link_rect.y0) / page.rect.height) * 100,
                    }
                    
                    link_data = {
                        'type': 'external',
                        'url': url,
                        'rect': rect_data,
                    }
                    
                    extracted_links.append(link_data)
            
            if extracted_links:
                links_data[page_num + 1] = extracted_links  # Store with 1-based page number
        
        doc.close()
        
        logger.info(
            f"Link extraction complete: {internal_links} internal links, "
            f"{external_links} external links found on {len(links_data)} pages"
        )
        
        return links_data

    def extract_toc(self, pdf_path: Path) -> List[Dict[str, any]]:
        """Extract table of contents / bookmarks from PDF.
        
        Uses PyMuPDF's get_toc() to extract the PDF bookmark tree.
        
        Args:
            pdf_path: Path to input PDF file
            
        Returns:
            List of TOC entries, each a dict with:
            {
                'level': int,      # Nesting level (1 = top-level)
                'title': str,      # Chapter/section title
                'page': int        # Target page number (1-based)
            }
        """
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        logger.info(f"Extracting TOC from: {pdf_path}")
        
        try:
            doc = fitz.open(pdf_path)
        except Exception as e:
            raise ValueError(f"Failed to open PDF: {e}")
        
        toc_raw = doc.get_toc()
        doc.close()
        
        if not toc_raw:
            logger.info("No TOC/bookmarks found in PDF")
            return []
        
        toc_data = []
        for entry in toc_raw:
            level, title, page = entry[0], entry[1], entry[2]
            title = title.strip()
            if not title or page < 1:
                continue
            toc_data.append({
                'level': level,
                'title': title,
                'page': page,
            })
        
        logger.info(f"TOC extraction complete: {len(toc_data)} entries")
        return toc_data

    def get_pdf_info(self, pdf_path: Path) -> Dict[str, any]:
        """Get basic information about a PDF file.

        Args:
            pdf_path: Path to PDF file

        Returns:
            Dictionary with PDF metadata
        """
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        try:
            doc = fitz.open(pdf_path)
            metadata = doc.metadata
            page_count = doc.page_count

            # Get dimensions of first page
            if page_count > 0:
                page = doc[0]
                rect = page.rect
                dimensions = (int(rect.width), int(rect.height))
            else:
                dimensions = (0, 0)

            doc.close()

            return {
                "page_count": page_count,
                "dimensions": dimensions,
                "title": metadata.get("title", ""),
                "author": metadata.get("author", ""),
                "subject": metadata.get("subject", ""),
                "producer": metadata.get("producer", ""),
            }
        except Exception as e:
            raise ValueError(f"Failed to read PDF info: {e}")
