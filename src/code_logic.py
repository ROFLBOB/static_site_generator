from textnode import TextNode, TextType, text_node_to_html_node

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    #takes a list of old nodes, a delimiter, and texttype. It should return a new list of nodes where any
    #text teype nodes in the input list are (potentially) split into multiple nodes based on the syntax
    
    #search for the delimiter in each node
    text_node_list = []
    for node in old_nodes:

        if node.text_type is TextType.TEXT:
            
            current_text = node.text
            while True:
                start_pos = current_text.find(delimiter)
                if start_pos == -1:
                    #no more delimiters, add remaining text as a node
                    if current_text:
                        text_node_list.append(TextNode(current_text,TextType.TEXT))
                    break
                end_pos = current_text.find(delimiter, start_pos+len(delimiter))              
                if end_pos == -1:
                    raise Exception(f"Invalid syntax, no closing delimiter found. Delimiter: {delimiter}")
                
                #add text before the delimiter
                if start_pos > 0:
                    text_node_list.append(TextNode(current_text[0:start_pos],TextType.TEXT,None))
                
                #add delimited text
                text_node_list.append(TextNode(current_text[start_pos+len(delimiter):end_pos],text_type))

                current_text = current_text[end_pos + len(delimiter):]
                
        
        else:
            text_node_list.append(node)

    return text_node_list


old_nodes = [TextNode("This is text with a `code block` word", TextType.TEXT),TextNode("more `code words`", TextType.TEXT),TextNode("this block has `multiple code blocks` in it. See, `here` is another `one`.",TextType.TEXT)]

print(split_nodes_delimiter(old_nodes,"`", TextType.CODE))