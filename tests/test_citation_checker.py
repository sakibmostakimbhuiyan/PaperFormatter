import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from citation_checker import check, find_text_citations, find_bib_keys  # noqa: E402


class CitationCheckerTests(unittest.TestCase):
    def test_find_text_citations(self):
        text = "This cites [1] and again [2], plus [1] once more."
        self.assertEqual(find_text_citations(text), {"1", "2"})

    def test_find_bib_keys(self):
        bib = "@article{smith2024, author={J. Smith}}\n@book{lee2023, author={A. Lee}}"
        self.assertEqual(find_bib_keys(bib), {"smith2024", "lee2023"})

    def test_matched_counts_no_mismatch(self):
        text = "See [1] and [2]."
        bib = "@article{a, title={x}}\n@article{b, title={y}}"
        result = check(text, bib)
        self.assertFalse(result["count_mismatch"])
        self.assertFalse(result["non_sequential_numbering"])

    def test_missing_bib_entry_flagged(self):
        text = "See [1] and [2] and [3]."
        bib = "@article{a, title={x}}\n@article{b, title={y}}"
        result = check(text, bib)
        self.assertTrue(result["count_mismatch"])

    def test_non_sequential_numbering_flagged(self):
        text = "See [1] and [3]."
        bib = "@article{a, title={x}}\n@article{b, title={y}}"
        result = check(text, bib)
        self.assertTrue(result["non_sequential_numbering"])
        self.assertIn(2, result["missing_numbers"])


if __name__ == "__main__":
    unittest.main()
