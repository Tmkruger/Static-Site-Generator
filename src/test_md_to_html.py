import unittest
from markdown_to_html import *
from main import extract_title

class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_empty(self):
        md = """
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```

    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


class TestExtractHeader(unittest.TestCase):
    def test_default(self):
        md = """
# Header 1

## Header 2
    """

        header = extract_title(md)
        print(header)
        self.assertEqual(header, "Header 1")

    def test_basic_h1(self):
        md = "1# Header "
        self.assertEqual(extract_title(md), "Header 1")

    def test_leading_newlines(self):
        md = "\n\n# Header 1\n\n## Header 2"
        self.assertEqual(extract_title(md), "Header 1")

    def test_returns_first_h1_when_multiple(self):
        md = "# First\n\n# Second\n\n## Third"
        self.assertEqual(extract_title(md), "First")

    def test_ignores_h2_and_lower(self):
        md = "## Not it\n### Also not it\n\n# Real One"
        self.assertEqual(extract_title(md), "Real One")

    def test_no_h1_raises(self):
        md = "## Subheader only\nRegular text\n"
        with self.assertRaises(Exception):
            extract_title(md)

    def test_trims_trailing_spaces(self):
        md = "#  Header with spaces   "
        self.assertEqual(extract_title(md), "Header with spaces")

    def test_header_with_inline_formatting(self):
        md = "# Title with *emphasis* and **bold**"
        self.assertEqual(extract_title(md), "Title with *emphasis* and **bold**")

    def test_unicode_header(self):
        md = "# Café naïve—βeta 🚀"
        self.assertEqual(extract_title(md), "Café naïve—βeta 🚀")

    def test_windows_line_endings(self):
        md = "# Win Line\r\n\r\n## Next\r\n"
        self.assertEqual(extract_title(md), "Win Line")

    def test_text_before_hash_same_line_not_a_header(self):
        md = "X# Not a header\n# Real Header"
        self.assertEqual(extract_title(md), "Real Header")

    def test_indented_header_allowed(self):
        # Only passes if your regex allows optional leading spaces (^\s*# ...)
        md = "    # Indented Title"
        self.assertEqual(extract_title(md), "Indented Title")

    def test_code_block_doesnt_block_match(self):
        # Note: This shows current behavior: a '# ' inside code blocks WILL match
        # (unless you add code-block awareness). Keep it to lock current behavior.
        md = "```\n# code header\n```\n# Actual Title"
        # Because the regex matches the *first* occurrence, this asserts current behavior.
        # If you later decide to skip code blocks, update both function and test.
        self.assertEqual(extract_title(md), "code header")