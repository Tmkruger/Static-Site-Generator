from textnode import TextNode , TextType
from htmlnode import HtmlNode, LeafNode, ParentNode
from nodemanager import split_nodes_delmiter
from markdown_to_html import *

import re
import os
import shutil



def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    static_to_public("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")

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
    pattern = r"^#(?!#)[ \t]+(.+?)[ \t]*#*[ \t]*$"
    m = re.search(pattern, md, flags=re.MULTILINE)
    if not m:
        raise Exception("No Header")
    return m.group(1)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    try:
        with open(from_path, "r") as file:
            markdown_contents = file.read()
    except FileNotFoundError:
        print(f"Error: The File {from_path} was not found")
    except Exception as e:
        print(f"An error occured: {e}")
    try:
        with open(template_path, "r") as file:
            template_contents = file.read()
    except FileNotFoundError:
        print(f"Error: The File {from_path} was not found")
    except Exception as e:
        print(f"An error occured: {e}")
    node = markdown_to_html_node(markdown_contents)
    html_string = node.to_html()
    title = extract_title(markdown_contents)
    contents = template_contents.replace('{{ Title }}', title)
    print(f"\nHTML STRING: {html_string}\n")
    contents = contents.replace('{{ Content }}', html_string)
    file_name = dest_path + "/generated.html"
    if os.path.exists("public"):
        try:
            with open(dest_path, 'w') as file:
                file.write(contents)
                print(f"File '{file_name}' successfully written to '{dest_path}'.")
        except Exception as e:
            print(f"error 1 {e}")
    else:
        os.makedirs(dest_path)
        try:
            with open(dest_path, 'w') as file:
                file.write(contents)
                print(f"File '{file_name}' successfully written to '{dest_path}'.")
        except Exception as e:
            print(f"error 2 {e}")
main()
