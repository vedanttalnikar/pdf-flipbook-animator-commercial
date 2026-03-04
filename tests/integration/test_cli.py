"""Integration tests for CLI commands."""

import pytest
from pathlib import Path
from click.testing import CliRunner

from pdf_flipbook_animator.cli import cli


@pytest.fixture
def runner():
    """Create a Click CLI test runner."""
    return CliRunner()


def test_cli_version(runner):
    """Test --version flag."""
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "version" in result.output.lower() or "0.1.0" in result.output


def test_cli_help(runner):
    """Test --help flag."""
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "PDF Flipbook Animator" in result.output
    assert "convert" in result.output
    assert "batch" in result.output
    assert "info" in result.output


def test_convert_command_help(runner):
    """Test convert command help."""
    result = runner.invoke(cli, ["convert", "--help"])
    assert result.exit_code == 0
    assert "Convert a PDF" in result.output
    assert "--dpi" in result.output
    assert "--quality" in result.output


def test_convert_basic(runner, sample_pdf, tmp_path):
    """Test basic convert command."""
    output_dir = tmp_path / "output"
    
    result = runner.invoke(cli, [
        "convert",
        str(sample_pdf),
        "--output-dir", str(output_dir)
    ])
    
    # Check command completed
    assert result.exit_code == 0
    assert "Success" in result.output or "✅" in result.output
    
    # Check output files exist
    assert output_dir.exists()
    assert (output_dir / "index.html").exists()
    assert (output_dir / "css" / "style.css").exists()
    assert (output_dir / "js" / "flipbook.js").exists()
    assert (output_dir / "images").exists()


def test_convert_with_options(runner, sample_pdf, tmp_path):
    """Test convert command with custom options."""
    output_dir = tmp_path / "custom_output"
    
    result = runner.invoke(cli, [
        "convert",
        str(sample_pdf),
        "--output-dir", str(output_dir),
        "--dpi", "200",
        "--quality", "90",
        "--title", "Test Book",
        "--primary-color", "#FF5722"
    ])
    
    assert result.exit_code == 0
    assert output_dir.exists()
    
    # Check title in HTML
    html_content = (output_dir / "index.html").read_text()
    assert "Test Book" in html_content


def test_convert_nonexistent_pdf(runner):
    """Test convert with non-existent PDF."""
    result = runner.invoke(cli, [
        "convert",
        "nonexistent.pdf"
    ])
    
    assert result.exit_code != 0
    assert "Error" in result.output or "not found" in result.output.lower()


def test_info_command(runner, sample_pdf):
    """Test info command."""
    result = runner.invoke(cli, ["info", str(sample_pdf)])
    
    assert result.exit_code == 0
    assert "Pages:" in result.output or "pages" in result.output.lower()
    assert "3" in result.output  # Our sample PDF has 3 pages


def test_info_nonexistent_pdf(runner):
    """Test info with non-existent PDF."""
    result = runner.invoke(cli, ["info", "nonexistent.pdf"])
    
    assert result.exit_code != 0


def test_batch_command_help(runner):
    """Test batch command help."""
    result = runner.invoke(cli, ["batch", "--help"])
    assert result.exit_code == 0
    assert "Batch convert" in result.output
    assert "--pattern" in result.output


def test_batch_command(runner, tmp_path):
    """Test batch conversion of multiple PDFs."""
    # Create multiple test PDFs
    pdf_dir = tmp_path / "pdfs"
    pdf_dir.mkdir()
    
    import fitz
    for i in range(2):
        pdf_path = pdf_dir / f"test{i + 1}.pdf"
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((50, 50), f"Test PDF {i + 1}")
        doc.save(pdf_path)
        doc.close()
    
    output_dir = tmp_path / "outputs"
    
    result = runner.invoke(cli, [
        "batch",
        str(pdf_dir),
        "--output-dir", str(output_dir)
    ])
    
    assert result.exit_code == 0
    assert output_dir.exists()
    # Should have converted both PDFs
    assert (output_dir / "test1").exists()
    assert (output_dir / "test2").exists()


def test_verbose_flag(runner, sample_pdf, tmp_path):
    """Test --verbose flag."""
    result = runner.invoke(cli, [
        "--verbose",
        "convert",
        str(sample_pdf),
        "--output-dir", str(tmp_path / "output")
    ])
    
    # Verbose mode should produce output
    assert len(result.output) > 0


def test_quiet_flag(runner, sample_pdf, tmp_path):
    """Test --quiet flag."""
    result = runner.invoke(cli, [
        "--quiet",
        "info",
        str(sample_pdf)
    ])
    
    # In quiet mode, should have minimal output (only errors or required info)
    assert result.exit_code == 0
