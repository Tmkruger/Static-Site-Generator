class HtmlNode():

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        string = ""
        if self.props != None and type(self.props) == type(dict()):
            for value in self.props:
                string += f' {value}="{self.props[value]}"'
            return string
        else:
            return ValueError

    def __repr__(self):
        return f"HtmlNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HtmlNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag,value)
        self.props = props

    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return self.value
        if self.props:
            prop_string = super().props_to_html()
            #print(f"PROP STRING: {prop_string}")
            return f"<{self.tag}{prop_string}>{self.value}</{self.tag}>"
        else:
            #print(f"NO PROPS")
            return f"<{self.tag}>{self.value}</{self.tag}>"

class ParentNode(HtmlNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag)
        self.children = children
        self.props = props

    def to_html(self):
        string = ""
        if self.tag == None:
            raise ValueError("No Tag found in Node(Required for parent)")
        elif self.children == None:
            raise ValueError("No Children")
        elif self.tag != None and self.children != None and self.children != []:

            for child in self.children:
                string += child.to_html()
            return f'<{self.tag}>{string}</{self.tag}>'
        else:
            raise ValueError("Unknown Error")
