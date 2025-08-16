from textnode import TextNode, TextType
from htmlnode import *
from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "code"
    QUOTE = "blockquote"
    U_LIST = "ul"
    O_LIST = "ol"

def split_nodes_delmiter(old_nodes, delimiter, text_type):
    converted_nodes = []
    if not old_nodes:
        raise ValueError("No nodes to split")

    if not delimiter:
        # Return a shallow copy of the original list
        for node in old_nodes:
            converted_nodes.append(node)
        return converted_nodes

    re_delim = re.escape(delimiter)
    # Match the same opener/closer via \1 and allow back-to-back like **a****b**
    # Escaped delimiters (e.g., \**) are ignored via (?<!\\)
    pattern = rf'(?<!\\)({re_delim})(.*?)\1'

    for node in old_nodes:
        if not isinstance(node, TextNode):
            raise ValueError("Node is not a TextNode")

        text = node.text or ""
        if text.count(delimiter) % 2 != 0:
            # Handle malformed case — maybe treat everything as plain text
            converted_nodes.append(TextNode(text, TextType.TEXT))
            continue

        matches = list(re.finditer(pattern, text))
        if not matches:
            converted_nodes.append(node)
            continue

        last_end = 0
        for match in matches:
            # Unstyled text before the match
            if match.start() > last_end:
                unstyled_text = text[last_end:match.start()]
                if unstyled_text:
                    converted_nodes.append(TextNode(unstyled_text, TextType.TEXT))

            # Styled (delimited) inner text (group 2)
            styled_text = match.group(2)
            if styled_text:
                converted_nodes.append(TextNode(styled_text, text_type))

            last_end = match.end()

        # Trailing unstyled text
        if last_end < len(text):
            remaining = text[last_end:]
            if remaining:
                converted_nodes.append(TextNode(remaining, TextType.TEXT))

    return converted_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\)]*)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def split_nodes_image(old_nodes):
    converted_nodes = []
    if not old_nodes:
        raise ValueError("No nodes to split")

    for node in old_nodes:
        if not isinstance(node, TextNode):
            raise ValueError("Node is not a TextNode")

        text = node.text

        matches = extract_markdown_images(text)
        if not matches:
            converted_nodes.append(node)
            continue
        for match in matches:
            image_alt = match[0]
            image_link = match[1]
            sections = text.split(f"![{image_alt}]({image_link})", 1)
            for section in sections:
                if not extract_markdown_images(section) and section != "":
                    converted_nodes.append(TextNode(section, TextType.TEXT))
                if TextNode("", TextType.IMAGE, {"src": image_link, "alt": image_alt}) not in converted_nodes:
                    converted_nodes.append(TextNode("", TextType.IMAGE, {"src": image_link, "alt": image_alt}))
            text = sections[len(sections)-1]
    return converted_nodes

def split_nodes_link(old_nodes):
    out = []
    link_re = re.compile(r'(?<!!)\[([^\[\]]+)\]\(([^()\s]+)\)')  # [text](url), not images

    for node in old_nodes:
        # Only rewrite plain TEXT nodes
        if not isinstance(node, TextNode) or node.text_type is not TextType.TEXT:
            out.append(node)
            continue

        text = node.text or ""
        pos = 0
        for m in link_re.finditer(text):
            start, end = m.span()
            alt, url = m.group(1), m.group(2)

            if start > pos:
                out.append(TextNode(text[pos:start], TextType.TEXT))            # keep text before link
            out.append(TextNode(alt, TextType.LINK, {"href": url}))            # use href, not src
            pos = end

        if pos < len(text):
            out.append(TextNode(text[pos:], TextType.TEXT))                     # keep trailing text

    return out

def text_to_textnodes(text):
    # Start with one TEXT node, then transform step-by-step.
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)                 # must run before bold/italic/code
    nodes = split_nodes_delmiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delmiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delmiter(nodes, "_", TextType.ITALIC)  
    nodes = split_nodes_delmiter(nodes, "`", TextType.CODE)
    return nodes

def find_malformed_delimiters(text, delimiter):
    count = text.count(delimiter)
    return count % 2 != 0

def markdown_to_blocks(markdown):
    if markdown == "":
        return []
    blocks = []
    temp = ""
    sections = markdown.split("\n")
    start_of_block = True
    for section in sections:
        #print(f"SECTION: {section} | START OF BLOCK?: {start_of_block}")
        #print(f"TEMP: {temp}| BLOCKS: {blocks}")
        section = section.strip(" ")
        if section == "" and temp == "":
            #print("TURNING TRUE")
            start_of_block = True
            continue
        elif start_of_block == True and section != "":
            temp = section
            #print("TURNING FALSE")
            start_of_block = False
        elif start_of_block == False and section !="":
            temp+=f"\n{section}"
        else:
            blocks.append(temp)
            temp = ""
            start_of_block = True
    if temp:
        blocks.append(temp)
    return blocks

def block_to_blocktype(block):
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif re.match(r"^>", block):
        return BlockType.QUOTE
    elif re.match(r"^- ", block):
        return BlockType.U_LIST
    elif re.match(r"^\d+\. ", block):
        return BlockType.O_LIST
    else:
        return BlockType.PARAGRAPH

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
