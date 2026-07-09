"""
Simple PDF Generator for CV
Converts the HTML CV to PDF using Playwright
"""

import os
import re
import asyncio
from playwright.async_api import async_playwright

# Bounds for the auto-fit search. Kept fairly narrow so the CV and cover
# letter never end up looking like noticeably different text sizes next
# to each other.
SCALE_FLOOR = 0.85
SCALE_CEIL = 1.2

GROWTH_FACTOR = 1.08
SHRINK_FACTOR = 1 / 1.08

# Final scale tolerance for the binary search, and how far below the
# measured fit boundary to land - small safety margin so a tiny rendering
# difference between environments (e.g. local Windows vs. the CI runner's
# fallback font) can't tip the result over the page limit.
TOLERANCE = 0.01
SAFETY_MARGIN = 0.015


def pdf_page_count(pdf_bytes):
    counts = [int(m) for m in re.findall(rb'/Count\s+(\d+)', pdf_bytes)]
    return max(counts) if counts else None


async def render_at_scale(page, pdf_path, scale):
    await page.pdf(
        path=pdf_path,
        format='A4',
        print_background=True,
        scale=scale,
        margin={
            'top': '0mm',
            'right': '0mm',
            'bottom': '0mm',
            'left': '0mm'
        }
    )


async def find_fit_scale(page, pdf_path, target_pages):
    """Binary-search the render scale against real rendered page counts
    to find the largest scale that still fits within target_pages."""

    async def pages_at(scale):
        await render_at_scale(page, pdf_path, scale)
        with open(pdf_path, 'rb') as f:
            return pdf_page_count(f.read())

    scale = 1.0
    pages = await pages_at(scale)

    if pages <= target_pages:
        lo, hi = scale, None
        candidate = scale
        while hi is None and candidate < SCALE_CEIL:
            candidate = min(candidate * GROWTH_FACTOR, SCALE_CEIL)
            if await pages_at(candidate) > target_pages:
                hi = candidate
            else:
                lo = candidate
        if hi is None:
            return lo
    else:
        hi, lo = scale, None
        candidate = scale
        while lo is None and candidate > SCALE_FLOOR:
            candidate = max(candidate * SHRINK_FACTOR, SCALE_FLOOR)
            if await pages_at(candidate) <= target_pages:
                lo = candidate
            else:
                hi = candidate
        if lo is None:
            return SCALE_FLOOR

    while hi - lo > TOLERANCE:
        mid = (lo + hi) / 2
        if await pages_at(mid) <= target_pages:
            lo = mid
        else:
            hi = mid

    return max(SCALE_FLOOR, lo - SAFETY_MARGIN)


async def generate_pdf(html_path, pdf_path, target_pages):
    """Generate PDF from HTML file, auto-scaled to fill target_pages exactly."""
    if not os.path.exists(html_path):
        print(f"Error: HTML file not found at {html_path}")
        return False

    launch_kwargs = {}
    _chromium_path = os.environ.get('PW_CHROMIUM_PATH')
    if _chromium_path and os.path.exists(_chromium_path):
        launch_kwargs['executable_path'] = _chromium_path

    async with async_playwright() as p:
        browser = await p.chromium.launch(**launch_kwargs)
        page = await browser.new_page()

        # Load the HTML file
        file_url = f'file:///{os.path.abspath(html_path).replace(os.sep, "/")}'
        await page.goto(file_url, wait_until='networkidle')

        scale = await find_fit_scale(page, pdf_path, target_pages)
        await render_at_scale(page, pdf_path, scale)

        await browser.close()

    return True


async def main():
    files_to_generate = [
        ('docs/index.html', 'docs/pdf/CV Nicolas Christie (en).pdf', 2),
        ('docs/cover-letter.html', 'docs/pdf/CL Nicolas Christie (en).pdf', 1),
    ]

    all_success = True
    for html_file, pdf_file, target_pages in files_to_generate:
        print(f"Generating PDF from {html_file}...")
        success = await generate_pdf(html_file, pdf_file, target_pages)

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
