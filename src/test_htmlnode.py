import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHtmlNode(unittest.TestCase):
    def test_props_to_html_1(self):
        node = HTMLNode("a", "click here!", None, {"href": "www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="www.google.com"')

    def test_props_to_html_2(self):
        node = HTMLNode("a", "click here!", None, {"href": "www.google.com", "class": "anchor_class"})
        self.assertEqual(node.props_to_html(), ' href="www.google.com" class="anchor_class"')

    def test_props_to_html_3(self):
        node = HTMLNode("a", "click here!", None, None)
        self.assertEqual(node.props_to_html(), '')

    def test_repr(self):
        node = HTMLNode("a", "click here!", None, {"href": "www.google.com"})
        self.assertEqual(repr(node), "HTMLNode(a, click here!, children: None, {'href': 'www.google.com'})")
    
    def test_values(self):
        node = HTMLNode("div", "I'm a div!")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "I'm a div!")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "www.boot.dev"})
        self.assertEqual(node.to_html(), '<a href="www.boot.dev">Click me!</a>')
    
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Apply Here")
        self.assertEqual(node.to_html(), "Apply Here")
    
    def test_repr_leaf_node(self):
        node = LeafNode("b", "Apply Here")
        self.assertEqual(repr(node), "LeafNode(b, Apply Here, None)")
    
    def test_to_html_with_children(self):
        child1_node = LeafNode("span", "child")
        child2_node = LeafNode("b", "Click Me!")
        child3_node = LeafNode(None, "No tags!")
        parent_node = ParentNode("div", [child1_node, child2_node, child3_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><b>Click Me!</b>No tags!</div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_multiple_grandchildren(self):
        grandchild1_1_node = LeafNode("b", "grandchild1")
        grandchild1_2_node = LeafNode("i", "grandchild2")
        child1_node = ParentNode("span", [grandchild1_1_node, grandchild1_2_node])
        grandchild2_1_node = LeafNode(None, "No tag")
        grandchild2_2_node = LeafNode("i", "nesting is fun")
        child2_node = ParentNode("div", [grandchild2_1_node, grandchild2_2_node])
        parent_node = ParentNode("div", [child1_node, child2_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild1</b><i>grandchild2</i></span><div>No tag<i>nesting is fun</i></div></div>",
        )
    
    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(
            parent_node.to_html(),
            "<div></div>"
        )
    
    def test_to_html_parent_with_children_with_no_children(self):
        child_node = ParentNode("div", [])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><div></div></div>"
        )

if __name__ == "__main__":
    unittest.main()