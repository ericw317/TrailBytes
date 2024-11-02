import os

# print list
def print_list(list):
    string = ""
    for element in list:
        string += f"\n{element}"
    return string

# print list numbered
def print_list_numbered(list):
    string = ""
    for number, element in enumerate(list, start=1):
        string += f"\n{number}: {element}"
    return string

def sort_files_by_modification(files):
    # Sort files by their modification time
    return sorted(files, key=lambda x: os.path.getmtime(x))