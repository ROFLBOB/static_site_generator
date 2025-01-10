from code_logic import markdown_to_blocks, markdown_to_html_node

def extract_title(markdown):
    #pull the h1 header from the md file and return it

    #identify the first instance of "# "
    md_blocks = markdown_to_blocks(markdown)

    for block in md_blocks:
        if block.startswith("# "):
            return f"{block[2:]}"
    
    raise Exception("No valid h1")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    #read and store the md file, template file
    markdown_file = open(from_path)
    markdown = markdown_file.read()
    markdown_file.close()
    template_file = open(template_path)
    template = template_file.read()
    template_file.close()

    #use the markdown_to_html_node function and .to_html() to convert the md file to an html string

    html_node = markdown_to_html_node(markdown)
    html = html_node.to_html()

    #extract the title from the markdown
    h1_title = extract_title(markdown)

    #replace the {{ Title }} and {{ Content }} placeholders in the template with the html and title that were generated
    template = template.replace("{{ Title }}", h1_title)
    template = template.replace("{{ Content }}", html)

    #write the new full html page to a file at dest_path. create any necessary directories if they don't exist
    



    return ""