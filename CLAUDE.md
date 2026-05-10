## Project Overview

Lightweight CV and Cover Letter project with HTML documents and PDF generation.

**Files:**
- `index.html` - Curriculum Vitae document with embedded styles
- `cover-letter.html` - Cover Letter document with embedded styles
- `generate_pdf.py` - Python script to convert HTML files to PDF using Playwright
- `styles/cv_styles.css` - Shared stylesheet for both documents

## Setup

```
python -m venv venv
venv\Scripts\activate
pip install playwright
playwright install
```

## Usage

```
python generate_pdf.py
```

Generates PDF files to `docs/pdf/`:
- `docs/pdf/CV Nicolas Christie (en).pdf`
- `docs/pdf/CL Nicolas Christie (en).pdf`

## Technical Details

- **HTML to PDF conversion**: Uses Playwright for browser-based rendering
- **Format**: A4 with zero margins to preserve exact layout
- **CSS support**: Full CSS styling preserved in PDF output