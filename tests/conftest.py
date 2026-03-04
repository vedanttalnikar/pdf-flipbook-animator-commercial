"""Pytest configuration and shared fixtures."""

import pytest
from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image

from pdf_flipbook_animator.config import Config


@pytest.fixture
def sample_pdf(tmp_path):
    """Create a simple test PDF with 3 pages."""
    pdf_path = tmp_path / "test.pdf"
    doc = fitz.open()
    
    # Create 3 pages with different content
    for i in range(3):
        page = doc.new_page(width=595, height=842)  # A4 size
        text = f"Page {i + 1}"
        page.insert_text((50, 50), text, fontsize=24)
        
        # Draw a rectangle to make each page unique
        rect = fitz.Rect(100, 100, 200 + i * 50, 200 + i * 50)
        page.draw_rect(rect, color=(0, 0, 0), width=2)
    
    doc.save(pdf_path)
    doc.close()
    
    return pdf_path


@pytest.fixture
def sample_image(tmp_path):
    """Create a simple test image."""
    img_path = tmp_path / "test.png"
    img = Image.new("RGB", (800, 600), color=(73, 109, 137))
    img.save(img_path)
    return img_path


@pytest.fixture
def temp_output_dir(tmp_path):
    """Create and return a temporary output directory."""
    output = tmp_path / "output"
    output.mkdir()
    return output


@pytest.fixture
def default_config():
    """Return a default configuration object."""
    return Config()


@pytest.fixture
def custom_config():
    """Return a custom configuration object."""
    return Config(
        dpi=200,
        quality=90,
        title="Test Flipbook",
        primary_color="#FF5722",
    )


@pytest.fixture
def mock_metadata():
    """Return mock conversion metadata."""
    return {
        "page_count": 3,
        "images": [
            "images/page_001.webp",
            "images/page_002.webp",
            "images/page_003.webp",
        ],
        "dimensions": (1240, 1754),
        "total_size_bytes": 1500000,
        "total_size_mb": 1.43,
        "dpi": 150,
        "average_page_size_kb": 488.28,
    }
