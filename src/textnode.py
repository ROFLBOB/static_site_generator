from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "normal"
    BOLD = "bold"
    ITALIC = "italics"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text == other.text:
            if self.text_type == other.text_type:
                if self.url == other.url:
                    return True
        return False
    
    def __repr__(self):
        return f"TextNode('{self.text}', {self.text_type}, {self.url})\n"
    
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(text_node.text,None,None)
        case TextType.BOLD:
            return LeafNode(text_node.text, "b", None)
        case TextType.ITALIC:
            return LeafNode(text_node.text, "i", None)
        case TextType.CODE:
            return LeafNode(text_node.text, "code", None)
        case TextType.LINK:
            return LeafNode(text_node.text, "a", {"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode(None,"img", {"src":text_node.url,"alt":"Alt text"})
        case _:
            return "Not a valid text type."
    

'''def test_text_node_to_html_node():
    print(text_node_to_html_node(TextNode("normal text",TextType.TEXT, None)).to_html())
    print(text_node_to_html_node(TextNode("bold text",TextType.BOLD, None)).to_html())
    print(text_node_to_html_node(TextNode("italic text",TextType.ITALIC, None)).to_html())
    print(text_node_to_html_node(TextNode("coded text",TextType.CODE, None)).to_html())
    print(text_node_to_html_node(TextNode("a link to googs",TextType.LINK, "https://google.com")).to_html())
    print(text_node_to_html_node(TextNode("an image",TextType.IMAGE, None)))'''