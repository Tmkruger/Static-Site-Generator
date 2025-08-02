from textnode import TextNode , TextType
from htmlnode import HtmlNode, LeafNode, ParentNode

def main():
    test = TextNode("Happy hApPy", TextType.PLAIN)
    test2 = TextNode("SAD SAD", TextType.LINK, "https://youtube.com")
    test3 = HtmlNode("a", "link to youtube", None, {"href" : "https://youtube.com", "target": "_blank"})
    node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    parent_node = ParentNode("div", [])
    print("PRINTING!")
    print(repr(test))
    print(repr(test2))
    print(f"LEAF NODE HTML: {node.to_html()}")
    print(f'PARENT NODE HTML: {parent_node.children}')


main()
