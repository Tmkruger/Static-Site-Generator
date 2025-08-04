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
