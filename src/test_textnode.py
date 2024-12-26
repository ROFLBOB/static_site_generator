import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_caps(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        node2 = TextNode("THIS IS A TEXT NODE", TextType.NORMAL)
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode("URL", TextType.NORMAL, "https://google.com")
        node2 = TextNode("URL", TextType.NORMAL, "https://discord.com")
        self.assertNotEqual(node, node2)

    def test_code(self):
        node = TextNode("URL", TextType.NORMAL, "https://google.com")
        node2 = TextNode("URL", TextType.CODE, "https://discord.com")
        self.assertNotEqual(node, node2)
    
    def test_images(self):
        node = TextNode("URL", TextType.NORMAL, "https://google.com")
        node2 = TextNode("URL", TextType.IMAGE, "https://discord.com")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()

