from enum import Enum

class TextType (Enum):
	NORMAL = "normal"
	BOLD = "bold"
	ITALIC = "italic"
	CODE = "code"
	LINKS = "link"
	IMAGES = "image"

class TextNode():
		def __init__(self, text_cont, text_type, url=None):
			self.text_type = text_type
			self.text_cont = text_cont
			self.url = url
		def __eq__(self, other):
			return ((self.text_type == other.text_type) 
			and (self.text_cont == other.text_cont) 
			and (self.url == other.url))
			
				
		def __repr__(self):
			content = f"{self.text_cont}, {self.text_type.value}, {self.url}"
			return f"TextNode({content})"