
from textnode import TextNode, TextType
from test_textnode import TestTextNode

def main():
    node = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
    print(node)

main()