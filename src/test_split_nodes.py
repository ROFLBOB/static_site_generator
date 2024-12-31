import unittest

from textnode import TextNode, TextType
from code_logic import *


class TestSplitNodes(unittest.TestCase):
    def test_single_link(self):
        node = TextNode("Visit [Boot.dev](https://www.boot.dev) for coding courses.", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("Visit ", TextType.TEXT),
            TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" for coding courses.", TextType.TEXT)
        ]
        assert result == expected, f"Expected {expected}, but got {result}"


    def test_multiple_links(self):
        node = TextNode("Learn [Boot.dev](https://www.boot.dev) and watch [YouTube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("Learn ", TextType.TEXT),
            TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and watch ", TextType.TEXT),
            TextNode("YouTube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
        ]
        assert result == expected, f"Expected {expected}, but got {result}"


    def test_no_links(self):
        node = TextNode("Just a simple text node.", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [node]  # As no links exist, it should return the original node
        assert result == expected, f"Expected {expected}, but got {result}"

if __name__ == "__main__":
    unittest.main()

