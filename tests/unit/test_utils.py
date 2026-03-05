"""Unit tests for image utilities."""

import random
import pytest
from pathlib import Path
from PIL import Image

from pdf_flipbook_animator.utils.image import (
    convert_to_webp,
    create_jpg_fallback,
    resize_image,
)


def test_convert_to_webp(sample_image, tmp_path):
    """Test converting image to WebP format."""
    img = Image.open(sample_image)
    output_path = tmp_path / "output.webp"
    
    file_size = convert_to_webp(img, output_path, quality=85)
    
    assert output_path.exists()
    assert file_size > 0
    assert output_path.suffix == ".webp"


def test_convert_to_webp_quality(tmp_path):
    """Test WebP conversion with different quality settings."""
    random.seed(42)
    # Use an image with varied pixel data so quality level meaningfully affects file size
    pixels = bytes([random.randint(0, 255) for _ in range(800 * 600 * 3)])
    img = Image.frombytes("RGB", (800, 600), pixels)

    high_quality_path = tmp_path / "high.webp"
    low_quality_path = tmp_path / "low.webp"

    high_size = convert_to_webp(img, high_quality_path, quality=95)
    low_size = convert_to_webp(img, low_quality_path, quality=50)

    # Higher quality should result in larger file
    assert high_size > low_size


def test_create_jpg_fallback(sample_image, tmp_path):
    """Test creating JPG fallback image."""
    img = Image.open(sample_image)
    output_path = tmp_path / "output.jpg"
    
    file_size = create_jpg_fallback(img, output_path, quality=90)
    
    assert output_path.exists()
    assert file_size > 0
    assert output_path.suffix in [".jpg", ".jpeg"]


def test_create_jpg_from_rgba(tmp_path):
    """Test JPG creation from RGBA image."""
    # Create RGBA image
    img = Image.new("RGBA", (800, 600), color=(255, 0, 0, 128))
    output_path = tmp_path / "output.jpg"
    
    file_size = create_jpg_fallback(img, output_path)
    
    assert output_path.exists()
    # JPG should not have alpha channel
    saved_img = Image.open(output_path)
    assert saved_img.mode == "RGB"


def test_resize_image_downscale():
    """Test resizing image to smaller dimensions."""
    img = Image.new("RGB", (1000, 800), color=(100, 150, 200))
    
    resized = resize_image(img, max_width=500, max_height=400)
    
    assert resized.width <= 500
    assert resized.height <= 400
    # Aspect ratio should be maintained
    assert abs((resized.width / resized.height) - (1000 / 800)) < 0.01


def test_resize_image_no_upscale():
    """Test that resize doesn't upscale small images."""
    img = Image.new("RGB", (400, 300), color=(100, 150, 200))
    
    resized = resize_image(img, max_width=1000, max_height=800)
    
    # Should not upscale
    assert resized.width == 400
    assert resized.height == 300


def test_resize_image_aspect_ratio():
    """Test that resize maintains aspect ratio."""
    img = Image.new("RGB", (1600, 900), color=(100, 150, 200))
    
    resized = resize_image(img, max_width=800, max_height=800)
    
    original_ratio = 1600 / 900
    resized_ratio = resized.width / resized.height
    
    assert abs(original_ratio - resized_ratio) < 0.01


def test_webp_file_is_valid(sample_image, tmp_path):
    """Test that created WebP file is valid and can be reopened."""
    img = Image.open(sample_image)
    output_path = tmp_path / "test.webp"
    
    convert_to_webp(img, output_path)
    
    # Try to open the created WebP file
    reopened = Image.open(output_path)
    assert reopened.format == "WEBP"
    assert reopened.size == img.size


def test_jpg_file_is_valid(sample_image, tmp_path):
    """Test that created JPG file is valid and can be reopened."""
    img = Image.open(sample_image)
    output_path = tmp_path / "test.jpg"
    
    create_jpg_fallback(img, output_path)
    
    # Try to open the created JPG file
    reopened = Image.open(output_path)
    assert reopened.format == "JPEG"
    assert reopened.size == img.size
