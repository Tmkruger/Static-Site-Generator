from textnode import TextNode , TextType
from htmlnode import HtmlNode, LeafNode, ParentNode
from nodemanager import split_nodes_delmiter
from markdown_to_html import *
import os
import shutil



def main():
    static_to_public("static", "public")

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

main()
