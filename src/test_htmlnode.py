import unittest

from htmlnode import HTMLNode

#HTMLNode(tag, value, children, props)

test_node = HTMLNode("span", "this is spanned red text >_>", None, {"line_weight":600,"color":"red"})
list_of_html_nodes = [HTMLNode(None,"A word",None,None),HTMLNode(None,"of the wise",None,None),HTMLNode(None,"Dont eat yellow snow",None,None)]

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        
        
        node = HTMLNode("a", "Hello world", list_of_html_nodes, test_node)
        node2 = HTMLNode("b", "Hellow orld", None, None)
        self.assertNotEqual(node, node2)
    
    def test_to_html(self):
        print(test_node.to_html())

    def test_props_to_html(self):
        print("Not implemented. Running will raise an error.")

    def test_nones(self):
        list_of_html_nodes = [HTMLNode(None,"A word",None,None),HTMLNode(None,"of the wise",None,None),HTMLNode(None,"Dont eat yellow snow",None,None)]
        node = HTMLNode("a", "Hello world", list_of_html_nodes, None)
        node2 = HTMLNode("b", "Hellow orld", None, None)
        node3 = HTMLNode("c")
        node4 = HTMLNode()
        print(node)
        print(node2)
        print(node3)
        print(node4)
    



if __name__ == "__main__":
    unittest.main()

