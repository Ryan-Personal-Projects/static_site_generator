import unittest
from markdown_block import (
    markdown_to_blocks, 
    block_to_block_type,
    markdown_to_html_node, 
    extract_title,
    BlockType
)

class TestMarkdownBlock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_excess_newlines(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line with an ![image](www.google.com)           




- This is a list
- with items

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line with an ![image](www.google.com)",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "###### heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "1. list\n3. items"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "> quote\nmore quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "- list\n-items"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "```\ncode\n``"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = """
- Item 1
- Item 2
- Item 3
    """
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )   

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_unordered_list(self):
            md = """
- Item 1
- Item 2
- Item 3
    """
            node = markdown_to_html_node(md)
            html = node.to_html()
            print(html)
            self.assertEqual(
                html,
                "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>",
            )

    def test_ordered_list(self):
            md = """
1. First
2. Second
3. Third
    """
            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><ol><li>First</li><li>Second</li><li>Third</li></ol></div>",
            )

    def test_quote_block(self):
            md = """
> This is a quote
> that spans lines
    """
            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><blockquote>This is a quote that spans lines</blockquote></div>",
            )

    def test_heading(self):
            md = """
    # Heading 1

    ## Heading 2

    ###### Heading 6
    """
            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><h1>Heading 1</h1><h2>Heading 2</h2><h6>Heading 6</h6></div>",
            )
    
    def test_extract_title(self):
            md = """
    # Heading 1

    ## Heading 2

    ###### Heading 6
    """
            header = extract_title(md)
            self.assertEqual(
                  header,
                  "Heading 1"
            )

    def test_extract_title_double(self):
        actual = extract_title(
            """
# This is a title

# This is a second title that should be ignored
"""
        )
        self.assertEqual(actual, "This is a title")

    def test_extract_title_long(self):
        actual = extract_title(
            """
# title

this is a bunch

of text

- and
- a
- list
"""
        )
        self.assertEqual(actual, "title")

    def test_none(self):
        try:
            extract_title(
                """
no title
"""
            )
            self.fail("Should have raised an exception")
        except ValueError as e:
            self.assertEqual(str(e), "Invalid Markdown: markdown must begin with h1 header")
            
if __name__ == "__main__":
    unittest.main()