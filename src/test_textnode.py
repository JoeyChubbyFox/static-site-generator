import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_different_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    def test_url_property(self):
        # Test with default None url
        node_without_url = TextNode("Link text", TextType.LINK)
        # Test with explicit url
        node_with_url = TextNode("Link text", TextType.LINK, "https://www.example.com")
        # They should be different
        self.assertNotEqual(node_without_url, node_with_url)

    def test_url_default_none(self):
        node = TextNode("Text", TextType.TEXT)
        self.assertEqual(node.url, None)


if __name__ == "__main__":
    unittest.main()
