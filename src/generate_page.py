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
    file_properties = os.path.splitext(from_path)
    new_path = os.path.join(os.path.dirname(dest_path),os.path.basename(from_path)+".html")
    print(f"path is: {new_path}")
    os.makedirs(os.path.dirname(dest_path), exist_ok = True)
    with open(dest_path, 'w') as file:
        file.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
        #crawl every entry in the content directory
        #for each markdown file found, generate a new .html file using the same template.html

        #go over every file in the directory with a for loop
        items = os.listdir(dir_path_content)
        for item in items:
            #generate full path and check if it's an item or folder
            full_path = os.path.join(dir_path_content, item)
            print(f"full path of current file: {full_path}")
            if os.path.isfile(full_path):
                #it's an item. is it a markdown page?
                file_properties = os.path.splitext(item)
                print(f"{item} has the following extension: {file_properties[1]}")
                if file_properties[1] == ".md":
                    #yes it is. generate a new .html file using the template.html file with generate page
                    dest_file_path = os.path.join(dest_dir_path, os.path.splitext(os.path.basename(full_path))[0]+'.html')
                    print(f"running generate_page({full_path, template_path, dest_dir_path})")
                    generate_page(full_path,template_path,dest_file_path)
                    print(f"generated")
                    continue
            #is it a folder?
            if os.path.isdir(full_path):
                #it is! 
                inside_dir = os.path.join(dest_dir_path,item)
                print(f"{full_path} is a directory! creating copy at {inside_dir}")
                # create the new folder inside the destination directory
                os.makedirs(inside_dir,exist_ok=True)
                # run this function inside that folder
                generate_pages_recursive(full_path,template_path,inside_dir)
                print(f"running generate_pages_recursive({full_path},{template_path},{inside_dir})")
            

        return ""
    