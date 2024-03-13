'''
Browse through the specified files and create table of contents (TOC) in each file.
If already existing, the TOC will be updated.

Parameters:
-----------
python md-toc -r "https.github/repo.git" -f "myfile.md" -p "mypath/" 
    -r or --url: url
    -f or --files: list of files, default=None
    -p or --paths: list of paths, default=None
    
'''
import sys
import argparse

def main():
    url, filenames, paths = parse_command_line()
    print(f"url={url}")
    print(f"files={filenames}") 
    print(f"paths={paths}")

    """
    files_updated = 0
    # Update table of content
    for filename in filenames:
        if update_toc(filename):
            files_updated += 1
    """

def parse_command_line() -> tuple:
    # Parse command line  
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--url", required=True) 
    parser.add_argument("-f", "--files", nargs="+", default=[])  
    parser.add_argument("-p", "--paths", nargs="+", default=[])

    args = parser.parse_args()

    url = args.url
    filenames = args.files
    paths = args.paths

    return url, filenames, paths


def update_toc(filename: str) -> bool:
    file = read_content(filename)
    toc = create_toc(file)

    if toc_exists(file):
        file = overwrite_toc(file, toc)
    else:
        file = insert_toc(file,toc)
    save_file(file, filename)
    return True


def read_content(filename: str) -> str:
    return "Test\nMe\n"


def create_toc(file: str) -> str:
    return "ToC\n"


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
    
