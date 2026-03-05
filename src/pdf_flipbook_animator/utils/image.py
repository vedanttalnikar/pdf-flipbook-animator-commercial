"""Image processing utilities."""

import logging
from pathlib import Path
from typing import Optional

from PIL import Image

logger = logging.getLogger(__name__)


def convert_to_webp(
    image: Image.Image, output_path: Path, quality: int = 85, lossless: bool = False
) -> int:
    """Convert PIL Image to WebP format.

    Args:
        image: PIL Image object
        output_path: Path to save WebP file
        quality: WebP quality (1-100, ignored if lossless=True)
        lossless: Use lossless compression (better for text/diagrams)

    Returns:
        File size in bytes
    """
    try:
        save_params = {
            "format": "WEBP",
            "lossless": lossless,
        }
        
        if not lossless:
            # Lossy mode: use quality and method settings
            save_params["quality"] = quality
            save_params["method"] = 6  # Best compression
        
        image.save(output_path, **save_params)
        file_size = output_path.stat().st_size
        mode_str = "lossless" if lossless else f"quality {quality}"
        logger.debug(f"Saved WebP ({mode_str}): {output_path.name} ({file_size // 1024} KB)")
        return file_size
    except Exception as e:
        logger.error(f"Failed to save WebP {output_path}: {e}")
        raise


def create_jpg_fallback(
    image: Image.Image, output_path: Path, quality: int = 90
) -> int:
    """Create JPG fallback image for older browsers.

    Args:
        image: PIL Image object
        output_path: Path to save JPG file
        quality: JPG quality (1-100)

    Returns:
        File size in bytes
    """
    try:
        # Convert RGBA to RGB if necessary
        if image.mode in ("RGBA", "LA", "P"):
            background = Image.new("RGB", image.size, (255, 255, 255))
            if image.mode == "P":
                image = image.convert("RGBA")
            background.paste(image, mask=image.split()[-1] if image.mode == "RGBA" else None)
            image = background

        image.save(output_path, "JPEG", quality=quality, optimize=True)
        file_size = output_path.stat().st_size
        logger.debug(f"Saved JPG fallback: {output_path.name} ({file_size // 1024} KB)")
        return file_size
    except Exception as e:
        logger.error(f"Failed to save JPG {output_path}: {e}")
        raise


def optimize_image(
    image_path: Path, quality: Optional[int] = None
) -> int:
    """Optimize an existing image file.

    Args:
        image_path: Path to image file
        quality: Optional quality setting (format-dependent)

    Returns:
        New file size in bytes
    """
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    img = Image.open(image_path)
    original_size = image_path.stat().st_size

    # Determine format and optimize
    fmt = img.format or image_path.suffix[1:].upper()

    if fmt == "WEBP":
        quality = quality or 85
        img.save(image_path, "WEBP", quality=quality, method=6)
    elif fmt in ("JPEG", "JPG"):
        quality = quality or 90
        img.save(image_path, "JPEG", quality=quality, optimize=True)
    elif fmt == "PNG":
        img.save(image_path, "PNG", optimize=True)

    new_size = image_path.stat().st_size
    savings = original_size - new_size

    logger.info(
        f"Optimized {image_path.name}: "
        f"{original_size // 1024} KB → {new_size // 1024} KB "
        f"(saved {savings // 1024} KB)"
    )

    return new_size


def resize_image(
    image: Image.Image, max_width: int, max_height: int
) -> Image.Image:
    """Resize image while maintaining aspect ratio.

    Args:
        image: PIL Image object
        max_width: Maximum width
        max_height: Maximum height

    Returns:
        Resized PIL Image
    """
    # Calculate scaling factor
    width_ratio = max_width / image.width
    height_ratio = max_height / image.height
    scale = min(width_ratio, height_ratio, 1.0)  # Don't upscale

    if scale < 1.0:
        new_width = int(image.width * scale)
        new_height = int(image.height * scale)
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        logger.debug(f"Resized image to {new_width}x{new_height}")

    return image
