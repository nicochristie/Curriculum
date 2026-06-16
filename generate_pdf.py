"""
Simple PDF Generator for CV
Converts the HTML CV to PDF using Playwright
"""

import os
import asyncio
import re
import subprocess
from playwright.async_api import async_playwright

MAX_PAGES = 2
SCALE_STEPS = [1.0, 0.97, 0.94, 0.91, 0.88, 0.85]


def get_version_label():
    """Build a small stamp (git short SHA) so a regenerated PDF can be told apart from a previous one."""
    try:
        sha = subprocess.check_output(
            ['git', 'rev-parse', '--short', 'HEAD'], stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        sha = 'dev'
    return f"v{sha}"


def count_pdf_pages(pdf_path):
    """Dependency-free page count: the page-tree root declares /Count N,
    where N is the total number of leaf pages."""
    with open(pdf_path, 'rb') as f:
        data = f.read()
    match = re.search(rb'/Type\s*/Pages.{0,200}?/Count\s+(\d+)', data, re.DOTALL)
    if not match:
        match = re.search(rb'/Count\s+(\d+).{0,200}?/Type\s*/Pages', data, re.DOTALL)
    return int(match.group(1)) if match else None


async def generate_pdf(html_path, pdf_path):
    """Generate PDF from HTML file, shrinking the render scale as needed to
    stay within MAX_PAGES."""
    if not os.path.exists(html_path):
        print(f"Error: HTML file not found at {html_path}")
        return False

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Load the HTML file
        file_url = f'file:///{os.path.abspath(html_path).replace(os.sep, "/")}'
        await page.goto(file_url, wait_until='networkidle')

        # Append a tiny version stamp as the last element so it lands near the
        # bottom of the last page without affecting earlier page breaks.
        await page.evaluate(
            """(label) => {
                const el = document.createElement('div');
                el.textContent = label;
                el.style.textAlign = 'right';
                el.style.fontSize = '6pt';
                el.style.color = '#bbb';
                el.style.marginTop = '6px';
                el.style.marginRight = '10px';
                const container = document.querySelector('.main-content');
                if (container) container.appendChild(el);
            }""",
            get_version_label()
        )

        pdf_kwargs = dict(
            path=pdf_path,
            format='A4',
            print_background=True,
            margin={
                'top': '0mm',
                'right': '0mm',
                'bottom': '0mm',
                'left': '0mm'
            }
        )

        for scale in SCALE_STEPS:
            await page.pdf(scale=scale, **pdf_kwargs)
            pages = count_pdf_pages(pdf_path)
            if pages is not None and pages <= MAX_PAGES:
                if scale != SCALE_STEPS[0]:
                    print(f"  Note: scaled to {scale} to fit within {MAX_PAGES} pages.")
                break
        else:
            print(f"  Warning: still over {MAX_PAGES} pages at minimum scale ({SCALE_STEPS[-1]}).")

        await browser.close()

    return True


async def main():
    files_to_generate = [
        ('docs/index.html', 'docs/pdf/CV Nicolas Christie (en).pdf'),
        ('docs/cover-letter.html', 'docs/pdf/CL Nicolas Christie (en).pdf'),
    ]

    all_success = True
    for html_file, pdf_file in files_to_generate:
        print(f"Generating PDF from {html_file}...")
        success = await generate_pdf(html_file, pdf_file)

        if success:
            print(f"PDF generated successfully: {os.path.abspath(pdf_file)}")
        else:
            print(f"PDF generation failed for {html_file}!")
            all_success = False

    if all_success:
        print("\nAll PDFs generated successfully!")
    else:
        print("\nSome PDF generations failed.")


if __name__ == '__main__':
    asyncio.run(main())
