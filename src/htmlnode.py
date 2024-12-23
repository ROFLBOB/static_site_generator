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
            prop_string += f' {key}="{value}" ' 
        print(f"Converting prop item to html: {prop_string}")
        return prop_string
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"