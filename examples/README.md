# Examples

This directory contains example PDFs for testing PDF Flipbook Animator.

## Sample PDF

The `January_2026_patrabhet.pdf` file is a sample document you can use to test the flipbook generator.

## Quick Test

Try converting the sample:

```bash
pdf-flipbook convert examples/January_2026_patrabhet.pdf
```

The output will be created in `output/January_2026_patrabhet/`.

## Creating Your Own Examples

To add your own example PDFs:

1. Place PDF files in this directory
2. Convert them:
   ```bash
   pdf-flipbook batch examples/
   ```

## Example Commands

### Basic Conversion
```bash
pdf-flipbook convert examples/January_2026_patrabhet.pdf
```

### High Quality
```bash
pdf-flipbook convert examples/January_2026_patrabhet.pdf \
    --dpi 200 \
    --quality 95 \
    --title "January 2026 Edition"
```

### Custom Styling
```bash
pdf-flipbook convert examples/January_2026_patrabhet.pdf \
    --primary-color "#E91E63" \
    --title "Sample Magazine"
```

## View Examples

After conversion, open the generated flipbooks:

- Single PDF: `output/January_2026_patrabhet/index.html`
- All examples: `output/*/index.html`

## Notes

- Keep example PDFs under 10 MB for repository size
- Only include copyright-free or self-created PDFs
- Document any special features or characteristics of example PDFs
