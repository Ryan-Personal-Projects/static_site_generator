import re

from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Splits text nodes in a list by a given delimiter and assigns a specified text type to the delimited sections.
    Args:
        old_nodes (list): List of TextNode objects to process.
        delimiter (str): The delimiter string used to split the text (e.g., '**' for bold).
        text_type (TextType): The TextType to assign to text found between delimiters.
    Returns:
        list: A new list of TextNode objects, with text split and appropriately typed.
    Raises:
        ValueError: If the number of delimited sections is invalid (i.e., a formatted section is not properly closed).
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        split_nodes = node.text.split(delimiter)
        if  len(split_nodes) % 2 == 0:
            raise ValueError("Invalid markdown: formatted section not closed")
        
        for i in range(0, len(split_nodes)):
            if split_nodes[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(split_nodes[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(split_nodes[i], text_type))
    
    return new_nodes

def extract_markdown_images(text):
    """
    Extracts all Markdown image references from the given text.

    Args:
        text (str): The input string containing Markdown content.

    Returns:
        list of tuple: A list of tuples, each containing the alt text and URL of an image found in the Markdown text.
                       Each tuple is in the form (alt_text, url).
    """
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    """
    Extracts all inline Markdown links from the given text.

    Args:
        text (str): The input string containing Markdown content.

    Returns:
        list of tuple: A list of tuples, each containing the link text and the URL
        (i.e., [(link_text, url), ...]) for each Markdown link found.

    Note:
        - This function ignores image links (i.e., links starting with '!').
        - Only standard inline Markdown links of the form [text](url) are extracted.
    """
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    """
    Splits text nodes containing Markdown image syntax into separate text and image nodes.
    Args:
        old_nodes (list): A list of nodes, where each node is expected to have 'text' and 'text_type' attributes.
    Returns:
        list: A new list of nodes where any Markdown image syntax (e.g., ![alt](src)) in text nodes
              is replaced by separate image nodes (with text_type=IMAGE) and text nodes.
    Raises:
        ValueError: If an image in the text is not properly formatted according to Markdown syntax.
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        node_text = node.text
        image_nodes = extract_markdown_images(node_text)
        if len(image_nodes) == 0:
            new_nodes.append(node)
            continue

        for image in image_nodes:
            node_parts = node_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(node_parts) != 2:
                raise ValueError("Invalid markdown: image not properly formatted")
            if node_parts[0] != "":
                new_nodes.append(TextNode(node_parts[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            node_text = node_parts[1]
        if node_text != "":
            new_nodes.append(TextNode(node_text, TextType.TEXT))
        
    return new_nodes

def split_nodes_link(old_nodes):
    """
    Splits text nodes containing Markdown-style links into separate text and link nodes.
    Args:
        old_nodes (list): A list of nodes, where each node is expected to have 'text' and 'text_type' attributes.
    Returns:
        list: A new list of nodes where any Markdown links in text nodes are split into separate text and link nodes.
    Raises:
        ValueError: If a link is not properly formatted in the input text.
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        node_text = node.text
        link_nodes = extract_markdown_links(node_text)
        if len(link_nodes) == 0:
            new_nodes.append(node)
            continue
            
        for link in link_nodes:
            node_parts = node_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(node_parts) != 2:
                raise ValueError("Invalid markup: link not properly formatted")
            if node_parts[0] != "":
                new_nodes.append(TextNode(node_parts[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            node_text = node_parts[1]
        if node_text != "":
            new_nodes.append(TextNode(node_text, TextType.TEXT))
        
    return new_nodes

def text_to_text_nodes(text):
    """
    Converts a markdown-formatted text string into a list of TextNode objects, 
    splitting the text into nodes based on inline markdown syntax such as bold (**), 
    italic (_), code (`), images, and links.

    Args:
        text (str): The input string containing markdown inline formatting.

    Returns:
        List[TextNode]: A list of TextNode objects representing the parsed segments 
        of the input text, each annotated with its corresponding TextType.
    """
    text_node = TextNode(text, TextType.TEXT)
    text_nodes = [text_node]
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    return text_nodes
