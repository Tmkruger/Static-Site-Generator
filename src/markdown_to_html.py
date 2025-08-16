from htmlnode import HtmlNode, ParentNode, LeafNode
from nodemanager import *



def markdown_to_html_node(markdown):
    if markdown == "":
        return ParentNode("div", [])
    nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_blocktype(block)
        #print(f"Block: {block} | Block_Type: {block_type}")
        children_nodes = text_to_children(block, block_type)
        match block_type:
            case BlockType.HEADING:
                heading_count = block.count("#")
                nodes.append(ParentNode(f"h{heading_count}", children_nodes))
            case BlockType.CODE:
                nodes.append(text_to_code_node(block))
            case BlockType.QUOTE:
                nodes.append(ParentNode("blockquote", children_nodes))
            case BlockType.U_LIST:
                items = block.split("\n")
                li_nodes = []
                for item in items:
                    item = strip_md_id(item, block_type)
                    li_nodes.append(ParentNode("li", text_to_children(item, BlockType.PARAGRAPH)))
                nodes.append(ParentNode("ul", li_nodes))
            case BlockType.O_LIST:
                items = block.split("\n")
                li_nodes = []
                for item in items:
                    item = strip_md_id(item, block_type)
                    li_nodes.append(ParentNode("li", text_to_children(item, BlockType.PARAGRAPH)))
                nodes.append(ParentNode("ol", li_nodes))
            case BlockType.PARAGRAPH:
                nodes.append(ParentNode("p", children_nodes))
            case _:
                pass
    return ParentNode("div", nodes)


def text_to_children(block, block_type):
    children = []
    block = strip_md_id(block, block_type)
    text_nodes = text_to_textnodes(block)
    #print(f"Text Nodes: {text_nodes}")
    for node in text_nodes:
        children.append(text_node_to_html_node(node))
    #print(f"CHILDREN: {children}")
    return children

def strip_md_id(text, block_type):
    #text = text.replace("\n", " ")
    #print(f"\nTEXT: {text}!!--!!\n")
    match block_type:
        case BlockType.HEADING:
            text = text.lstrip("#")
            text = text.lstrip()
            return text
        case BlockType.QUOTE:
            text = text.replace("> ","")
            text = text.replace(">", "")
            return text
        case BlockType.O_LIST:
            return text.split(". ")[1]
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
    #print(f'\nTEXT: {text}!!--!!\n')
    block = text.lstrip("```\n")
    block = block.rstrip("```")
    child = LeafNode("code", block)
    parent = ParentNode("pre", [child])
    return parent
