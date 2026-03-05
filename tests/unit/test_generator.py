"""Unit tests for flipbook generator."""

import pytest
from pathlib import Path

from pdf_flipbook_animator.core.generator import FlipbookGenerator
from pdf_flipbook_animator.config import Config


def test_generator_initialization():
    """Test FlipbookGenerator initializes correctly."""
    generator = FlipbookGenerator()
    assert generator.config is not None


def test_generator_with_custom_config(custom_config):
    """Test FlipbookGenerator with custom configuration."""
    generator = FlipbookGenerator(custom_config)
    assert generator.config.title == "Test Flipbook"
    assert generator.config.primary_color == "#FF5722"


def test_generate_html(temp_output_dir, mock_metadata):
    """Test HTML generation."""
    generator = FlipbookGenerator()
    
    # Create fake images directory
    images_dir = temp_output_dir / "images"
    images_dir.mkdir()
    
    html_path = generator.generate(
        images_dir,
        temp_output_dir,
        mock_metadata,
        "Test Flipbook"
    )
    
    # Check HTML file exists
    assert html_path.exists()
    assert html_path.name == "index.html"
    
    # Check HTML content
    html_content = html_path.read_text(encoding="utf-8")
    assert "Test Flipbook" in html_content
    assert 'id="total-pages">3' in html_content
    assert "page_001.webp" in html_content or "page_001" in html_content


def test_generate_creates_directories(temp_output_dir, mock_metadata):
    """Test that generator creates required directories."""
    generator = FlipbookGenerator()
    images_dir = temp_output_dir / "images"
    images_dir.mkdir()
    
    generator.generate(images_dir, temp_output_dir, mock_metadata)
    
    assert (temp_output_dir / "css").exists()
    assert (temp_output_dir / "js").exists()


def test_generate_css(temp_output_dir, mock_metadata):
    """Test CSS generation."""
    generator = FlipbookGenerator()
    images_dir = temp_output_dir / "images"
    images_dir.mkdir()
    
    generator.generate(images_dir, temp_output_dir, mock_metadata)
    
    css_path = temp_output_dir / "css" / "style.css"
    assert css_path.exists()
    
    css_content = css_path.read_text(encoding="utf-8")
    assert "--primary-color:" in css_content
    assert "flexbox" in css_content.lower() or "flex" in css_content


def test_generate_js(temp_output_dir, mock_metadata):
    """Test JavaScript generation."""
    generator = FlipbookGenerator()
    images_dir = temp_output_dir / "images"
    images_dir.mkdir()
    
    generator.generate(images_dir, temp_output_dir, mock_metadata)
    
    js_path = temp_output_dir / "js" / "flipbook.js"
    assert js_path.exists()
    
    js_content = js_path.read_text(encoding="utf-8")
    assert "class Flipbook" in js_content
    assert "nextPage" in js_content
    assert "previousPage" in js_content


def test_custom_colors(temp_output_dir, mock_metadata):
    """Test custom color configuration."""
    config = Config(primary_color="#FF5722", background_color="#FAFAFA")
    generator = FlipbookGenerator(config)
    
    images_dir = temp_output_dir / "images"
    images_dir.mkdir()
    
    generator.generate(images_dir, temp_output_dir, mock_metadata)
    
    css_path = temp_output_dir / "css" / "style.css"
    css_content = css_path.read_text(encoding="utf-8")
    
    assert "#FF5722" in css_content
    assert "#FAFAFA" in css_content


def test_fullscreen_option(temp_output_dir, mock_metadata):
    """Test fullscreen button configuration."""
    config_with_fullscreen = Config(enable_fullscreen=True)
    generator_with = FlipbookGenerator(config_with_fullscreen)
    
    images_dir = temp_output_dir / "images"
    images_dir.mkdir()
    
    html_path = generator_with.generate(
        images_dir, temp_output_dir, mock_metadata
    )
    
    html_content = html_path.read_text(encoding="utf-8")
    assert "fullscreen" in html_content.lower()


def test_generated_html_structure(temp_output_dir, mock_metadata):
    """Test that generated HTML has correct structure."""
    generator = FlipbookGenerator()
    images_dir = temp_output_dir / "images"
    images_dir.mkdir()
    
    html_path = generator.generate(images_dir, temp_output_dir, mock_metadata)
    html_content = html_path.read_text(encoding="utf-8")
    
    # Check for essential HTML elements
    assert "<!DOCTYPE html>" in html_content
    assert "<html" in html_content
    assert "<head>" in html_content
    assert "<body>" in html_content
    assert '<div class="page"' in html_content
    assert "css/style.css" in html_content
    assert "js/flipbook.js" in html_content


def test_page_count_in_html(temp_output_dir, mock_metadata):
    """Test that page count is correctly embedded in HTML."""
    generator = FlipbookGenerator()
    images_dir = temp_output_dir / "images"
    images_dir.mkdir()
    
    html_path = generator.generate(images_dir, temp_output_dir, mock_metadata)
    html_content = html_path.read_text(encoding="utf-8")
    
    # Should have 3 pages based on mock_metadata
    assert html_content.count('<div class="page"') == 3
