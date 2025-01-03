from textnode import TextNode, TextType, text_node_to_html_node
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
    print("Initial node: ", text_node)
    converted_nodes = split_nodes_delimiter(text_node, "**", TextType.BOLD)
    print("After bold: ", converted_nodes)
    converted_nodes = split_nodes_delimiter(converted_nodes, "*", TextType.ITALIC)
    print("After italics: ", converted_nodes)
    converted_nodes = split_nodes_delimiter(converted_nodes, "`", TextType.CODE)
    print("After code: ", converted_nodes)
    
    try: 
        converted_nodes = split_nodes_images(converted_nodes)
        print("After images: ", converted_nodes)
    except Exception as e:
        print("Error in split_nodes_images: ", e)

    try: 
        converted_nodes = split_nodes_link(converted_nodes)
        print("After images: ", converted_nodes)
    except Exception as e:
        print("Error in split_nodes_link: ", e)
    
 
    



    return converted_nodes

#print(text_to_textnodes("**this is bold text**"))
#print(text_to_textnodes("*this is italic text*"))
#print(text_to_textnodes("`this is code text`"))
#print(text_to_textnodes("here is a link: [to google](https://google.com)"))
#print(text_to_textnodes("and my friend, an image of my dog: ![an image](http://mydog.com/dog.jpg)"))
#print(text_to_textnodes("This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)."))
#print(text_to_textnodes("![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"))

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

def block_to_block_type(md_block):
    # determine what kind of block md_block is (markdown string)
    #supports h1-6, code blocks, quote blocks, ul and ol, and normal text

    #look for header start with regex
    x = re.search(r"^#{1,6}\s",md_block)
    if x != None:
        return "heading"
    #look for 3 backticks at start and end for code blocks
    if md_block.startswith("```") and md_block.endswith("```"):
        return "code"
    #look for > at start of each line for code block
    split_line = md_block.splitlines()
    is_quote = False
    for line in split_line:
        if line.startswith(">") == False:
            is_quote = False
            break
        is_quote = True
    if is_quote:
        return "quote"
    # check for ordered list
    is_ol = False
    is_ul = True
    for y in range(len(split_line)-1):
        if split_line[y].startswith(f"{y+1}. "):
            is_ol = True
        elif split_line[y].startswith("* ") or split_line[y].startswith("- "):
            is_ul = True
        else:
            is_ol = False
            is_ul = False
            break
    if is_ol:
        return "ordered_list"
    if is_ul:
        return "unordered_list"
    
    return "paragraph"


h1heading = "# An h1 heading here"
h2heading = "## This is a h2 heading"
h3heading = "### This is an h3 heading"
code_block = "```\nThis is a code block\n```"
quote_block = ">this is a quote block\n>on two lines"
unordered_list = "* an unordered list item\n* the second item\n* The third item"
ordered_list = "1. first item of ordered list\n2. second item and \n3. third item"
regular_text = "this is just regular paragraph text"

tests = [h1heading, h2heading, h3heading, code_block, quote_block, unordered_list, ordered_list, regular_text]

for test in tests:
    print(f"\"{test}\" is a {block_to_block_type(test)}")
