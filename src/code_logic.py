from textnode import TextNode, TextType, text_node_to_html_node
import re

#split_nodes_delimiter: takes a list of text nodes and splits it according to the delimiter.
def split_nodes_delimiter(old_nodes, delimiter, text_type):
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
                    raise ValueError(f"Invalid syntax, no closing delimiter found. Delimiter: {delimiter}")
                #add text before the delimiter
                if start_pos > 0:
                    text_node_list.append(TextNode(current_text[0:start_pos],TextType.TEXT,None))
                #add delimited text
                text_node_list.append(TextNode(current_text[start_pos+len(delimiter):end_pos],text_type))
                current_text = current_text[end_pos + len(delimiter):]
        else:
            text_node_list.append(node)
    return text_node_list

def extract_markdown_images(text):
    #takes raw markdown text and returns a list of tuples (alt text, URL)
    matched_images = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    #matched images = "[![rick rolll](https://i.imgur.com/aKa0qIh.gif)]"
    matched_tuples = []
    for match in matched_images:
        matched_tuples.append(tuple(match))
    return matched_tuples

def extract_markdown_links(text):
    #takes raw md text and returns a list of tuples - [to boot dev](https://boot.dev) - [(anchor_text, url)]
    matched_links = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    matched_tuples = []
    for match in matched_links:
        matched_tuples.append(tuple(match))
    return matched_tuples



#node = TextNode(
    #"This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    #TextType.TEXT,
#)
#new_nodes = split_nodes_link([node])
# [
#     TextNode("This is text with a link ", TextType.TEXT),
#     TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
#     TextNode(" and ", TextType.TEXT),
#     TextNode(
#         "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
#     ),
# ]


def split_nodes_link(old_nodes):
    #takes a list of nodes and identify the links in them, and return a list of all the nodes with the proper text type.
    #image syntax: ![alt text](url_here)
    text_node_list = []
    for node in old_nodes:
        #check if the extract markdown links function created anything
        links = extract_markdown_links(old_nodes)
        if len(links) == 0:
            #no links, just add the text node to the list as normal
            if len(node.text) > 0:
                text_node_list.append(node)
            continue

        node_text = node.text

        #there is at least one link and it's set up as a list of tuples [(alt text,url)(alt text,url)]. go through each tuple in the list
        #and save the alt. We want to  and append it as a new link to the text node
        for link_details in links:
            this_node_components = []
            alt = link_details[0]
            url = link_details[1]
            #split the current node's text at the md link to a max of 2 items
            split_text = node_text.split(f"[{alt}]({url})", 1)
            this_node_components.append(TextNode(node_text[1],TextType.TEXT))
            this_node_components.append(TextNode(f"[{alt}]({url})"))
            
            #the node has been split and added to this_node_components
            


    return ""

