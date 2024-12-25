import unittest

from htmlnode import HTMLNode, LeafNode

#HTMLNode(value, tag=None, props)

test_node = HTMLNode("span", "this is spanned red text >_>", None, {"line_weight":600,"color":"red"})
list_of_html_nodes = [HTMLNode(None,"A word",None,None),HTMLNode(None,"of the wise",None,None),HTMLNode(None,"Dont eat yellow snow",None,None)]
leaf1 = LeafNode("p", "This is a paragraph of text.")
leaf2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})



class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        print("Testing the test_eq function:")
        return self.assertNotEqual(leaf1, leaf2)
    
    def test_to_html(self):
        print("Testing the test_to_html function")
        print(leaf1.to_html())
        print(leaf2.to_html())

    def test_printing(self):
        print("Testing the test_printing function:")
        print(leaf1)
        print(leaf2)



if __name__ == "__main__":
    unittest.main()

