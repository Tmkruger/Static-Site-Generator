class HTMLNode():
	def __init__(self, tag=None, value=None, children=None, props=None):
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