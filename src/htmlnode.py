from textnode import TextType, TextNode

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        try:
            raise NotImplementedError
        except NotImplementedError as e:
            print("Not implemented yet.")

    
    def props_to_html(self):
        #convert the props dict to a string
        #eg href="https://google.com" target="__blank"
        prop_string = ""
        if self.props is None:
            return prop_string
        for key, value in self.props.items():
            prop_string += f' {key}="{value}"' 
        print(f"Converting prop item to html: {prop_string}")
        return prop_string
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, props=None):
        #run the constructor from HTMLNode, no children and value should be required
        super().__init__(tag, value, None, props) 
    
    def to_html(self):
        #this function renders the leaf node as an html string by returning a string
        if self.value is None:
            #all leaf nodes must have a value
            try: 
                raise ValueError
            except ValueError as e:
                print(f"There is no value in {self}: {e}")
        if self.tag is None:
            #return raw text
            return self.value
        if self.props is None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        props_string = self.props_to_html()
        html_string = f"<{self.tag}{props_string}>{self.value}</{self.tag}>"
        return html_string
    
    def __repr__(self):
        return f"LeafNode({self.value}, {self.tag}, {self.props})"

class ParentNode(HTMLNode):
    #any HTML node that has children is a parent node
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        
    def to_html(self):
        def generate_html(node):
            #base case: there's no more children (list of nodes)    
            if isinstance(node, LeafNode):
                return node.to_html() 
            html_string = ""
            for element in node.children:
                #for each element in the child list, run generate_html(node) on it
                html_string += generate_html(element)
            return f"<{node.tag}{node.props_to_html()}>{html_string}</{node.tag}>"
        
        if self.tag is None:
            raise ValueError(f"{self} has an invalid tag")
        if self.children is None:
            raise ValueError(f"{self} node must have children.")
        return generate_html(self)

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(text_node.text,None,None)
        case TextType.BOLD:
            return LeafNode(text_node.text, "strong", None)
        case TextType.ITALIC:
            return LeafNode(text_node.text, "em", None)
        case TextType.CODE:
            return LeafNode(text_node.text, "code", None)
        case TextType.LINK:
            return LeafNode(text_node.text, "a", {"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode(None,"img", {"src":text_node.url,"alt":"Alt text"})
        case _:
            return "Not a valid text type."
        
#TextNode(text, type, url)

print(TextNode("normal text",TextType.TEXT, None))

def test_text_node_to_html_node():
    print(text_node_to_html_node(TextNode("normal text",TextType.TEXT, None)))
    print(text_node_to_html_node(TextNode("bold text",TextType.BOLD, None)))
    print(text_node_to_html_node(TextNode("italic text",TextType.ITALIC, None)))
    print(text_node_to_html_node(TextNode("coded text",TextType.CODE, None)))
    print(text_node_to_html_node(TextNode("a link to googs",TextType.LINK, "https://google.com")))
    print(text_node_to_html_node(TextNode("an image",TextType.IMAGE, None)))

test_text_node_to_html_node()