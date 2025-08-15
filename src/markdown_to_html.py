from htmlnode import HtmlNode, ParentNode, LeafNode
from nodemanager import *



def markdown_to_html_node(markdown):
    string = ""
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_blocktype(block)
        print(f"Block: {block} | Block_Type: {block_type}")
        children_nodes = text_to_children(block, block_type)
        match block_type:
            case BlockType.HEADING:
                heading_count = block.count("#")
                string += ParentNode(f"h{heading_count}", children_nodes).to_html()
            case BlockType.CODE:
                string += text_to_code_node(block)
            case BlockType.QUOTE:
                string += ParentNode("blockquote", children_nodes).to_html()
            case BlockType.U_LIST:
                child_nodes = []
                list_items = block.split("\n")
                for item in list_items:
                    item = strip_md_id(item, block_type)
                    child_nodes.append(LeafNode("li", item))
                string += ParentNode("ul", child_nodes).to_html()
            case BlockType.O_LIST:
                child_nodes = []
                list_items = block.split("\n")
                for item in list_items:
                    item = strip_md_id(item, block_type)
                    child_nodes.append(LeafNode("li", item))
                string += ParentNode("ol", child_nodes).to_html()

            case BlockType.PARAGRAPH:
                string += ParentNode("p", children_nodes).to_html()
            case _:
                pass
        print(f"STRING: {string}")


def text_to_children(block, block_type):
    children = []
    block = strip_md_id(block, block_type)
    text_nodes = text_to_textnodes(block)
    print(f"Text Nodes: {text_nodes}")
    for node in text_nodes:
        children.append(text_node_to_html_node(node))
    print(f"CHILDREN: {children}")
    return children

def strip_md_id(text, block_type):
    match block_type:
        case BlockType.HEADING:
            text = text.lstrip("#")
            text = text.lstrip()
            return text
        case BlockType.QUOTE:
            return text.lstrip(">")
        case BlockType.O_LIST:
            return text.lstrip(". ")
        case BlockType.U_LIST:
            return text.lstrip("- ")
        case BlockType.PARAGRAPH:
            return text
        case BlockType.CODE:
            text = text.lstrip("'")
            text = text.rstrip("'")
            return text
        case _:
            raise Exception("unknown block type")

def text_to_code_node(text):

    return ""
