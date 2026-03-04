# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Three animation modes: simple, 3d-css, and realistic
- 3D CSS page folding effect with CSS transforms
- Realistic page curl animation using StPageFlip library
- `--animation-mode` CLI flag to select animation style
- `--flip-duration` CLI flag to customize animation timing
- `--enable-curl` CLI flag for enhanced page curl effect
- JavaScript template system for different animation modes
- Animation configuration options in Config class
- Documentation for animation modes in README
- Feature specification document (FEATURE_REALISTIC_ANIMATION.md)

### Changed
- Updated generator to support multiple JavaScript templates
- Enhanced CLI with animation-related options
- Improved flipbook viewer with mode-specific behaviors

## [0.1.0] - 2026-03-04

### Added
- Initial release
- PDF page extraction and conversion to images
- WebP format with JPG fallback
- Simple flip transition animations
- Manual navigation with keyboard and mouse
- Responsive design for mobile and desktop
- Static site generation for easy hosting
- CLI tool: `pdf-flipbook convert`
- Batch processing support
- Customizable output options (DPI, quality, title)
- Complete documentation
- Example PDFs and outputs

[Unreleased]: https://github.com/yourusername/pdf-flipbook-animator/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yourusername/pdf-flipbook-animator/releases/tag/v0.1.0
