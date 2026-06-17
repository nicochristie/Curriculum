## Project Overview

Lightweight CV and Cover Letter project with HTML documents and PDF generation.

**Files:**
- `docs/index.html` - Curriculum Vitae document
- `docs/cover-letter.html` - Cover Letter document
- `docs/styles/cv_styles.css` - Shared stylesheet for both documents
- `docs/media/header-photo.jpg` - Profile photo used in the CV header
- `generate_pdf.py` - Python script to convert HTML files to PDF using Playwright

## Setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install playwright
playwright install
```

## Connect to venv

```powershell
# PowerShell
.venv\Scripts\Activate.ps1

# Command Prompt
.venv\Scripts\activate.bat
```

## Usage

```powershell
python generate_pdf.py
```

Generates PDF files to `docs/pdf/`:
- `docs/pdf/CV Nicolas Christie (en).pdf`
- `docs/pdf/CL Nicolas Christie (en).pdf`

## Technical Details

- **HTML to PDF conversion**: Uses Playwright for browser-based rendering
- **Format**: A4 with zero margins to preserve exact layout
- **CSS support**: Full CSS styling preserved in PDF output
