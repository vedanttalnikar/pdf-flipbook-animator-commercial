"""Unit tests for configuration."""

import pytest
from pdf_flipbook_animator.config import Config


def test_default_config():
    """Test default configuration values."""
    config = Config()
    
    assert config.dpi == 150
    assert config.quality == 85
    assert config.jpg_quality == 90
    assert config.title == "Flipbook"
    assert config.enable_fullscreen is True
    assert config.lazy_load is True


def test_custom_config():
    """Test custom configuration values."""
    config = Config(
        dpi=200,
        quality=90,
        title="My Book",
        primary_color="#FF0000"
    )
    
    assert config.dpi == 200
    assert config.quality == 90
    assert config.title == "My Book"
    assert config.primary_color == "#FF0000"


def test_config_validation_dpi_too_low():
    """Test that DPI below 72 raises error."""
    with pytest.raises(ValueError, match="DPI must be at least 72"):
        Config(dpi=50)


def test_config_validation_dpi_too_high():
    """Test that DPI above 600 raises error."""
    with pytest.raises(ValueError, match="DPI should not exceed 600"):
        Config(dpi=1000)


def test_config_validation_quality():
    """Test quality validation."""
    with pytest.raises(ValueError, match="Quality must be between 1 and 100"):
        Config(quality=0)
    
    with pytest.raises(ValueError, match="Quality must be between 1 and 100"):
        Config(quality=101)


def test_config_validation_jpg_quality():
    """Test JPG quality validation."""
    with pytest.raises(ValueError, match="JPG quality must be between 1 and 100"):
        Config(jpg_quality=0)
    
    with pytest.raises(ValueError, match="JPG quality must be between 1 and 100"):
        Config(jpg_quality=150)


def test_config_validation_preload_pages():
    """Test preload pages validation."""
    with pytest.raises(ValueError, match="Preload pages must be non-negative"):
        Config(preload_pages=-1)


def test_config_valid_edge_cases():
    """Test that edge case values are accepted."""
    # Should not raise
    config1 = Config(dpi=72, quality=1, jpg_quality=100)
    assert config1.dpi == 72
    
    config2 = Config(dpi=600, quality=100, preload_pages=0)
    assert config2.dpi == 600
