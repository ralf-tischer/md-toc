"""
Browse through the specified files and create table of contents (TOC) in each file.
If already existing, the TOC will be updated.

Usage:
------
python md-toc "myfile.md", "mypath/"

Parameters:
-----------
files : list of str, default=[]
    Example: ["myfile.md", "newfile.md", "mypath/"]

"""

import sys


def main():
    args = sys.argv[1:]
        
    # Parse command line arguments
    print(f"Parsing {len(args)} arguments:")
    filenames = []
    for arg in args:
        print(f"- {arg}", end=" ")
        if arg[-1] == "/" or arg[-1] == "\\":
            # TODO: Path detected
            print("path detected.")
        else:
            filenames.append(arg)
            print("appended to file list.")
    print("Total # of filenames:", len(filenames))
    files_updated = 0

    # Update table of content
    for filename in filenames:
        if update_toc(filename):
            files_updated += 1


def read_content(filename: str) -> str:
    return "Test\nMe\n"


def create_toc(file: str) -> str:
    return "ToC\n"


def update_toc(filename: str) -> bool:
    file = read_content(filename)
    toc = create_toc(file)

    if toc_exists(file):
        file = overwrite_toc(file, toc)
    else:
        file = insert_toc(file,toc)
    save_file(file, filename)
    return True


def toc_exists(file: str) -> bool:
    return False
        
    
def overwrite_toc(file: str, toc: str) -> str:
    return toc + file


def insert_toc(file: str, toc: str) -> str:
    return toc + file


def save_file(file: str, filename: str) -> str:
    print(f"Content of {filename}:")
    print(file)
    return True

if __name__ == "__main__":
    main()
    