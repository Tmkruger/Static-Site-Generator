from htmlnode import HtmlNode, LeafNode, ParentNode
from textnode import TextNode, TextType

def split_nodes_delmiter(old_nodes, delimiter, text_type):
    converted_nodes = []
    
    if len(old_nodes) == 0:
        raise ValueError("No nodes to split")
    # Iterate through each node in the old_nodes list
    for node in old_nodes:
        if isinstance(node,TextNode):
            if node.text.find(delimiter) != -1:
                # Check if the Delimiter is closed
                index1 = node.text.find(delimiter)
                section_after_delimiter = node.text[index1:]
                if section_after_delimiter.find(delimiter) == -1:
                    raise ValueError("Unclosed delimiter found in text node")
                else:
                    # Split the text node by the delimiter
                    parts = node.text.split(delimiter)
                    # Create new TextNodes for each part
                    before_delimiter = (TextNode(parts[0], TextType.TEXT))
                    delim_section = (TextNode(parts[1], text_type))
                    after_delimiter = (TextNode(parts[2], TextType.TEXT))
                    # Check if len is 1 to avoid nested lists when only one node is passed
                    # Than either append to converted_nodes and move continue loop or return the converted node
                    if len(old_nodes) == 1:
                        return [before_delimiter, delim_section, after_delimiter]
                    else:
                        converted_nodes.append([before_delimiter, delim_section, after_delimiter])
            else:
                # Means no delimiter found, so just append/return the original node

                # Check if len is 1 to avoid nested lists when only one node is passed
                if len(old_nodes) == 1:
                    return [node]
                else:
                    converted_nodes.append(node)
        else:
            raise ValueError("Node is not a TextNode")
    
    return converted_nodes