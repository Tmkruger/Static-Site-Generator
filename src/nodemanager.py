from textnode import TextNode, TextType
import re

def split_nodes_delmiter(old_nodes, delimiter, text_type):
    converted_nodes = []
    if not old_nodes:
        raise ValueError("No nodes to split")

    if not delimiter:
        # Just return filtered original nodes (only TextType.TEXT are eligible)
        converted_nodes = []
        for node in old_nodes:
            converted_nodes.append(node)
        return converted_nodes

    for node in old_nodes:
        if not isinstance(node, TextNode):
            raise ValueError("Node is not a TextNode")

        if not delimiter:
            if len(old_nodes) > 1:
                converted_nodes.append(node)
            else:
                return old_nodes
        text = node.text
        re_delimiter = re.escape(delimiter)
        pattern = pattern = rf'(?<!{re_delimiter}){re_delimiter}(?!{re_delimiter})(.+?)(?<!{re_delimiter}){re_delimiter}(?!{re_delimiter})'
        matches = list(re.finditer(pattern, text))
        if not matches:
            converted_nodes.append(node)
            continue

        last_end = 0
        for match in matches:
            # Add unstyled text before the delimiter
            if match.start() > last_end:
                unstyled_text = text[last_end:match.start()]
                if unstyled_text:
                    converted_nodes.append(TextNode(unstyled_text, TextType.TEXT))

            # Add styled (delimited) text
            styled_text = match.group(1)
            converted_nodes.append(TextNode(styled_text, text_type))

            last_end = match.end()

        # Add remaining unstyled text after the last match
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
        #print(f"MATCHES: {matches}")
        for match in matches:
            #print(f"TEXT: {text}")
            #print(f"MATCH: {match}")
            image_alt = match[0]
            image_link = match[1]
            sections = text.split(f"![{image_alt}]({image_link})", 1)
            for section in sections:
                print(f"SECTION! : {section}!!!")
                if not extract_markdown_images(section) and section != "":
                    converted_nodes.append(TextNode(section, TextType.TEXT))
                if TextNode(image_alt, TextType.IMAGE, image_link) not in converted_nodes:
                    converted_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            text = sections[len(sections)-1]
            print(f"SECTIONS: {sections}")
            # Add styled (delimited) text
    print(f"CONVERTED_NODES : {converted_nodes}")
    return converted_nodes

def split_nodes_link(old_nodes):
    pass
