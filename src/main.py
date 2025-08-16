from textnode import TextNode , TextType
from htmlnode import HtmlNode, LeafNode, ParentNode
from nodemanager import split_nodes_delmiter
from markdown_to_html import *

import re
import os
import shutil



def main():
    file_path = "content/index.md"
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            #print(content)
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}") 
    static_to_public("static", "public")
    extract_title(content)

def static_to_public(source, destination):
    print(f"SOURCE: {source} | DESTINATION: {destination}")
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)
    if os.path.isfile(source) != True:
        dirs = os.listdir(source)
        print(f"DIRS: {dirs}")
        for dir in dirs:
            print(f"DIR: {dir}")
            if dir == ".git":
                continue
            elif dir == ".DS_Store":
                continue
            elif os.path.isfile(f"{source}/{dir}") != True:
                print(f"Going deeper into {dir}")
                print(f"MAKING DIR {os.path.join(destination, dir)}")
                os.mkdir(os.path.join(destination, dir))
                new_destination = os.path.join(destination, dir)
                static_to_public(os.path.join(source, dir), new_destination)
            elif os.path.isfile(f"{source}/{dir}") == True:
                print(f"Copying file {os.path.join(source, dir)} to {destination}")
                shutil.copy(os.path.join(source, dir), destination)
    else:
        print(f"ADDING {source} TO {destination}")
        shutil.copy(source, destination)

def extract_title(md):
    #CURSED REGEX :O
    pattern = r"^[ \t]*#\s+([^\r\n]*\S)[ \t]*\r?$"
    m = re.search(pattern, md, flags=re.MULTILINE)
    if not m:
        raise Exception("No Header")
    return m.group(1)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    

main()
