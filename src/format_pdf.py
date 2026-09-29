"""Renders an HTML manuscript + CSS stylesheet into a PDF using WeasyPrint.

Requires: pip install weasyprint
WeasyPrint also needs system libraries (Pango, Cairo, GDK-PixBuf). See
https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation
This step was NOT run in the environment that built this project; test it
on your own machine after installing WeasyPrint and its dependencies.
"""
import sys


def generate_pdf(html_path, css_path, output_pdf_path):
    try:
        from weasyprint import HTML, CSS
    except ImportError:
        sys.exit(
            "WeasyPrint is not installed. Run: pip install weasyprint\n"
            "(It also needs system libraries -- see the docstring in this file.)"
        )
    HTML(html_path).write_pdf(output_pdf_path, stylesheets=[CSS(css_path)])
    print(f"Generated: {output_pdf_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Render HTML+CSS manuscript to PDF.")
    parser.add_argument("html_file")
    parser.add_argument("css_file")
    parser.add_argument("output_pdf")
    args = parser.parse_args()
    generate_pdf(args.html_file, args.css_file, args.output_pdf)
