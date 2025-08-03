from textnode import TextNode , TextType
from htmlnode import HtmlNode, LeafNode, ParentNode
from nodemanager import split_nodes_delmiter

def main():
    '''
        test = TextNode("Happy hApPy", TextType.TEXT)
        test2 = TextNode("SAD SAD", TextType.LINK, "https://youtube.com")
        test3 = HtmlNode("a", "link to youtube", None, {"href" : "https://youtube.com", "target": "_blank"})
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        parent_node = ParentNode("div", [])
        print("PRINTING!")
        print(repr(test))
        print(repr(test2))
        print(f"LEAF NODE HTML: {node.to_html()}")
        print(f'PARENT NODE HTML: {parent_node.children}')
    '''
    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delmiter([node], "`", TextType.CODE)
    print(f"NEW NODES: {new_nodes}")
    print(f'CONVERTED NODES: {split_nodes_delmiter([node], "`", TextType.CODE)}')
    pass

def text_node_to_html_node(text_node):
        match text_node.text_type:
            case TextType.TEXT:
                return LeafNode(None, text_node.text)
            case TextType.BOLD:
                return LeafNode("b", text_node.text)
            case TextType.ITALIC:
                return LeafNode("i", text_node.text)
            case TextType.CODE:
                return LeafNode("code", text_node.text)
            case TextType.LINK:
                return LeafNode("a", text_node.text, text_node.props)
            case TextType.IMAGE:
                return LeafNode("img", "", text_node.props)
            case _:
                raise ValueError("TextType not found")


main()
