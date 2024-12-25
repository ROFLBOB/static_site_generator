import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

#HTMLNode(tag(string), children(list), props=None(dict))

paragraph_node = ParentNode(
    "p", 
    [
        LeafNode(None, "This is a "), 
        ParentNode("a", [LeafNode(None, "link")], {"href": "https://example.com"})
    ]
)
paragraph_node2 = ParentNode(
    "p", 
    [
        LeafNode(None, "This is another "), 
        ParentNode("a", [LeafNode(None, "link")], {"href": "https://example.com"})
    ]
)





class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        print("Testing the test_eq function:")
        return self.assertNotEqual(paragraph_node2, paragraph_node)
    
    def test_to_html(self):
        print("Testing the test_to_html function")
        print(paragraph_node.to_html())

    def test_printing(self):
        print("Testing the test_printing function:")
        print(paragraph_node)



if __name__ == "__main__":
    unittest.main()

