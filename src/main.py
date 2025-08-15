from textnode import TextNode , TextType
from htmlnode import HtmlNode, LeafNode, ParentNode
from nodemanager import split_nodes_delmiter
from markdown_to_html import *


def main():
    markdown = """
This is **bolded** paragraph

This is another paragraph with *italic* text and code: `print("Hello World")` here
This is _the_ same paragraph on a new line, ending **bold**

```
This is text that _should_ remain
the **same** even with inline stuff
```

- This is a list
- with items
"""
    markdown_to_html_node(markdown)



main()
