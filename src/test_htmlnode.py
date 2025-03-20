import unittest
from htmlnode import HTMLNode, LeafNode  # Adjust the import based on the actual file name containing LeafNode
# Add ParentNode import
from htmlnode import ParentNode  # Adjust if needed based on actual location
from textnode import TextNode, TextType
from markdown_parser import text_node_to_html_node

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        # Test with no props
        node = HTMLNode("p", "Hello, world!")
        self.assertEqual(node.props_to_html(), "")
    
    def test_props_to_html_single_prop(self):
        # Test with a single prop
        node = HTMLNode("a", "Click me!", props={"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')
    
    def test_props_to_html_multiple_props(self):
        # Test with multiple props
        node = HTMLNode(
            "a", 
            "Click me!", 
            props={
                "href": "https://example.com", 
                "target": "_blank",
                "class": "button"
            }
        )
        # Since dictionary order isn't guaranteed, we need to check each attribute is present
        html_props = node.props_to_html()
        self.assertIn(' href="https://example.com"', html_props)
        self.assertIn(' target="_blank"', html_props)
        self.assertIn(' class="button"', html_props)
        # Also verify the total length to ensure nothing extra was added
        expected_length = len(' href="https://example.com"') + len(' target="_blank"') + len(' class="button"')
        self.assertEqual(len(html_props), expected_length)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just some text")
        self.assertEqual(node.to_html(), "Just some text")

    def test_leaf_to_html_no_value(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None).to_html()

    # ParentNode tests
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_parent_no_tag(self):
        # Test that ValueError is raised if tag is None
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("p", "test")]).to_html()
    
    def test_parent_no_children(self):
        # Test that ValueError is raised if children is None
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()

    def test_parent_with_multiple_children(self):
        # Test with multiple children at the same level
        parent = ParentNode("ul", [
            LeafNode("li", "Item 1"),
            LeafNode("li", "Item 2"),
            LeafNode("li", "Item 3")
        ])
        self.assertEqual(
            parent.to_html(),
            "<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>"
        )

    def test_parent_with_props(self):
        # Test a parent node with properties
        parent = ParentNode("div", [LeafNode("span", "Hello")], {"class": "container", "id": "main"})
        html = parent.to_html()
        self.assertIn('<div class="container"', html)
        self.assertIn(' id="main"', html)
        self.assertIn('<span>Hello</span>', html)
        self.assertTrue(html.endswith('</div>'))

    def test_complex_nesting(self):
        # Test a complex nested structure with multiple levels and siblings
        form = ParentNode("form", [
            ParentNode("div", [
                LeafNode("label", "Username:"),
                LeafNode("input", "", {"type": "text", "name": "username"})  # Changed None to ""
            ], {"class": "form-group"}),
            ParentNode("div", [
                LeafNode("label", "Password:"),
                LeafNode("input", "", {"type": "password", "name": "password"})  # Changed None to ""
            ], {"class": "form-group"}),
            LeafNode("input", "", {"type": "submit", "value": "Login"})  # Changed None to ""
        ], {"action": "/login", "method": "post"})
    
        html = form.to_html()
        # Check form attributes
        self.assertIn('<form action="/login"', html)
        self.assertIn(' method="post"', html)
        # Check div elements with class
        self.assertIn('<div class="form-group">', html)
        # Check label and input elements
        self.assertIn('<label>Username:</label>', html)
        self.assertIn('<input type="text" name="username">', html)
        self.assertIn('<label>Password:</label>', html)
        self.assertIn('<input type="password" name="password">', html)
        self.assertIn('<input type="submit" value="Login">', html)
        # Check closing tags
        self.assertIn('</div>', html)
        self.assertIn('</form>', html)

    def test_empty_children_list(self):
        # Test with an empty children list (should work, but render just the parent tags)
        parent = ParentNode("div", [])
        self.assertEqual(parent.to_html(), "<div></div>")

    def test_parent_with_text_and_elements(self):
        # Test mixing text nodes and element nodes
        parent = ParentNode("p", [
            LeafNode(None, "This is "),
            LeafNode("strong", "important"),
            LeafNode(None, " text.")
        ])
        self.assertEqual(
            parent.to_html(),
            "<p>This is <strong>important</strong> text.</p>"
        )

    def test_nested_parent_with_no_leaf_children(self):
        # Test parent nodes nested inside other parent nodes with no leaf children
        inner = ParentNode("div", [])
        outer = ParentNode("section", [inner])
        self.assertEqual(outer.to_html(), "<section><div></div></section>")

    def test_parent_with_mixed_child_types(self):
        # Test with a mix of LeafNode and ParentNode children
        parent = ParentNode("article", [
            LeafNode("h1", "Article Title"),
                ParentNode("div", [
                LeafNode("p", "Paragraph 1"),
                LeafNode("p", "Paragraph 2")
            ]),
            LeafNode("footer", "Copyright 2023")
        ])
        self.assertEqual(
            parent.to_html(),
            "<article><h1>Article Title</h1><div><p>Paragraph 1</p><p>Paragraph 2</p></div><footer>Copyright 2023</footer></article>"
        )

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        # Already provided in the assignment
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
    
    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
    
    def test_code(self):
        node = TextNode("Code snippet", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code snippet")

    def test_link(self):
        node = TextNode("Click me", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me")
        self.assertEqual(html_node.props["href"], "https://example.com")

    def test_image(self):
        node = TextNode("Alt text for image", TextType.IMAGE, "https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "https://example.com/image.png")
        self.assertEqual(html_node.props["alt"], "Alt text for image")

    def test_invalid_type(self):
        # Test with an invalid TextType to ensure it raises an exception
        node = TextNode("Invalid type", "not_a_valid_type")
        with self.assertRaises(Exception):
            text_node_to_html_node(node)

if __name__ == "__main__":
    unittest.main()
