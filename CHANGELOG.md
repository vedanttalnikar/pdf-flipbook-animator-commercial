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
- **Touch/swipe gesture support for mobile devices**
- **Mobile device testing suite and documentation**
- **Interactive mobile device tester HTML page**
- **Comprehensive mobile compatibility testing (MOBILE_TESTING.md)**
- **`--preserve-links` flag** - Preserves clickable PDF links (internal navigation LINK_GOTO and external URLs LINK_URI)
- **`--enable-toc` flag** - Extracts PDF bookmarks into a searchable Table of Contents sidebar
- **Collapsible TOC hierarchy** - H1 headings visually distinct with expand/collapse toggle for child H2/H3/H4 entries
- **TOC search** - Filter TOC entries with real-time search, auto-expand/collapse aware
- **TOC "Index" label** - Button shows "📋 Index" text alongside icon with responsive sizing
- **Active TOC highlighting** - Current page highlighted in sidebar, auto-expands parent H1 group
- **Zoom & pan** - Scroll-wheel zoom with click-and-drag panning across all animation modes
- **Cursor states** - Context-aware cursors (grab, zoom-in, zoom-out, pointer for links)
- **HTML mode** - Uses DOM elements instead of canvas for perfect text quality
- **Device pixel ratio support** - 2-3x sharper rendering on Retina/4K displays
- **Lossless WebP** - Zero compression artifacts for text-heavy documents
- **Jump-to-index button** - Quick access button with configurable target page
- **Windows executable** - Standalone .exe via PyInstaller, no Python required

### Changed
- Updated generator to support multiple JavaScript templates
- Enhanced CLI with animation-related options
- Improved flipbook viewer with mode-specific behaviors
- **Enhanced simple mode with touch/swipe navigation**
- **Enhanced 3D CSS mode with touch/swipe navigation**
- **Optimized performance for mobile devices**
- **Improved responsive CSS for tablets and phones**
- **Default DPI increased to 250** for better clarity
- **Lossless WebP enabled by default**
- **Side panel layout** - Maximizes vertical space (~99vh for PDF viewing)
- **Fully responsive breakpoints** - Desktop (≥1024px), Tablet (768-1023px), Mobile (<768px)
- **Mobile toolbar** - Compact layout with proper spacing at all breakpoints
- **Fullscreen mode** - Fixed duplicate event handlers on reinitialize, proper stacking context

### Fixed
- **Page skip bug** - nextPage/previousPage now uses flipNext()/flipPrev() for spread-aware navigation
- **Fullscreen page skip** - Fixed duplicate event handlers on reinitialize
- **Mobile layout overflow** - Rewrote mobile CSS for compact toolbar
- **TOC mobile click** - Fixed click handler race condition on mobile
- **goToPage fullscreen** - Fixed race condition in fullscreen goToPage
- **TOC fullscreen stacking** - Fixed z-index stacking context in fullscreen mode

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

[Unreleased]: https://github.com/vedanttalnikar/pdf-flipbook-animator-commercial/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/vedanttalnikar/pdf-flipbook-animator-commercial/releases/tag/v0.1.0
