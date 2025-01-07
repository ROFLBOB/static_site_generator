from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode
import re

#split_nodes_delimiter: takes a list of text nodes and splits it according to the delimiter.
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    text_node_list = []
    for node in old_nodes:
        #print(f"The node: {node}")
        if node.text_type == TextType.TEXT:
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

        #check if links are in the node_text
        for link_details in links:
            alt, url = link_details
            #split the node text at the link
            split_text = node_text.split(f"[{alt}]({url})", 1)
            #append split_text[0] to the overall list
            text_node_list.append(TextNode(split_text[0],TextType.TEXT))
            text_node_list.append(TextNode(alt,TextType.LINK,url))
            if len(split_text) == 2:
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


        #check if links are in the node_text
        images = extract_markdown_images(node_text)
        for img_details in images:
            alt = img_details[0]
            url = img_details[1]
            #split the node text at the link
            split_text = node_text.split(f"![{alt}]({url})", 1)
            #append split_text[0] to the overall list
            text_node_list.append(TextNode(split_text[0],TextType.TEXT))
            text_node_list.append(TextNode(f"{alt}",TextType.IMAGE,url))
            if len(split_text) == 2:
                node_text = split_text[1]
                        
        if node_text:
            text_node_list.append(TextNode(node_text, TextType.TEXT))
        
    return text_node_list

def text_to_textnodes(text):
    #when given md text, it outputs a list of textnodes with their proper types
    #apply all splitting functions to the text
    
    #convert to a textnode
    text_node = [TextNode(text, TextType.TEXT)]
    #print("Initial node: ", text_node)
    converted_nodes = split_nodes_delimiter(text_node, "**", TextType.BOLD)
    #print("After bold: ", converted_nodes)
    converted_nodes = split_nodes_delimiter(converted_nodes, "*", TextType.ITALIC)
    #print("After italics: ", converted_nodes)
    converted_nodes = split_nodes_delimiter(converted_nodes, "`", TextType.CODE)
    #print("After code: ", converted_nodes)
    
    try: 
        converted_nodes = split_nodes_images(converted_nodes)
        #print("After images: ", converted_nodes)
    except Exception as e:
        print("Error in split_nodes_images: ", e)

    try: 
        converted_nodes = split_nodes_link(converted_nodes)
        #print("After images: ", converted_nodes)
    except Exception as e:
        print("Error in split_nodes_link: ", e)
    return converted_nodes

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"

def markdown_to_blocks(markdown):
    #take raw markdown string (a full document) as input and returns a list of "block" strings
    #md blocks are separated by a blank, empty line. 
    #strip any leading or trailing whitespace from each block
    #remove empty blocks due to excessive newlines


    #separate the string into a list
    markdown_list = markdown.split("\n\n")
    filtered_blocks = []
    for block in markdown_list:
        #if the block is empty, remove it
        if block == '':
            continue
        #strip any extra leading or trailing whitespace from each block
        block = block.strip()
        filtered_blocks.append(block)
    
    return markdown_list

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("#", "##", "###", "####", "#####", "######")):
        return block_type_heading
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return block_type_code
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return block_type_paragraph
        return block_type_quote
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return block_type_paragraph
        return block_type_ulist
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return block_type_paragraph
        i += 1
        return block_type_olist
    return block_type_paragraph

def convert_paragraph(block):
    #convert a paragraph block to HTML node
    text_nodes = text_to_children(block)

    return ParentNode("p",text_nodes)



def convert_heading(block):
    heading_level = block.find(" ")
    children = text_to_children(block)
    return ParentNode(f"h{heading_level}", children)


def convert_code(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    code = block[4:-3]
    children = text_to_chilldren(code)
    return ParentNode("pre", children)

def convert_quote(block):
    split_lines = block.split("\n")
    new_value = []
    for line in split_lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")    
        new_value.append(line.lstrip(">").strip())
    content = " ".join(new_value)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def convert_unordered_list(block):
    split_lines = block.split("\n")
    html_items = []
    for item in split_lines:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

        
def convert_ordered_list(block):
    items = block.split('\n')
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li",children))
    return ParentNode("ol",html_items)

def markdown_to_html_node(markdown):
    #returns a parent htmlnode that contains many child htmlnodes representing the nested elements
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return convert_paragraph(block)
    if block_type == block_type_heading:
        return convert_heading(block)
    if block_type == block_type_code:
        return convert_code(block)
    if block_type == block_type_olist:
        return convert_ordered_list(block)
    if block_type == block_type_ulist:
        return convert_unordered_list(block)
    if block_type == block_type_quote:
        return convert_quote(block)
    raise ValueError("Invalid block type")


def text_to_children(text):
    #takes a string of text and returns a list of HTMLNodes that represetn the line markdown using previously created function
    #id the inline elements

    #converts the text to text nodes
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

paragraph = """
This is **bolded** paragraph
text in a p tag here
"""

multiple_paragraphs = """
This is a **bolded** paragraph
text in a p tag
tag here

This is another paragraph with *italic* text and `code` here
"""

lists = """
- This is a list
- with items
- and *more* items

1. This is an ordered list
2. with items
3. and **more** items
"""

headings = """# this is an h1

this is paragraph text

## this is h2

and another paragraph
"""

tests = [paragraph, multiple_paragraphs, lists, headings]

for test in tests:
    test_node = markdown_to_html_node(test)
    html = test_node.to_html()
    print(f"Testing...\n")
    print(html)
    print("\n")
