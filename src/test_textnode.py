import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_dif_urls(self):
        node1 = TextNode("I'm a test", TextType.IMAGE, "www.imagebase.com")
        node2 = TextNode("I'm a test", TextType.IMAGE, "www.google.com")
        self.assertNotEqual(node1, node2)

    def test_empty_urls(self):
        node1 = TextNode("I'm a test", TextType.IMAGE, "")
        node2 = TextNode("I'm a test", TextType.IMAGE)
        self.assertNotEqual(node1, node2)
    
    def test_dif_types(self):
        node1 = TextNode("I'm a test", TextType.BOLD)
        node2 = TextNode("I'm a test", TextType.ITALIC)
        self.assertNotEqual(node1, node2)
        
    def test_dif_text(self):
        node1 = TextNode("I'm an NOT a test", TextType.BOLD)
        node2 = TextNode("I'm a test", TextType.BOLD)
        self.assertNotEqual(node1, node2)
    
    def test_dif_text_cases(self):
        node1 = TextNode("I'M A TEST", TextType.BOLD)
        node2 = TextNode("i'm a test", TextType.BOLD)
        self.assertNotEqual(node1, node2)
    
    def test_repr(self):
        node = TextNode("I'm a test", TextType.IMAGE, "www.google.com")
        self.assertEqual(repr(node), "TextNode(I'm a test, image, www.google.com)")
    
class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

if __name__ == "__main__":
    unittest.main()
