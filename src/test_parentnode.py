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





class TestParentNode(unittest.TestCase):
    def test_eq(self):
        print("Testing the test_eq function:")
        return self.assertNotEqual(paragraph_node2, paragraph_node)
    
    def test_to_html(self):
        print("Testing the test_to_html function")
        print(paragraph_node.to_html())

    def test_printing(self):
        print("Testing the test_printing function:")
        print(paragraph_node)

    def test_nested_parent_nodes(self):
        print(ParentNode("div", [ParentNode("p", [LeafNode("this is a paragraph",None,None)], {"font-size":"18px"}),LeafNode("Click Here","input",{"background-color":"purple"})], {"color":"red", "text-decoration":"underline"}).to_html())
        



if __name__ == "__main__":
    unittest.main()

