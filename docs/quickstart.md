# Quick Start

Get started with PDF Flipbook Animator in under 5 minutes!

## Step 1: Install

```bash
pip install pdf-flipbook-animator
```

## Step 2: Convert Your First PDF

```bash
pdf-flipbook convert your-document.pdf
```

That's it! The flipbook is created in `output/your-document/`.

## Step 3: View Your Flipbook

Open the generated flipbook in your browser:

=== "macOS"
    ```bash
    open output/your-document/index.html
    ```

=== "Linux"
    ```bash
    xdg-open output/your-document/index.html
    ```

=== "Windows"
    ```bash
    start output/your-document/index.html
    ```

Or use Python's built-in web server:

```bash
cd output/your-document
python -m http.server 8000
```

Then visit [http://localhost:8000](http://localhost:8000)

## Navigation

Use these controls in your flipbook:

- **← →** Arrow keys: Previous/Next page
- **Page Up/Down**: Navigate pages
- **Home/End**: First/Last page
- **F**: Toggle fullscreen
- **Click**: Page buttons or directly on pages
- **Touch**: Swipe on mobile devices

## Common Options

### Custom Title

```bash
pdf-flipbook convert book.pdf --title "My Amazing Book"
```

### Higher Quality

```bash
pdf-flipbook convert book.pdf --dpi 200 --quality 95
```

### Custom Output Location

```bash
pdf-flipbook convert book.pdf --output-dir ./my-website/flipbook
```

### Custom Colors

```bash
pdf-flipbook convert book.pdf --primary-color "#FF5722"
```

## Example with All Options

```bash
pdf-flipbook convert book.pdf \
    --output-dir ./my-flipbook \
    --dpi 200 \
    --quality 90 \
    --title "My Digital Magazine" \
    --primary-color "#9C27B0" \
    --single-page
```

## Check PDF Information

Before converting, check what you're working with:

```bash
pdf-flipbook info document.pdf
```

Output:
```
📄 PDF Information: document.pdf

  Pages: 24
  Dimensions: 595 × 842 pt
  Title: Sample Document
  Author: John Doe

  Estimated output size: ~12.0 MB
```

## Batch Conversion

Convert multiple PDFs at once:

```bash
pdf-flipbook batch ./my-pdfs-folder/
```

Or with a pattern:

```bash
pdf-flipbook batch ./pdfs/ --pattern "chapter*.pdf"
```

## Hosting Your Flipbook

Once generated, your flipbook is a static website. You can:

1. **Upload to any web host** (GitHub Pages, Netlify, Vercel, etc.)
2. **Share the folder** directly
3. **Embed in existing websites**

Example with GitHub Pages:

```bash
cd output/your-document
git init
git add .
git commit -m "Add flipbook"
git branch -M main
git remote add origin https://github.com/yourusername/my-flipbook.git
git push -u origin main
```

Then enable GitHub Pages in your repository settings!

## What's Next?

- Learn about [Advanced Options](usage/advanced.md)
- Explore [Hosting Options](usage/hosting.md)
- See [Examples](examples/gallery.md)

## Quick Reference

| Command | Description |
|---------|-------------|
| `pdf-flipbook convert FILE` | Convert a PDF |
| `pdf-flipbook batch DIR` | Convert multiple PDFs |
| `pdf-flipbook info FILE` | Show PDF information |
| `pdf-flipbook --help` | Show all commands |

## Tips

!!! tip "Optimize for Web"
    Use 150 DPI for web viewing - higher values create larger files with minimal visual improvement.

!!! tip "Test Locally First"
    Always preview your flipbook locally before deploying to ensure everything looks right.

!!! tip "Mobile Preview"
    Test on mobile devices or use browser dev tools to check responsive layout.
