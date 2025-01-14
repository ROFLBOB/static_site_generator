from code_logic import markdown_to_blocks, markdown_to_html_node
import os

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

    #check if paths exist
    if not os.path.exists(from_path):
        raise FileNotFoundError(f"The file '{from_path}' does not exist.")
    
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"The file '{template_path}' does not exist.")
    
    #read and store the md file, template file. use with open() because it closes the file automatically
    with open(from_path, 'r') as markdown_file:
        markdown = markdown_file.read()
    
    with open(template_path, 'r') as template_file:
        template = template_file.read()

    #use the markdown_to_html_node function and .to_html() to convert the md file to an html string

    html_node = markdown_to_html_node(markdown)
    html = html_node.to_html()

    #extract the title from the markdown
    h1_title = extract_title(markdown)

    #replace the {{ Title }} and {{ Content }} placeholders in the template with the html and title that were generated
    template = template.replace("{{ Title }}", h1_title)
    template = template.replace("{{ Content }}", html)

    #write the new full html page to a file at dest_path. create any necessary directories if they don't exist
    #check that the directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok = True)
    with open(dest_path, 'w') as file:
        file.write(template)
    