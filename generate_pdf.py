"""
Simple PDF Generator for CV
Converts the HTML CV to PDF using Playwright
"""

import os
import asyncio
from playwright.async_api import async_playwright


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
    # File paths
    html_file = 'CV Nicolas Christie (en).html'
    pdf_file = 'CV Nicolas Christie (en).pdf'

    print(f"Generating PDF from {html_file}...")

    success = await generate_pdf(html_file, pdf_file)

    if success:
        print(f"PDF generated successfully: {os.path.abspath(pdf_file)}")
    else:
        print("PDF generation failed!")


if __name__ == '__main__':
    asyncio.run(main())
