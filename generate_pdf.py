"""
Simple PDF Generator for CV
Converts the HTML CV to PDF using Playwright
"""

import os
import asyncio
import subprocess
from playwright.async_api import async_playwright


def get_version_label():
    """Build a small stamp (git short SHA) so a regenerated PDF can be told apart from a previous one."""
    try:
        sha = subprocess.check_output(
            ['git', 'rev-parse', '--short', 'HEAD'], stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        sha = 'dev'
    return f"v{sha}"


async def generate_pdf(html_path, pdf_path):
    """Generate PDF from HTML file"""
    if not os.path.exists(html_path):
        print(f"Error: HTML file not found at {html_path}")
        return False

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Load the HTML file
        file_url = f'file:///{os.path.abspath(html_path).replace(os.sep, "/")}'
        await page.goto(file_url, wait_until='networkidle')

        # Append a tiny version stamp inline onto the last existing line of
        # content (rather than as a new block) so it adds no extra height
        # and can't push a new page.
        await page.evaluate(
            """(label) => {
                const container = document.querySelector('.main-content');
                if (!container) return;
                const blocks = container.querySelectorAll('*');
                let last = null;
                for (const el of blocks) {
                    if (el.textContent && el.textContent.trim()) last = el;
                }
                if (!last) return;
                const stamp = document.createElement('span');
                stamp.textContent = ' ' + label;
                stamp.style.fontSize = '6pt';
                stamp.style.color = '#ccc';
                last.appendChild(stamp);
            }""",
            get_version_label()
        )

        # Generate PDF with print settings
        await page.pdf(
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
