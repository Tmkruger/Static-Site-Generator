import unittest

from textnode import TextNode, TextType
from nodemanager import extract_markdown_links, split_nodes_delmiter, extract_markdown_images, split_nodes_image, split_nodes_link




class TestSplitNodeDelimiter(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is plain text node", TextType.TEXT)
        new_nodes = split_nodes_delmiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [node])
    def test_bold(self):
        node = TextNode("This is a **bold** text node", TextType.TEXT)
        new_nodes = split_nodes_delmiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is a ", TextType.TEXT), TextNode("bold", TextType.BOLD), TextNode(" text node", TextType.TEXT)])
    def test_italic(self):
        node = TextNode("This is a *italic* text node", TextType.TEXT)
        new_nodes = split_nodes_delmiter([node], "*", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("This is a ", TextType.TEXT), TextNode("italic", TextType.ITALIC), TextNode(" text node", TextType.TEXT)])
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delmiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT)])
    def test_delim_beg(self):
        node = TextNode("*italic* is at the start", TextType.TEXT)
        new_nodes = split_nodes_delmiter([node], "*", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("italic", TextType.ITALIC), TextNode(" is at the start", TextType.TEXT)])
    def test_delim_end(self):
        node = TextNode("italic is at the *end*", TextType.TEXT)
        new_nodes = split_nodes_delmiter([node], "*", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("italic is at the ", TextType.TEXT), TextNode("end", TextType.ITALIC)])
    def test_multi_delim_same(self):
        node = TextNode("*italic* is at the start and *end*", TextType.TEXT)
        new_nodes = split_nodes_delmiter([node], "*", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("italic", TextType.ITALIC), TextNode(" is at the start and ", TextType.TEXT), TextNode("end", TextType.ITALIC)])
    def test_multi_delim_diff(self):
        node = TextNode("*italic* is at the start and an ending **bold**", TextType.TEXT)
        new_nodes = split_nodes_delmiter([node], "*", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("italic", TextType.ITALIC), TextNode(" is at the start and an ending **bold**", TextType.TEXT)])
    def test_no_delim(self):
        node = TextNode("*italic* is at the start and an ending **bold**", TextType.TEXT)
        new_nodes = split_nodes_delmiter([node], "", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("*italic* is at the start and an ending **bold**", TextType.TEXT)])
    def test_mixed_node_type(self):
        node = TextNode("*italic* is at the start and an ending **bold**", TextType.TEXT)
        node2 = TextNode("end", TextType.ITALIC)
        node3 = TextNode("code block", TextType.CODE)
        nodes = [node,node2,node3]
        new_nodes = split_nodes_delmiter(nodes, "", TextType.ITALIC)
        self.assertEqual(new_nodes, nodes)

class TestExtractImage(unittest.TestCase):
    def test_default(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertEqual(matches, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_no_text(self):
        text = "![rick roll](https://i.imgur.com/aKaOqIh.gif)![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertEqual(matches, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_missing_exclamation(self):
            text = "[rick roll](https://i.imgur.com/aKaOqIh.gif)![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
            matches = extract_markdown_images(text)
            self.assertEqual(matches, [("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_malformed(self):
            text = "![rick roll(https://i.imgur.com/aKaOqIh.gif)![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
            matches = extract_markdown_images(text)
            self.assertEqual(matches, [("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_nested(self):
        text = "[![rick roll](https://i.imgur.com/aKaOqIh.gif)](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertEqual(matches, [("rick roll", "https://i.imgur.com/aKaOqIh.gif")])

    def test_special_characters(self):
        text = "This is text with a ![rick & roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertEqual(matches, [("rick & roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_no_url(self):
        text = "This is text with a ![rick roll]() and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertEqual(matches, [("rick roll", ""), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_extra_parenthesis(self):
        text = "This is text with a ![rick roll]() and ![obi wan](https://i.imgur.com/fJRm(4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertEqual(matches, [("rick roll", ""), ("obi wan", "https://i.imgur.com/fJRm(4Vk.jpeg")])

class TestExtractLink(unittest.TestCase):
    def test_default(self):
        matches = extract_markdown_links(
            "This is a link to [youtube](https://www.youtube.com)"
        )
        self.assertListEqual([("youtube", "https://www.youtube.com")], matches)

    def test_no_text(self):
        matches = extract_markdown_links(
            "[youtube](https://www.youtube.com)"
        )
        self.assertListEqual([("youtube", "https://www.youtube.com")], matches)

    def test_malformed_link(self):
        matches = extract_markdown_links(
            "This is a link to [youtube](https:www.youtube.com)"
        )
        self.assertListEqual([("youtube", "https:www.youtube.com")], matches)

    def test_malformed(self):
        matches = extract_markdown_links(
            "This is a link to [youtube(https://www.youtube.com)"
        )
        self.assertListEqual([], matches)

    def test_nested(self):
        matches = extract_markdown_links(
            "This is a link to [youtube]([instagram](https://instagram.com)])"
        )
        self.assertListEqual([("instagram", "https://instagram.com")], matches)

    def test_special_characters(self):
        matches = extract_markdown_links(
            "This is a link to [youtube](https://www.you@tube.com)"
        )
        self.assertListEqual([("youtube", "https://www.you@tube.com")], matches)

    def test_no_url(self):
        matches = extract_markdown_links(
            "This is a link to [youtube]()"
        )
        self.assertListEqual([("youtube", "")], matches)

class TestSplitNodeImage(unittest.TestCase):

    def test_split_no_image(self):
        node = TextNode(
            "This is text that has no markdown",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text that has no markdown", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_single_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode(
                    "image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_multiple_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

        def test_split_images_with_link(self):
            node = TextNode(
                "This is text with an [youtube](https://youtube.com) and a ![second image](https://i.imgur.com/3elNhQu.png)",
                TextType.TEXT,
            )
            new_nodes = split_nodes_image([node])
            self.assertListEqual(
                [
                    TextNode("This is text with an [youtube](https://youtube.com) and a ", TextType.TEXT),
                    TextNode(
                        "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                    ),
                ],
                new_nodes,
            )
############################################################
    def test_split_image_beg_end(self):
        node = TextNode(
            "![image](https://i.imgur.com/1elNhQu.png) is the first image, and ![second image](https://i.imgur.com/2elNhQu.png) as well as ![third image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/1elNhQu.png"),
                TextNode(" is the first image, and ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/2elNhQu.png"),
                TextNode(" as well as ", TextType.TEXT),
                TextNode("third image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
            ],
            new_nodes,
        )


    def test_split_only_image(self):
        node = TextNode(
            "![image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode(
                    "image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_image_no_alt(self):
        node = TextNode(
            "This is text with an ![](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode(
                    "", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_image_complex_url(self):
        node = TextNode(
            "This is text with an ![image](https://example.com/path/image.png?param=value)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode(
                    "image", TextType.IMAGE, "https://example.com/path/image.png?param=value"
                ),
            ],
            new_nodes,
        )

    def test_split_image_multiple_nodes(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "This is text with an ![image](https://example.com/path/image.png?param=value)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node,node2])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode(
                    "image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode("This is text with an ", TextType.TEXT),
                TextNode(
                    "image", TextType.IMAGE, "https://example.com/path/image.png?param=value"
                ),

            ],
            new_nodes,
        )
