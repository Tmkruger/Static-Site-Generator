class HTMLNode():
	def __init__(self, value=None,tag=None, children=None, props=None):
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props

	def __eq__(self, other):
		return ((self.tag == other.tag) 
			and (self.value == other.value)
			and (self.children == other.children)
			and (self.props == other.props))

	def to_html(self):
		raise NotImplementedError

	def props_to_html(self):
		list = []
		items = self.props.items()
		for item in items:
			list.append(f"{item[0]}{item[1]}")
		return (" ".join(list))
	def __repr__(self):
		content = HTMLNode("h1", "This is a Header")
		return f"HTMLNODE({content})"

class LeafNode(HTMLNode):
	def __init__(self, value, tag=None, props=None):
		super().__init__()
		self.value = value
		self.tag = tag
		self.props = props

	def to_html:
		if self.value == None:
			raise ValueError("All leaf nodes must have a value")
		if self.tag == None:
			return self.value
		else:
			if self.tag == "a":
				url_tag_value = list(self.props.items())
				return f"<{self.tag} {url_tag_value[0]}={url_tag_value[1]}>{self.value}</{self.tag}>"
			else:
				return f"<{self.tag}>{self.value}</{self.tag}>"