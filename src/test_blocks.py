import unittest

from nodemanager import markdown_to_blocks, block_to_blocktype, BlockType

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_multiple_new_lines(self):
        md = """
This is **bolded** paragraph





This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_no_new_lines(self):
        md = """
This is **bolded** paragraph
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph\nThis is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line\n- This is a list\n- with items"
            ]
        )

    def test_whitespace(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty(self):
        md = """
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
            ]
        )

    def test_only_new_lines(self):
        md = """




"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
            ]
        )

class TestBlockType(unittest.TestCase):
    def test_heading6(self):
        block = "###### This is a Heading"
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_heading1(self):
        block = "# This is a Heading"
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_code(self):
        block = "```print(\"This is a code snippet\")```"
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_code2(self):
        code_block = r"```\nThis is text that _should_ remain\nthe **same** even with inline stuff\n```"
        block_type = block_to_blocktype(code_block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_quote(self):
        block = ">To infinity and beyond!"
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_u_list(self):
        block = "- Milk"
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.U_LIST)

    def test_o_list(self):
        block = ". Cereal"
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.O_LIST)

    def test_paragraph(self):
        block = "This is a paragraph"
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_malformed(self):
        block = "##$ This wanted to be a heading"
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
