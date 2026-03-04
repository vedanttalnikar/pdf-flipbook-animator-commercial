"""Unit tests for PDF converter."""

import pytest
from pathlib import Path

from pdf_flipbook_animator.core.converter import PDFConverter
from pdf_flipbook_animator.config import Config


def test_converter_initialization():
    """Test PDFConverter initializes correctly."""
    converter = PDFConverter()
    assert converter.config is not None
    assert converter.config.dpi == 150


def test_converter_with_custom_config(custom_config):
    """Test PDFConverter with custom configuration."""
    converter = PDFConverter(custom_config)
    assert converter.config.dpi == 200
    assert converter.config.quality == 90


def test_convert_basic_pdf(sample_pdf, temp_output_dir, default_config):
    """Test converting a basic PDF to images."""
    converter = PDFConverter(default_config)
    metadata = converter.convert_to_images(sample_pdf, temp_output_dir)
    
    # Check metadata
    assert metadata["page_count"] == 3
    assert len(metadata["images"]) == 3
    assert metadata["dpi"] == 150
    assert metadata["dimensions"] is not None
    
    # Check files were created
    images_dir = temp_output_dir / "images"
    assert images_dir.exists()
    assert (images_dir / "page_001.webp").exists()
    assert (images_dir / "page_002.webp").exists()
    assert (images_dir / "page_003.webp").exists()
    
    # Check fallback images
    fallback_dir = images_dir / "fallback"
    assert fallback_dir.exists()
    assert (fallback_dir / "page_001.jpg").exists()


def test_convert_pdf_custom_dpi(sample_pdf, temp_output_dir):
    """Test converting PDF with custom DPI."""
    config = Config(dpi=200)
    converter = PDFConverter(config)
    metadata = converter.convert_to_images(sample_pdf, temp_output_dir)
    
    assert metadata["dpi"] == 200
    # Higher DPI should result in larger images
    assert metadata["total_size_bytes"] > 0


def test_convert_nonexistent_pdf(temp_output_dir, default_config):
    """Test error handling for non-existent PDF."""
    converter = PDFConverter(default_config)
    fake_pdf = Path("nonexistent.pdf")
    
    with pytest.raises(FileNotFoundError):
        converter.convert_to_images(fake_pdf, temp_output_dir)


def test_get_pdf_info(sample_pdf):
    """Test getting PDF information."""
    converter = PDFConverter()
    info = converter.get_pdf_info(sample_pdf)
    
    assert info["page_count"] == 3
    assert info["dimensions"] == (595, 842)
    assert "title" in info
    assert "author" in info


def test_get_pdf_info_nonexistent():
    """Test error handling for non-existent PDF info."""
    converter = PDFConverter()
    fake_pdf = Path("nonexistent.pdf")
    
    with pytest.raises(FileNotFoundError):
        converter.get_pdf_info(fake_pdf)


def test_convert_creates_output_directory(sample_pdf, tmp_path):
    """Test that converter creates output directory if it doesn't exist."""
    output_dir = tmp_path / "new_output"
    assert not output_dir.exists()
    
    converter = PDFConverter()
    converter.convert_to_images(sample_pdf, output_dir)
    
    assert output_dir.exists()
    assert (output_dir / "images").exists()


def test_metadata_accuracy(sample_pdf, temp_output_dir):
    """Test that metadata accurately reflects conversion results."""
    converter = PDFConverter()
    metadata = converter.convert_to_images(sample_pdf, temp_output_dir)
    
    # Count actual files
    images_dir = temp_output_dir / "images"
    webp_files = list(images_dir.glob("*.webp"))
    
    assert len(webp_files) == metadata["page_count"]
    assert metadata["total_size_bytes"] > 0
    assert metadata["average_page_size_kb"] > 0
