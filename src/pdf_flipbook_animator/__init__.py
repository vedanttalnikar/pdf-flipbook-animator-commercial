"""PDF Flipbook Animator - Professional PDF to Flipbook Converter."""

__version__ = "0.2.0"
__author__ = "PDF Flipbook Animator"
__license__ = "Proprietary"

from pdf_flipbook_animator.core.converter import PDFConverter
from pdf_flipbook_animator.core.generator import FlipbookGenerator

__all__ = ["PDFConverter", "FlipbookGenerator", "__version__"]
