from code_logic import markdown_to_blocks

def extract_title(markdown):
    #pull the h1 header from the md file and return it

    #identify the first instance of "# "
    md_blocks = markdown_to_blocks(markdown)

    for block in md_blocks:
        if block.startswith("# "):
            return f"{block[2:]}"
    
    raise Exception("No valid h1")
    
md = """
the first paragraph

## an h2

# This is the title

and this is the body
"""

print(extract_title(md))