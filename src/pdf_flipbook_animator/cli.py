"""Command-line interface for PDF Flipbook Animator."""

import logging
import sys
from pathlib import Path
from typing import Optional

import click

from pdf_flipbook_animator import __version__
from pdf_flipbook_animator.config import Config
from pdf_flipbook_animator.core.converter import PDFConverter
from pdf_flipbook_animator.core.generator import FlipbookGenerator

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


@click.group()
@click.version_option(version=__version__, prog_name="pdf-flipbook")
@click.option(
    "--verbose", "-v", is_flag=True, help="Enable verbose output"
)
@click.option(
    "--quiet", "-q", is_flag=True, help="Suppress non-error output"
)
def cli(verbose: bool, quiet: bool):
    """PDF Flipbook Animator - Convert PDFs to animated flipbook web pages.

    \b
    Examples:
        pdf-flipbook convert input.pdf
        pdf-flipbook convert input.pdf --output-dir ./my-flipbook
        pdf-flipbook convert input.pdf --dpi 200 --quality 90
        pdf-flipbook batch ./pdfs/
        pdf-flipbook info input.pdf
    """
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    elif quiet:
        logging.getLogger().setLevel(logging.ERROR)


@cli.command()
@click.argument(
    "pdf_path",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(path_type=Path),
    help="Output directory (default: ./output/<pdf-name>)",
)
@click.option(
    "--dpi",
    type=click.IntRange(72, 600),
    default=150,
    help="Image resolution in DPI (default: 150)",
)
@click.option(
    "--quality",
    type=click.IntRange(1, 100),
    default=85,
    help="WebP quality 1-100 (default: 85)",
)
@click.option(
    "--jpg-quality",
    type=click.IntRange(1, 100),
    default=90,
    help="JPG fallback quality 1-100 (default: 90)",
)
@click.option(
    "--title",
    type=str,
    help="Flipbook title (default: PDF filename)",
)
@click.option(
    "--single-page",
    is_flag=True,
    help="Single page mode instead of double-page spread",
)
@click.option(
    "--no-fullscreen",
    is_flag=True,
    help="Disable fullscreen button",
)
@click.option(
    "--primary-color",
    type=str,
    default="#2196F3",
    help="Primary color for UI (default: #2196F3)",
)
@click.option(
    "--animation-mode",
    "-a",
    type=click.Choice(["simple", "3d-css", "realistic"]),
    default="simple",
    help="Page flip animation style (default: simple)",
)
@click.option(
    "--flip-duration",
    type=click.IntRange(200, 2000),
    default=800,
    help="Animation duration in milliseconds (default: 800)",
)
@click.option(
    "--enable-curl",
    is_flag=True,
    help="Enable 3D page curl effect (realistic mode only)",
)
def convert(
    pdf_path: Path,
    output_dir: Optional[Path],
    dpi: int,
    quality: int,
    jpg_quality: int,
    title: Optional[str],
    single_page: bool,
    no_fullscreen: bool,
    primary_color: str,
    animation_mode: str,
    flip_duration: int,
    enable_curl: bool,
):
    """Convert a PDF to an animated flipbook.

    Converts PDF_PATH to a web-ready flipbook animation with HTML viewer.
    The output is a self-contained folder that can be hosted on any web server.

    \b
    Examples:
        pdf-flipbook convert book.pdf
        pdf-flipbook convert book.pdf -o ./my-flipbook --dpi 200
        pdf-flipbook convert book.pdf --title "My Book" --primary-color "#FF5722"
        pdf-flipbook convert book.pdf --animation-mode realistic
        pdf-flipbook convert book.pdf -a 3d-css --flip-duration 1000
    """
    try:
        # Setup paths
        if output_dir is None:
            output_dir = Path("output") / pdf_path.stem
        output_dir = output_dir.resolve()

        # Setup title
        if title is None:
            title = pdf_path.stem.replace("_", " ").replace("-", " ").title()

        # Create configuration
        config = Config(
            dpi=dpi,
            quality=quality,
            jpg_quality=jpg_quality,
            title=title,
            single_page_mode=single_page,
            enable_fullscreen=not no_fullscreen,
            primary_color=primary_color,
            animation_mode=animation_mode,
            page_flip_duration=flip_duration,
            enable_page_curl=enable_curl,
            output_dir=output_dir,
        )

        click.echo(f"\n📄 Converting PDF: {click.style(pdf_path.name, fg='cyan', bold=True)}")
        click.echo(f"📁 Output directory: {click.style(str(output_dir), fg='cyan')}")
        click.echo(f"⚙️  Settings: DPI={dpi}, Quality={quality}, Animation={animation_mode}\n")

        # Step 1: Convert PDF to images
        click.echo("🔄 Step 1/2: Converting PDF pages to images...")
        converter = PDFConverter(config)
        metadata = converter.convert_to_images(pdf_path, output_dir)

        click.echo(
            f"✅ Converted {click.style(str(metadata['page_count']), fg='green', bold=True)} pages "
            f"({metadata['total_size_mb']} MB total)\n"
        )

        # Step 2: Generate HTML flipbook
        click.echo("🔄 Step 2/2: Generating flipbook viewer...")
        generator = FlipbookGenerator(config)
        html_path = generator.generate(
            output_dir / "images",
            output_dir,
            metadata,
            title,
        )

        click.echo(f"✅ Generated HTML viewer\n")

        # Success message
        click.echo(
            click.style("🎉 Success!", fg="green", bold=True)
            + f" Flipbook created at: {click.style(str(output_dir), fg='cyan', bold=True)}"
        )
        click.echo(f"\n📖 Open in browser: {click.style(str(html_path), fg='blue', underline=True)}")
        click.echo(
            f"🌐 To preview locally: cd {output_dir.name} && python -m http.server 8000\n"
        )

    except Exception as e:
        click.echo(click.style(f"\n❌ Error: {str(e)}", fg="red", bold=True), err=True)
        logger.exception("Conversion failed")
        sys.exit(1)


@cli.command()
@click.argument(
    "directory",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
)
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(path_type=Path),
    default=Path("output"),
    help="Base output directory (default: ./output)",
)
@click.option(
    "--pattern",
    type=str,
    default="*.pdf",
    help="File pattern to match (default: *.pdf)",
)
@click.option(
    "--dpi",
    type=click.IntRange(72, 600),
    default=150,
    help="Image resolution in DPI (default: 150)",
)
@click.option(
    "--quality",
    type=click.IntRange(1, 100),
    default=85,
    help="WebP quality 1-100 (default: 85)",
)
def batch(
    directory: Path,
    output_dir: Path,
    pattern: str,
    dpi: int,
    quality: int,
):
    """Batch convert multiple PDFs in a directory.

    Processes all PDF files matching PATTERN in DIRECTORY.
    Each PDF is converted to a separate flipbook in OUTPUT_DIR.

    \b
    Examples:
        pdf-flipbook batch ./pdfs/
        pdf-flipbook batch ./pdfs/ --pattern "chapter*.pdf"
        pdf-flipbook batch ./books/ -o ./flipbooks/ --dpi 200
    """
    try:
        pdf_files = list(directory.glob(pattern))

        if not pdf_files:
            click.echo(
                click.style(
                    f"No PDF files found matching '{pattern}' in {directory}",
                    fg="yellow",
                ),
                err=True,
            )
            sys.exit(1)

        click.echo(
            f"\n📚 Found {click.style(str(len(pdf_files)), fg='cyan', bold=True)} "
            f"PDF file(s) to convert\n"
        )

        output_dir = output_dir.resolve()
        output_dir.mkdir(parents=True, exist_ok=True)

        success_count = 0
        fail_count = 0

        for i, pdf_path in enumerate(pdf_files, 1):
            click.echo(
                f"\n{'='*60}\n"
                f"Processing {i}/{len(pdf_files)}: {click.style(pdf_path.name, fg='cyan', bold=True)}\n"
                f"{'='*60}"
            )

            try:
                pdf_output_dir = output_dir / pdf_path.stem
                title = pdf_path.stem.replace("_", " ").replace("-", " ").title()

                config = Config(
                    dpi=dpi,
                    quality=quality,
                    title=title,
                    output_dir=pdf_output_dir,
                )

                # Convert PDF
                converter = PDFConverter(config)
                metadata = converter.convert_to_images(pdf_path, pdf_output_dir)

                # Generate flipbook
                generator = FlipbookGenerator(config)
                generator.generate(
                    pdf_output_dir / "images",
                    pdf_output_dir,
                    metadata,
                    title,
                )

                click.echo(click.style(f"✅ Success: {pdf_path.name}", fg="green"))
                success_count += 1

            except Exception as e:
                click.echo(
                    click.style(f"❌ Failed: {pdf_path.name} - {str(e)}", fg="red"),
                    err=True,
                )
                logger.exception(f"Failed to convert {pdf_path}")
                fail_count += 1

        # Summary
        click.echo(f"\n{'='*60}")
        click.echo(click.style("Batch Conversion Complete!", fg="green", bold=True))
        click.echo(f"✅ Successful: {click.style(str(success_count), fg='green', bold=True)}")
        if fail_count > 0:
            click.echo(f"❌ Failed: {click.style(str(fail_count), fg='red', bold=True)}")
        click.echo(f"📁 Output directory: {click.style(str(output_dir), fg='cyan')}")
        click.echo(f"{'='*60}\n")

    except Exception as e:
        click.echo(click.style(f"\n❌ Error: {str(e)}", fg="red", bold=True), err=True)
        logger.exception("Batch conversion failed")
        sys.exit(1)


@cli.command()
@click.argument(
    "pdf_path",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
def info(pdf_path: Path):
    """Display information about a PDF file.

    Shows page count, dimensions, and metadata for PDF_PATH.

    \b
    Example:
        pdf-flipbook info document.pdf
    """
    try:
        converter = PDFConverter()
        pdf_info = converter.get_pdf_info(pdf_path)

        click.echo(f"\n📄 PDF Information: {click.style(pdf_path.name, fg='cyan', bold=True)}\n")
        click.echo(f"  Pages: {click.style(str(pdf_info['page_count']), fg='green', bold=True)}")
        click.echo(
            f"  Dimensions: {pdf_info['dimensions'][0]} × {pdf_info['dimensions'][1]} pt"
        )

        if pdf_info.get("title"):
            click.echo(f"  Title: {pdf_info['title']}")
        if pdf_info.get("author"):
            click.echo(f"  Author: {pdf_info['author']}")
        if pdf_info.get("subject"):
            click.echo(f"  Subject: {pdf_info['subject']}")

        # Estimate output size
        estimated_size = pdf_info["page_count"] * 0.5  # Rough estimate: 500KB per page
        click.echo(f"\n  Estimated output size: ~{estimated_size:.1f} MB\n")

    except Exception as e:
        click.echo(click.style(f"\n❌ Error: {str(e)}", fg="red", bold=True), err=True)
        sys.exit(1)


def main():
    """Entry point for CLI."""
    cli()


if __name__ == "__main__":
    main()
