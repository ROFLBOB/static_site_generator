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
        for key, value in self.props.items():
            prop_string += f' {key}="{value}"' 
        print(f"Converting prop item to html: {prop_string}")
        return prop_string
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, props=None):
        #run the constructor from HTMLNode, no children and value should be required
        super().__init__(value, tag, None, props) 
    
    def to_html(self):
        #this function renders the leaf node as an html string by returning a string
        if self.value is None:
            #all leaf nodes must have a value
            try: 
                raise ValueError
            except ValueError as e:
                print(f"There is no value in {self}.")
        if self.tag is None:
            #return raw text
            return self.value
        if self.props is None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        props_string = self.props_to_html()
        html_string = f"<{self.tag} {props_string}>{self.value}</{self.tag}>"
        return html_string
    
    def __repr__(self):
        return f"LeafNode({self.value}, {self.tag}, {self.props})"
