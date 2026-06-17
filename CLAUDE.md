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

## Writing Style

Rules for all text in CV and cover letter bodies. Concrete and checkable.

### Forbidden patterns

- **Em-dashes in body text** — use a comma, parentheses, or restructure the sentence
- **"It's not X, it's Y" / "You don't just X, you Y"** — AI aphorism structure; always cut
- **Fake connection phrases** — "maps directly to," "resonates deeply with," "aligns perfectly with" followed by a company or role name. Show the connection through facts, not a sentence declaring one
- **Reinforcement adverbs used for rhetorical weight** — "actually," "deliberately," "truly," "genuinely," "seamlessly," "deeply" in that function
- **Banned vocabulary** — "delve," "showcase," "underscores," "noteworthy," "pivotal," "realm," "multifaceted," "meticulous," "commendable"
- **Latinate over plain** — "utilize" → use, "facilitate" → help, "commence" → start
- **Formulaic paragraph starters** — "furthermore," "moreover," "additionally" as openers
- **Sweeping career openers** — "I've spent X years doing Y" as the first sentence of a cover letter

### What to do instead

- **Start concrete** — open with a specific situation, a named project, a specific problem solved
- **Vary sentence length** — mix short sentences (under 10 words) with longer ones; uniform 15–20 word sentences read as AI
- **Vary paragraph length** — not all paragraphs should run to the same depth
- **Earned connections only** — let the facts make the connection; don't add a sentence announcing that the connection exists
- **Plain connectors** — "so," "then," "still," "which meant," "that took" over formal transitions
