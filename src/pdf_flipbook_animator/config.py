"""Configuration and settings for PDF Flipbook Animator."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class Config:
    """Configuration for PDF to flipbook conversion."""

    # PDF conversion settings
    dpi: int = 250  # Image resolution (increased default for better text clarity)
    quality: int = 85  # WebP quality (1-100)
    jpg_quality: int = 90  # JPG fallback quality
    output_format: str = "webp"  # Primary image format
    lossless_webp: bool = True  # Use lossless WebP (essential for text quality)

    # Flipbook settings
    title: str = "Flipbook"
    single_page_mode: bool = False  # False = double page spread
    enable_fullscreen: bool = True
    enable_download: bool = True
    show_page_numbers: bool = True
    enable_index_button: bool = True  # Show jump-to-index button
    index_page: int = 2  # Page number for index button (1-based)

    # Performance settings
    lazy_load: bool = True
    preload_pages: int = 2  # Number of pages to preload ahead

    # Styling
    primary_color: str = "#2196F3"
    background_color: str = "#f5f5f5"
    dark_mode: bool = False

    # Animation settings
    animation_mode: str = "simple"  # simple, 3d-css, realistic
    enable_page_curl: bool = False
    page_flip_duration: int = 800  # milliseconds
    flip_easing: str = "ease-in-out"  # CSS easing function
    enable_flip_sound: bool = False

    # Paths
    output_dir: Optional[Path] = None
    template_dir: Optional[Path] = None

    def __post_init__(self):
        """Validate and normalize configuration values."""
        if self.dpi < 72:
            raise ValueError("DPI must be at least 72")
        if self.dpi > 600:
            raise ValueError("DPI should not exceed 600 for web use")

        if not 1 <= self.quality <= 100:
            raise ValueError("Quality must be between 1 and 100")

        if not 1 <= self.jpg_quality <= 100:
            raise ValueError("JPG quality must be between 1 and 100")

        if self.preload_pages < 0:
            raise ValueError("Preload pages must be non-negative")

        # Validate animation settings
        valid_modes = ["simple", "3d-css", "realistic"]
        if self.animation_mode not in valid_modes:
            raise ValueError(f"animation_mode must be one of {valid_modes}")

        if not 200 <= self.page_flip_duration <= 2000:
            raise ValueError("page_flip_duration must be between 200-2000ms")

        if self.index_page < 1:
            raise ValueError("index_page must be at least 1")


# Default configuration
DEFAULT_CONFIG = Config()
