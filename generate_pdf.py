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
    files_to_generate = [
        ('CV Nicolas Christie (en).html', 'CV Nicolas Christie (en).pdf'),
        ('CL Nicolas Christie (en).html', 'CL Nicolas Christie (en).pdf'),
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
