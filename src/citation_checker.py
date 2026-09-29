"""Citation checker: cross-references in-text [n] citations with a BibTeX file.

This does simple pattern matching only. It does not validate citation
formatting style (IEEE/APA/etc.) or check whether a .bib entry's content
is correct -- only whether numbers/keys line up between the two files.
"""
import re

CITATION_PATTERN = re.compile(r"\[(\d+)\]")
BIB_ENTRY_PATTERN = re.compile(r"@\w+\s*\{\s*([^,\s]+)")


def find_text_citations(html_or_text):
    """Return the set of citation numbers used in the text, as strings."""
    return set(CITATION_PATTERN.findall(html_or_text))


def find_bib_keys(bib_content):
    """Return the set of entry keys defined in a .bib file."""
    return set(BIB_ENTRY_PATTERN.findall(bib_content))


def check(html_or_text, bib_content):
    """Compare in-text citation numbers against bib entry count.

    Because in-text citations are numbers like [1], [2] and .bib entries
    are keyed by name (e.g. `smith2025`), this cannot match a specific
    number to a specific entry. It reports:
      - which numbers appear in the text
      - how many bib entries exist
      - a warning if those counts don't match, since that often signals
        a missing or extra reference
    """
    text_citations = find_text_citations(html_or_text)
    bib_keys = find_bib_keys(bib_content)

    numbers = sorted(int(n) for n in text_citations)
    expected = list(range(1, len(numbers) + 1)) if numbers else []
    missing_numbers = sorted(set(expected) - set(numbers))

    return {
        "citations_in_text": numbers,
        "bib_entries_found": len(bib_keys),
        "bib_keys": sorted(bib_keys),
        "count_mismatch": len(numbers) != len(bib_keys),
        "non_sequential_numbering": missing_numbers != [],
        "missing_numbers": missing_numbers,
    }


def format_report(result):
    lines = ["Citation check (pattern-matching only, not a style validator):"]
    lines.append(f"  In-text citation numbers found: {result['citations_in_text']}")
    lines.append(f"  Bibliography entries found: {result['bib_entries_found']}")
    if result["count_mismatch"]:
        lines.append(
            "  ⚠ Count mismatch: number of in-text citations does not match "
            "number of bib entries. Check for a missing or unused reference."
        )
    if result["non_sequential_numbering"]:
        lines.append(
            f"  ⚠ Citation numbers are not sequential from 1. "
            f"Missing: {result['missing_numbers']}"
        )
    if not result["count_mismatch"] and not result["non_sequential_numbering"]:
        lines.append("  ✔ No issues detected by these checks.")
    return "\n".join(lines)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Check citations against a .bib file.")
    parser.add_argument("text_file", help="HTML or text file with [n] citations")
    parser.add_argument("bib_file", help=".bib file")
    args = parser.parse_args()

    with open(args.text_file, encoding="utf-8") as f:
        text = f.read()
    with open(args.bib_file, encoding="utf-8") as f:
        bib = f.read()

    print(format_report(check(text, bib)))
