import functools

class HTMLNode():
    """
    Represents a generic HTML node with optional tag, value, children, and properties.
    Attributes:
        tag (str, optional): The HTML tag name (e.g., 'div', 'span'). Defaults to None.
        value (str, optional): The text value or content of the node. Defaults to None.
        children (list['HTMLNode'], optional): List of child HTMLNode objects. Defaults to None.
        props (dict, optional): Dictionary of HTML attributes (e.g., {'class': 'my-class'}). Defaults to None.
    Methods:
        to_html():
            Abstract method to convert the node and its children to an HTML string.
            Must be implemented by subclasses.
        props_to_html():
            Converts the props dictionary to a string of HTML attributes.
            Returns an empty string if no props are set.
        __repr__():
            Returns a string representation of the HTMLNode instance.
    """
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if not self.props:
            return ""
        return functools.reduce(lambda acc, item: acc + f' {item[0]}="{item[1]}"', self.props.items(), "")

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

class LeafNode(HTMLNode):
    """
    LeafNode represents an HTML element that does not have any child nodes.
    Args:
        tag (str): The HTML tag for the element (e.g., 'p', 'span'). If None, only the value is rendered.
        value (str): The text or content of the HTML element.
        props (dict, optional): A dictionary of HTML attributes for the element. Defaults to None.
    Methods:
        to_html():
            Returns the HTML string representation of the node.
            Raises:
                ValueError: If no value is provided for the node.
        __repr__():
            Returns a string representation of the LeafNode instance.
    """
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError("Invalid HTML: no value given")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
 
class ParentNode(HTMLNode):
    """
    ParentNode represents an HTML element that can contain child nodes.

    Attributes:
        tag (str): The HTML tag name for this node (e.g., 'div', 'ul').
        children (list[HTMLNode]): A list of child HTMLNode instances.
        props (dict, optional): A dictionary of HTML attributes for this node.

    Methods:
        to_html():
            Converts the ParentNode and its children into an HTML string.
            Raises:
                ValueError: If the tag or children are not provided.

        __repr__():
            Returns a string representation of the ParentNode instance.
    """
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Invalid HTML: no tag given")
        if self.children == None:
            raise ValueError("Invalid HTML: no children nodes given")

        child_nodes_to_html = ""
        for child in self.children:
            child_nodes_to_html += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{child_nodes_to_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
