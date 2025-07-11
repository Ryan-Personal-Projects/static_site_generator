from enum import Enum
import re

from htmlnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from markdown_inline import text_to_text_nodes

class BlockType(Enum):
    """
    An enumeration representing the different types of blocks that can appear in a markdown document.

    Attributes:
        PARAGRAPH: Represents a standard paragraph block.
        HEADING: Represents a heading block.
        CODE: Represents a block of code.
        QUOTE: Represents a blockquote.
        UNORDERED_LIST: Represents an unordered list.
        ORDERED_LIST: Represents an ordered (numbered) list.
    """
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    """
    Splits a markdown string into a list of blocks, separated by double newlines.

    Each block is stripped of leading and trailing whitespace, and empty blocks are excluded from the result.

    Args:
        markdown (str): The markdown text to split into blocks.

    Returns:
        list of str: A list of non-empty, stripped markdown blocks.
    """
    return list(filter(lambda x: x != "", list(map(lambda x: x.strip(), markdown.split("\n\n")))))

def extract_title(markdown):
    """
    Extracts the title from a Markdown string by retrieving the first block as an H1 header.

    Args:
        markdown (str): The Markdown content as a string.

    Returns:
        str: The title extracted from the H1 header.

    Raises:
        ValueError: If the Markdown does not begin with an H1 header (i.e., a line starting with '# ').
    """
    blocks = markdown_to_blocks(markdown)
    header = blocks[0]
    if not header.startswith("# "):
        raise ValueError("Invalid Markdown: markdown must begin with h1 header")
    return header[2:]

def block_to_block_type(markdown_block):
    """
    Determines the type of a given Markdown block.
    This function analyzes a block of Markdown text and returns its corresponding BlockType
    (e.g., heading, code, quote, unordered list, ordered list, or paragraph) based on pattern matching.
    Args:
        markdown_block (str): The Markdown block to classify.
    Returns:
        BlockType: The type of the Markdown block, such as HEADING, CODE, QUOTE, UNORDERED_LIST,
                   ORDERED_LIST, or PARAGRAPH.
    Notes:
        - Multi-line patterns (e.g., headings, code blocks) are checked first if the block starts
          with '#' or '`'.
        - Single-line patterns (e.g., quotes, lists) are checked for all lines in the block.
        - Ordered lists require that each line starts with an incrementing number.
        - If no pattern matches, the block is classified as a PARAGRAPH.
    """
    multi_line_md_patterns = [
        (BlockType.HEADING, re.compile(r"^(#{1,6})\s+(.+)$")),
        (BlockType.CODE, re.compile(r"^```[\s\S]*?```$", re.MULTILINE | re.DOTALL))
    ]

    single_line_md_patterns = [
        (BlockType.QUOTE, re.compile(r"^>.*$")),
        (BlockType.UNORDERED_LIST, re.compile(r"^- .+$")),
        (BlockType.ORDERED_LIST, re.compile(r"^(\d+)\. .+"))
    ]

    if markdown_block[0] in ("#", "`"):
        for block_type, pattern in multi_line_md_patterns:
            if pattern.match(markdown_block):
                return block_type
    else:
        lines = [line for line in markdown_block.splitlines() if line.strip()]
        for block_type, pattern in single_line_md_patterns:
            if block_type == BlockType.ORDERED_LIST:
                if all((match := pattern.match(line)) and int(match.group(1)) == i for i, line in enumerate(lines, start=1)):
                    return block_type
            else:
                if all(pattern.match(line) for line in lines):
                    return block_type

    
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    """
    Converts a markdown string into a ParentNode representing the HTML structure.

    Args:
        markdown (str): The markdown text to be converted.

    Returns:
        ParentNode: A ParentNode object with tag "div" containing the HTML nodes generated from the markdown blocks.
    """
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    """
    Converts a markdown block to its corresponding HTML node representation.

    Args:
        block: The markdown block to convert. The block should be a data structure
            that can be classified into one of the supported block types.

    Returns:
        An HTML node representing the given markdown block.

    Raises:
        ValueError: If the block type is invalid or unsupported.
    """
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    """
    Converts a text string into a list of HTML node children.

    This function splits the input text into text nodes, converts each text node
    into an HTML node, and returns a list of these HTML nodes.

    Args:
        text (str): The input text to be converted.

    Returns:
        list: A list of HTML node objects generated from the input text.
    """
    text_nodes = text_to_text_nodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    """
    Converts a block of text representing a paragraph into a ParentNode representing an HTML <p> element.

    Args:
        block (str): The paragraph text, potentially spanning multiple lines.

    Returns:
        ParentNode: An HTML node representing the paragraph, with its content parsed into child nodes.
    """
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    """
    Converts a Markdown heading block to an HTML node.

    Args:
        block (str): A string representing a Markdown heading (e.g., "# Heading 1").

    Returns:
        ParentNode: An HTML node representing the heading, with the appropriate level and children.

    Raises:
        ValueError: If the heading level is invalid (e.g., no space after the '#' characters or block too short).
    """
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    """
    Converts a Markdown code block string into a nested HTML node structure.

    Args:
        block (str): The Markdown code block string, expected to start and end with triple backticks (```).

    Returns:
        ParentNode: An HTML node representing the code block, structured as <pre><code>...</code></pre>.

    Raises:
        ValueError: If the input string does not start and end with triple backticks.
    """
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    """
    Converts a block of ordered list markdown text into an HTML node representation.

    Args:
        block (str): A string containing the markdown for an ordered list, where each item is on a new line and starts with a number and a period (e.g., "1. Item").

    Returns:
        ParentNode: An HTML node representing the ordered list (<ol>) with child <li> nodes for each list item.
    """
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    """
    Converts a Markdown unordered list block into an HTML node representation.

    Args:
        block (str): A string containing the Markdown unordered list, where each item is on a new line and starts with a list marker (e.g., '- ').

    Returns:
        ParentNode: An HTML node representing the unordered list (<ul>) with each item as a child <li> node.
    """
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    """
    Converts a Markdown blockquote block into a ParentNode representing an HTML <blockquote> element.

    Args:
        block (str): A string containing the Markdown blockquote, where each line starts with '>'.

    Returns:
        ParentNode: An HTML node representing the <blockquote> element with its children parsed from the blockquote content.

    Raises:
        ValueError: If any line in the block does not start with '>'.
    """
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
