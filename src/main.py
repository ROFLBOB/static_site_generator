
from textnode import TextNode, TextType
from test_textnode import TestTextNode
import os #checking if files exist, navigation
import shutil #copy files

def main():
    print("OK")
    source = 'static'
    destination = 'public'
    copy_source_directory(source,destination)

def copy_source_directory(source, destination): #copies all contents from source directory to the destination directory
    #it should first delete all the contents of the destination directory to ensure the copy is clean
    #it should copy all files, subdirectories, and nested files

    #clear out the destination directory
    if os.path.exists(destination):
        shutil.rmtree(destination)

    os.mkdir(destination)

    #look at each item in the source directory
    #if it's a file, copy it to the corresponding location in destination
    #if it's a directory, create that directory in the destination an dcurvusively copy the contents
    for item in os.listdir(source):
        print(f"Item: {item} ")
        #create the full path for both source and destination
        source_path = os.path.join(source,item)
        dest_path = os.path.join(destination, item)

        if os.path.isfile(source_path):
            shutil.copy2(source_path, dest_path)
            print(f"Created {dest_path}")
        else:
            #a directory, call the function recursively
            copy_source_directory(source_path, dest_path)


main()