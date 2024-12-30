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



node = TextNode(
    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    TextType.TEXT,
)


def split_nodes_link(old_nodes):
    #takes a list of nodes and identify the links in them, and return a list of all the nodes with the proper text type.
    #link syntax: [alt text](url_here)
    text_node_list = []
    for node in old_nodes:
        #check if the extract markdown links function created anything
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            #no links, just add the text node to the list as normal
            if len(node.text) > 0:
                text_node_list.append(node)
            continue

        node_text = node.text

        while len(links) > 0:
            #check if links are in the node_text
            links = extract_markdown_links(node_text)
            for link_details in links:
                alt = link_details[0]
                url = link_details[1]
                #split the node text at the link
                split_text = node_text.split(f"[{alt}]({url})", 1)
                #append split_text[0] to the overall list
                text_node_list.append(TextNode(split_text[0],TextType.TEXT))
                text_node_list.append(TextNode(f"[{alt}]({url})",TextType.LINK,url))
                node_text = split_text[1]
        
        if node_text:
            text_node_list.append(TextNode(node_text, TextType.TEXT))
        
    return text_node_list

def split_nodes_images(old_nodes):
    #takes a list of nodes and identify the images in them, and return a list of all the nodes with the proper text type.
    #image syntax: ![alt text](url_here)
    text_node_list = []
    for node in old_nodes:
        #check if the extract markdown links function created anything
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            #no links, just add the text node to the list as normal
            if len(node.text) > 0:
                text_node_list.append(node)
            continue

        node_text = node.text

        while len(images) > 0:
            #check if links are in the node_text
            images = extract_markdown_links(node_text)
            for img_details in images:
                alt = img_details[0]
                url = img_details[1]
                #split the node text at the link
                split_text = node_text.split(f"[{alt}]({url})", 1)
                #append split_text[0] to the overall list
                text_node_list.append(TextNode(split_text[0],TextType.TEXT))
                text_node_list.append(TextNode(f"![{alt}]({url})",TextType.IMAGE))
                node_text = split_text[1]
        
        if node_text:
            text_node_list.append(TextNode(node_text, TextType.TEXT))
        
    return text_node_list
            



node = TextNode(
    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    TextType.TEXT,
)
node2 = TextNode(
    "[a link to google](https://google.com) [followed by a link to facebook](https://facebook.com). Oh the humanity!",
    TextType.TEXT,
)
node3 = TextNode(
    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    TextType.TEXT,
)
new_nodes = split_nodes_link([node2])
print(new_nodes)