# coding=utf-8
import xml.etree.ElementTree as ET
import os
import csv
import re
from external_modules import xlsxwriter
from external_modules import sqlparse
from env2csv import env_files, env_parser


def xml_files(input_dir='input'):
    print "\nXML file(s) to be used in parsing:"
    count = 0
    xml_files = []
    for _file in os.listdir(input_dir):
        if not _file.__contains__('input') and _file.endswith('.xml'):
            xml_files.append(os.path.realpath(os.path.join(input_dir, _file)))
            count += 1
            print "\t%i)." % count, _file
        else:
            continue
    return xml_files


def parents(xml_file, parent_name=None, parent_attrib=None, parent_text=None, parent_start=None, parent_end=None):
    tree = ET.parse(xml_file)
    root = tree.getroot().tag
    parents = []
    if parent_name and not parent_attrib and not parent_text:
        for parent in tree.getiterator(parent_name):
            if parent.tag == parent_name:
                parents.append(parent)
    elif parent_name and parent_attrib:
        for parent in tree.getiterator(parent_name):
            if parent.tag == parent_name and parent.attrib == parent_attrib:
                parents.append(parent)
    elif parent_name and parent_attrib and parent_text:
        for parent in tree.getiterator(parent_name):
            if parent.tag == parent_name and parent.attrib == parent_attrib and parent.text == parent_text:
                parents.append(parent)
    elif parent_name and parent_attrib and parent_text or parent_start or parent_end:
        for parent in tree.getiterator(parent_name):
            if parent.tag == parent_name and parent.attrib == parent_attrib and parent.text == parent_text or parent.text.startswith(
                    parent_start) or parent.text.endswith(parent_end):
                parents.append(parent)
    else:
        for parent in tree.getiterator(root):
            parents.append(parent)
    return parents


def children(xml_file, child_name=None, child_attrib=None, child_text=None, child_start=None, child_end=None,
             parent_name=None, parent_attrib=None, parent_text=None, parent_start=None, parent_end=None):
    children = []
    for parent in parents(xml_file, parent_name, parent_attrib, parent_text, parent_start, parent_end):
        for child in parent:
            if child_name and not child_attrib and not child_text:
                if child.tag == child_name:
                    children.append(child)
            elif child_name and child_attrib:
                if child.tag == child_name and child.attrib == child_attrib:
                    children.append(child)
            elif child_name and child_attrib and child_text:
                if child.tag == child_name and child.attrib == child_attrib and child.text == child_text:
                    children.append(child)
            elif child_name and child_attrib and child_text or child_start or child_end:
                if child.tag == child_name and child.attrib == child_attrib and child.text == child_text or child.text.startswith(
                        child_start) or child.text.endswith(child_end):
                    children.append(child)
            else:
                children.append(child)
    return children


def main():
    for xml_file in xml_files():
        # general job information:
        for node in children(xml_file, parent_name="DSExport"):
            if node.tag == "Header":
                export_tool = node.get("ExportingTool")  # EXPORTING TOOL
                export_tool_version = node.get("ToolVersion")  # EXPORTING TOOL VERSION
                server_name = node.get("ServerName")  # SERVER NAME
                server_version = node.get("ServerVersion")  # SERVER VERSION
                instance_id = node.get("ToolInstanceID")  # INSTANCE ID
                print export_tool
                print export_tool_version
                print server_name
                print server_version
                print instance_id
            elif node.tag == "Job":
                job_name = node.get("Identifier")  # JOB NAME
                print job_name
        for node in children(xml_file, parent_name="Record",
                             parent_attrib={'Readonly': '0', 'Identifier': 'ROOT', 'Type': 'JobDefn'},
                             child_name="Property"):
            if node.attrib == {'Name': 'Description'}:
                job_description = node.text  # JOB DESCRIPTIONnode.text
                print job_description
            elif node.attrib["Name"] == "Container":
                container = node.text  # JOB CONTAINER
                print container
            elif node.attrib["Name"] == "JobVersion":
                job_version = node.text  # JOB VERSION
                print job_version


if __name__ in "__main__":
    main()
