from textnode import TextNode, TextType, text_node_to_html_node
import re

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