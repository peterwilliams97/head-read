"""test_hardread.py pins the Markdown handling in hardread.py: what is dropped, what becomes the
placeholder, that no block crosses a paragraph or list-item break, and that every block keeps the
source line it started on. No trained spaCy model is loaded here — a blank English pipeline with
a sentencizer stands in where a test needs sentences — so these run in milliseconds.
"""

import unittest

import spacy

from hardread import hardread
from hardread.features import Finding, sentence_line


class MarkdownTest(unittest.TestCase):
    def test_drops_fences_and_headings(self):
        self.assertEqual(texts(SOURCE), [
            "First paragraph runs over two lines.",
            "Call CODE and see CODE for docs.",
            "One item.",
            "Another item continues here.",
            "Quoted text keeps its link.",
        ])

    def test_line_numbers(self):
        self.assertEqual([b[0] for b in hardread.markdown_blocks(SOURCE)], [7, 10, 15, 16, 19])

    def test_line_starts_follow_substitution(self):
        first, starts, text = hardread.markdown_blocks("See `a very long span` here\nand there.")[0]
        self.assertEqual((first, starts), (1, [0, 14]))
        self.assertEqual(text[starts[1]:], "and there.")

    def test_emphasis_across_lines(self):
        source = 'He wrote *"this goes\nover a line"* once. Then\nhe stopped.'
        first, starts, text = hardread.markdown_blocks(source)[0]
        self.assertEqual(text, 'He wrote "this goes over a line" once. Then he stopped.')
        self.assertEqual((first, text[starts[1]:starts[2]], text[starts[2]:]),
                         (1, 'over a line" once. Then ', "he stopped."))
        nlp = spacy.blank("en")
        nlp.add_pipe("sentencizer")
        doc = nlp(text)
        doc.user_data["first_line"], doc.user_data["line_starts"] = first, starts
        self.assertEqual([(s.text, sentence_line(s)) for s in doc.sents],
                         [('He wrote "this goes over a line" once.', 1), ("Then he stopped.", 2)])

    def test_setext_heading_dropped(self):
        self.assertEqual(texts("Title\n=====\n\nBody text."), ["Body text."])

    def test_link_list_dropped(self):
        source = "[a](x) (every field) · [b](y) (the code) · [c](z)\n\nBody text."
        self.assertEqual(texts(source), ["Body text."])

    def test_text_blocks(self):
        self.assertEqual(hardread.text_blocks("a b\nc\n\n\nd"), [(1, [0, 4], "a b c"), (5, [0], "d")])

    def test_mark(self):
        f = Finding("StackedNouns", "The cache eviction policy is long.", "cache eviction policy", 1, "")
        self.assertEqual(hardread.mark(f), "The «cache eviction policy» is long.")


def texts(source):
    return [text for _, _, text in hardread.markdown_blocks(source)]


SOURCE = """\
# Heading

```go
x := 1
```

First paragraph runs
over two lines.

Call `fn()` and see https://example.com/x for docs.

## Sub

| a | b |
- One item.
- Another item
  continues here.

> Quoted text keeps its [link](https://example.com).
"""


if __name__ == "__main__":
    unittest.main()
