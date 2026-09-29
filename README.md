# 📄 PaperFormatter: Citation Consistency Checker

> A small Python tool that checks whether in-text `[n]` citations in a research manuscript line up with the entries in a `.bib` bibliography file, plus an optional HTML→PDF renderer for a simple print layout.

![Status](https://img.shields.io/badge/status-working%20prototype-brightgreen)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 🎯 Motivation

Manually checking that every `[3]` in a paper's text has a matching bibliography entry (and vice versa) is tedious and error-prone. This tool automates that specific check.

## ⚠️ What This Is (and Is Not)

- It does **not** check IEEE/APA formatting rules, only citation-count consistency.
- It matches citation **numbers** (`[1]`, `[2]`) against the **count** of `.bib` entries — it cannot verify that citation `[2]` in the text corresponds to the *second* bib entry, since `.bib` files are keyed by name, not number. It flags count mismatches and gaps in numbering, which are the two most common real mistakes.
- The PDF renderer (`src/format_pdf.py`) depends on [WeasyPrint](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html), which was **not** tested in the environment this project was built in — WeasyPrint needs system libraries (Pango, Cairo) that must be installed separately. Test it on your own machine after `pip install weasyprint`.
- The citation checker (`src/citation_checker.py`) **is** tested and runs with only the Python standard library — see `tests/`.

## ⚙️ How It Works

`citation_checker.py`:
1. Finds all `[n]` citation numbers in the manuscript text.
2. Finds all `@type{key, ...}` entries in the `.bib` file.
3. Reports a count mismatch or a gap in citation numbering (e.g. `[1]` and `[3]` used but no `[2]`).

## 🚀 Usage

```bash
git clone https://github.com/sakibmostakimbhuiyan/PaperFormatter.git
cd PaperFormatter

# Check citations (works out of the box, no dependencies)
python3 src/citation_checker.py samples/sample_paper.html samples/references.bib

# Run tests
python3 -m unittest tests/test_citation_checker.py

# Optional: render to PDF (requires WeasyPrint + system libraries)
pip install weasyprint
python3 src/format_pdf.py samples/sample_paper.html samples/style.css output.pdf
```

## 🗂️ Project Structure

```
src/        citation_checker.py (tested), format_pdf.py (untested, needs WeasyPrint)
tests/      unit tests for citation_checker.py
samples/    example manuscript, stylesheet, and .bib file
```

## 🗺️ Roadmap

- [x] Citation-count checker with unit tests
- [ ] Test and confirm PDF rendering with WeasyPrint locally
- [ ] Support APA-style author-year citations, not just numbered
- [ ] Flag bib entries that are never cited in the text

## 📄 License

MIT License. See [LICENSE](LICENSE).

## 👤 Author

**Sakib Mostakim Bhuiyan** · [GitHub](https://github.com/sakibmostakimbhuiyan)
