from enum import Enum

from htmlnode import LeafNode

class TextType(Enum):
    """
    An enumeration representing different types of text formatting.

    Attributes:
        TEXT: Represents plain text.
        BOLD: Represents bold formatted text.
        ITALIC: Represents italic formatted text.
        CODE: Represents inline code text.
        LINK: Represents a hyperlink.
        IMAGE: Represents an image.
    """
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    """
    Represents a node of text with an associated type and optional URL.

    Attributes:
        text (str): The textual content of the node.
        text_type (Enum): The type/category of the text (e.g., plain, bold, link).
        url (str, optional): An optional URL associated with the text (used for links).

    Methods:
        __init__(text, text_type, url=None): Initializes a TextNode instance.
        __eq__(other): Checks equality with another TextNode based on attributes.
        __repr__(): Returns a string representation of the TextNode.
    """
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text 
            and self.text_type == other.text_type 
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
        
def text_node_to_html_node(text_node):
    """
    Converts a TextNode object into a corresponding HTML node.

    Args:
        text_node (TextNode): The text node to convert. Must have attributes 'text_type', 'text', and optionally 'url'.

    Returns:
        LeafNode: An HTML node representing the given text node, with appropriate tag and attributes.

    Raises:
        ValueError: If the text_type of the text_node is not recognized.
    """
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
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Invalid text type: {text_node.text_type}")
