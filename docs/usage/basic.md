# Basic Usage

This guide covers the essential commands and options for PDF Flipbook Animator.

## Convert Command

The `convert` command transforms a single PDF into an interactive flipbook.

### Basic Syntax

```bash
pdf-flipbook convert <pdf-file> [OPTIONS]
```

### Examples

#### Default Conversion

```bash
pdf-flipbook convert document.pdf
```

Creates output in `./output/document/`

#### Specify Output Directory

```bash
pdf-flipbook convert document.pdf --output-dir ./my-flipbook
```

#### Custom Title

```bash
pdf-flipbook convert document.pdf --title "My Document"
```

The title appears in the browser tab and flipbook header.

## Quality Options

### DPI (Resolution)

Control image resolution with `--dpi`:

```bash
# Lower quality, smaller files (web browsing)
pdf-flipbook convert doc.pdf --dpi 96

# Standard quality (recommended)
pdf-flipbook convert doc.pdf --dpi 150

# High quality (detailed documents)
pdf-flipbook convert doc.pdf --dpi 200

# Print quality (large files!)
pdf-flipbook convert doc.pdf --dpi 300
```

**Recommendations:**
- **96-120 DPI**: Quick preview, small files
- **150 DPI**: Best for most use cases ⭐
- **200-300 DPI**: High-detail documents, large file sizes

### Image Quality

Control WebP compression with `--quality`:

```bash
# Lower quality, smallest files
pdf-flipbook convert doc.pdf --quality 70

# Good balance (default)
pdf-flipbook convert doc.pdf --quality 85

# High quality, larger files
pdf-flipbook convert doc.pdf --quality 95
```

**Quality Scale:**
- **1-60**: Low quality, visible artifacts
- **70-85**: Good balance ⭐
- **90-100**: Minimal compression, large files

### JPG Fallback Quality

For browsers without WebP support:

```bash
pdf-flipbook convert doc.pdf --jpg-quality 90
```

## Appearance Options

### Primary Color

Customize the UI color scheme:

```bash
# Blue (default)
pdf-flipbook convert doc.pdf --primary-color "#2196F3"

# Red
pdf-flipbook convert doc.pdf --primary-color "#F44336"

# Purple
pdf-flipbook convert doc.pdf --primary-color "#9C27B0"

# Custom brand color
pdf-flipbook convert doc.pdf --primary-color "#FF5722"
```

### Single Page Mode

By default, flipbooks show two pages side-by-side on wide screens. Use `--single-page` to show one page at a time:

```bash
pdf-flipbook convert doc.pdf --single-page
```

### Disable Fullscreen

Remove the fullscreen button:

```bash
pdf-flipbook convert doc.pdf --no-fullscreen
```

## Combined Example

Putting it all together:

```bash
pdf-flipbook convert annual-report.pdf \
    --output-dir ./website/reports/2024 \
    --dpi 180 \
    --quality 90 \
    --title "Annual Report 2024" \
    --primary-color "#1976D2" \
    --single-page
```

## Info Command

Get information about a PDF before converting:

```bash
pdf-flipbook info document.pdf
```

**Output:**
```
📄 PDF Information: document.pdf

  Pages: 48
  Dimensions: 595 × 842 pt
  Title: Company Handbook
  Author: HR Department

  Estimated output size: ~24.0 MB
```

This helps you:
- Estimate conversion time
- Plan storage requirements
- Verify the PDF before processing

## Output Structure

Each conversion creates this structure:

```
output/document-name/
├── index.html              # Main viewer
├── css/
│   └── style.css          # Styling
├── js/
│   └── flipbook.js        # Interactivity
└── images/
    ├── page_001.webp      # Page images
    ├── page_002.webp
    ├── ...
    └── fallback/          # Browser fallbacks
        ├── page_001.jpg
        ├── page_002.jpg
        └── ...
```

## Tips & Best Practices

!!! tip "Start with Defaults"
    The default settings (150 DPI, quality 85) work well for most PDFs. Only adjust if needed.

!!! tip "Test Before Publishing"
    Always preview the flipbook locally before deploying to production.

!!! tip "File Size Awareness"
    Monitor `Estimated output size` in the conversion log. Large sizes may require CDN hosting.

!!! warning "Very Large PDFs"
    PDFs with 100+ pages or high-resolution images may take several minutes to convert and create large output files.

## Verbose and Quiet Modes

### Verbose Mode

See detailed conversion progress:

```bash
pdf-flipbook --verbose convert document.pdf
```

Useful for:
- Debugging issues
- Monitoring conversion progress
- Understanding what the tool is doing

### Quiet Mode

Minimal output (errors only):

```bash
pdf-flipbook --quiet convert document.pdf
```

Useful for:
- Automated scripts
- CI/CD pipelines
- Clean logs

## Next Steps

- Learn about [Advanced Options](advanced.md)
- Discover [Batch Processing](batch.md)
- Explore [Hosting Options](hosting.md)
