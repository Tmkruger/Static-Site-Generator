import unittest

from textnode import TextNode, TextType
from nodemanager import extract_markdown_links, split_nodes_delmiter, extract_markdown_images, split_nodes_image, split_nodes_link, text_to_textnodes





class TestSplitNodeDelimiter(unittest.TestCase):
    def test_double_bold(self):
        text1 = TextNode("This is text with a **bold****twice**", TextType.TEXT)
        nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("twice", TextType.BOLD)
        ]
        self.assertListEqual(split_nodes_delmiter([text1], "**", TextType.BOLD), nodes)


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
        new_nodes = split_nodes_delmiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("*italic* is at the start and an ending ", TextType.TEXT),TextNode("bold", TextType.BOLD)])
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

class TestSplitNodeLink(unittest.TestCase):
    def test_split_no_link(self):
        node = TextNode(
            "This is text that has no markdown",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text that has no markdown", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_single_link(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode(
                    "image", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_multiple_links(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_link_beg_mid_end(self):
        node = TextNode(
            "[image](https://i.imgur.com/1elNhQu.png) is the first image, and [second image](https://i.imgur.com/2elNhQu.png) as well as [third image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.LINK, "https://i.imgur.com/1elNhQu.png"),
                TextNode(" is the first image, and ", TextType.TEXT),
                TextNode("second image", TextType.LINK, "https://i.imgur.com/2elNhQu.png"),
                TextNode(" as well as ", TextType.TEXT),
                TextNode("third image", TextType.LINK, "https://i.imgur.com/3elNhQu.png")
            ],
            new_nodes,
        )


    def test_split_only_link(self):
        node = TextNode(
            "[image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode(
                    "image", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_link_no_alt(self):
        node = TextNode(
            "This is text with an [](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode(
                    "", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_link_complex_url(self):
        node = TextNode(
            "This is text with an [image](https://example.com/path/image.png?param=value)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode(
                    "image", TextType.LINK, "https://example.com/path/image.png?param=value"
                ),
            ],
            new_nodes,
        )

    def test_split_link_multiple_nodes(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "This is text with an [image](https://example.com/path/image.png?param=value)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node,node2])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode(
                    "image", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode("This is text with an ", TextType.TEXT),
                TextNode(
                    "image", TextType.LINK, "https://example.com/path/image.png?param=value"
                ),

            ],
            new_nodes,
        )

class TestTextToTextNode(unittest.TestCase):
    def base_case(self):
        text1 = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(text_to_textnodes(text1), nodes)

    def test_no_markdown(self):
        text1 = "This is text with an italic word and a code block and an obi wan imagemhttps://i.imgur.com/fJRm4Vk.jpeg and a link https://boot.dev"
        nodes = [
            TextNode("This is text with an italic word and a code block and an obi wan imagemhttps://i.imgur.com/fJRm4Vk.jpeg and a link https://boot.dev", TextType.TEXT),
        ]
        self.assertListEqual(text_to_textnodes(text1), nodes)

    def test_double_bold(self):
        text1 = "This is text with a **bold****twice**"
        nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("twice", TextType.BOLD)
        ]
        self.assertListEqual(text_to_textnodes(text1), nodes)

    def test_empty_markdown(self):
        text1 = "This is text with a ****"
        nodes = [
            TextNode("This is text with a ", TextType.TEXT)
        ]
        self.assertListEqual(text_to_textnodes(text1), nodes)

    def test_empty_string(self):
        text = ""
        nodes = [TextNode("", TextType.TEXT)]
        self.assertListEqual(text_to_textnodes(text), nodes)

    def test_beg_mid_end(self):
        text = "**bold** plain text *italic* [youtube](https://youtube.com)"
        nodes = [
            TextNode("bold", TextType.BOLD),
            TextNode(" plain text ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("youtube", TextType.LINK, "https://youtube.com")
        ]
        self.assertListEqual(text_to_textnodes(text), nodes)

    def test_multiple_spaces(self):
        text = "**bold**       plain text      *italic*      "
        nodes = [
            TextNode("bold", TextType.BOLD),
            TextNode("       plain text      ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode("      ", TextType.TEXT)
        ]
        self.assertListEqual(text_to_textnodes(text), nodes)

    def test_malformed_markdown(self):
        text = "**bold* is malformed but *italic* is not"
        nodes = [
            TextNode("**bold* is malformed but *italic* is not", TextType.TEXT)
        ]
        self.assertListEqual(text_to_textnodes(text), nodes)

    def test_realworld_link(self):
        text = "For more information, visit [our documentation](https://docs.example.com)."
        nodes = [
            TextNode("For more information, visit ", TextType.TEXT),
            TextNode("our documentation", TextType.LINK, "https://docs.example.com"),
            TextNode(".", TextType.TEXT)
        ]

    def test_realworld_image(self):
        text = "![profile picture](https://example.com/avatar.png)Welcome to my blog post about Python!"
        nodes = [
            TextNode("profile picture", TextType.IMAGE, "https://example.com/avatar.png"),
            TextNode("Welcome to my blog post about Python!", TextType.TEXT)
        ]

    def test_realworld_code(self):
        text = "Use the `print(\"Hello, world!\")` function to display text."
        nodes = [
            TextNode("Use the ", TextType.TEXT),
            TextNode("print(\"Hello, world!\")", TextType.CODE),
            TextNode(" function to display text.", TextType.TEXT)
        ]
