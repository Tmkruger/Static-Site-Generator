from textnode import TextNode , TextType
from htmlnode import HtmlNode, LeafNode, ParentNode
from nodemanager import split_nodes_delmiter
from markdown_to_html import *
from pathlib import Path

import re
import os
import shutil
import sys

def main():
    if len(sys.argv) < 2:
        base_path = "/"
    else:
        base_path = sys.argv[1]
    if os.path.exists("public"):
        shutil.rmtree("public")
    static_to_public("static", "docs")
    generate_page_recursive("content", "template.html", "docs", base_path)


def static_to_public(source, destination):
    #print(f"SOURCE: {source} | DESTINATION: {destination}")
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)
    if os.path.isfile(source) != True:
        dirs = os.listdir(source)
        #print(f"DIRS: {dirs}")
        for dir in dirs:
            #print(f"DIR: {dir}")
            if dir == ".git":
                continue
            elif dir == ".DS_Store":
                continue
            elif os.path.isfile(f"{source}/{dir}") != True:
                #print(f"Going deeper into {dir}")
                #print(f"MAKING DIR {os.path.join(destination, dir)}")
                os.mkdir(os.path.join(destination, dir))
                new_destination = os.path.join(destination, dir)
                static_to_public(os.path.join(source, dir), new_destination)
            elif os.path.isfile(f"{source}/{dir}") == True:
                #print(f"Copying file {os.path.join(source, dir)} to {destination}")
                shutil.copy(os.path.join(source, dir), destination)
    else:
        #print(f"ADDING {source} TO {destination}")
        shutil.copy(source, destination)

def extract_title(md):
    #CURSED REGEX :O
    pattern = r"^#(?!#)[ \t]+(.+?)[ \t]*#*[ \t]*$"
    m = re.search(pattern, md, flags=re.MULTILINE)
    if not m:
        raise Exception("No Header")
    return m.group(1)

def generate_page(from_path, template_path, dest_path, base_path):
    # Opens Up md file from the from_path
    try:
        with open(from_path, "r") as file:
            markdown_contents = file.read()
    except FileNotFoundError:
        print(f"Error: The File {from_path} was not found")
    except Exception as e:
        print(f"An error occured: {e}")
    # Opens up the HTML Template File
    try:
        with open(template_path, "r") as file:
            template_contents = file.read()
    except FileNotFoundError:
        print(f"Error: The File {from_path} was not found")
    except Exception as e:
        print(f"An error occured: {e}")

    # Convert the md into an html string / get the webpage title
    node = markdown_to_html_node(markdown_contents)
    html_string = node.to_html()
    title = extract_title(markdown_contents)

    # Replace some of the html with proper paths
    contents = template_contents.replace('{{ Title }}', title)
    contents = contents.replace('{{ Content }}', html_string)
    contents = contents.replace('href="/',f'href="{base_path}')
    contents = contents.replace('src="/',f'src="{base_path}')

    dest_dir_path = os.path.dirname(dest_path)  # Get the parent directory
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)  # Create the parent directory
    to_file = open(dest_path, "w")  # Write to the file
    to_file.write(contents)

'''
    file_name = dest_path + "/index.html"
    out_dir = os.path.dirname(dest_path) or "."
    os.makedirs(out_dir, exist_ok=True)
    if os.path.exists(dest_path):
        try:
            with open(dest_path, 'w') as file:
                file.write(contents)
                print(f"File '{file_name}' successfully written to '{dest_path}'.")
        except Exception as e:
            print(f"error 1 {e}")
    else:
        os.makedirs(dest_path)
        try:
            with open(file_name, 'w') as file:
                file.write(contents)
                print(f"File '{file_name}' successfully written to '{dest_path}'.")
        except Exception as e:
            print(f"error 2 {e}")
'''

def generate_page_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    if os.path.isfile(dir_path_content):
        dest_dir_path = dest_dir_path.rstrip(".md") + ".html"
        generate_page(dir_path_content, template_path, dest_dir_path, base_path)
    else:
        items_in_dir = os.listdir(dir_path_content)
        print(f"ITEMS_IN_DIR: {items_in_dir}")
        for item in items_in_dir:
            if item.endswith('.md'):
                new_dest_path = os.path.join(dest_dir_path, item[:-3] + '.html')
            else:
                new_dest_path = os.path.join(dest_dir_path, item)
            if os.path.isfile(os.path.join(dir_path_content, item)):
                item_path = os.path.join(dir_path_content, item)
                generate_page(item_path, template_path, new_dest_path, base_path)
            else:
                new_cont_path = os.path.join(dir_path_content, item)
                generate_page_recursive(new_cont_path, template_path, new_dest_path, base_path)

if __name__ == "__main__":
    main()
