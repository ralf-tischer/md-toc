'''
Browse through the specified files and create table of contents (TOC) in each file.
If already existing, the TOC will be updated.

Parameters:
-----------
python md-toc -f "myfile.md" -p "mypath/" 
    -f or --files: list of files, default=None
    -p or --paths: list of paths, default=None

Examples
--------
-r https://github.com/RalfTischer/coding-cookbook
-f general.md
    
'''
import argparse
import re

ANCHOR_REGEX = r"^#+\s*(.+?)\s*#*"
HEADING_LEVELS = {
    "#": 1, 
    "##": 2,
    "###": 3, 
    "####": 4
}


def main():
    filenames, paths = parse_command_line()
    print(f"files={filenames}") 
    print(f"paths={paths}")

    # TODO: paths

    files_updated = 0
    # Update table of content
    for filename in filenames:
        if update_toc(filename):
            files_updated += 1


def parse_command_line() -> tuple:
    """ Parse command line. 

    Returns
    -------
    filenames : list of str
    paths : list of paths
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--files", nargs="+", default=[])  
    parser.add_argument("-p", "--paths", nargs="+", default=[])

    args = parser.parse_args()

    filenames = args.files
    paths = args.paths
    return filenames, paths


def update_toc(filename: str) -> bool:
    """ Update table of content of a single file

    Parameters
    ----------
    filename : str
        Including path, if required

    Returns
    -------
    was_updated : bool
    """
    file = read_content(filename)
    max_level = 99  # TODO: max_level
    toc = create_toc(file, max_level)

    if toc_exists(file):
        file = overwrite_toc(file, toc)
    else:
        file = insert_toc(file,toc)
    save_file(file, filename)
    return True


def read_content(filename: str) -> str:
  """ Read the content of a file from the local directory
  
  Parameters
  ----------
  filename : str
      Including path, if required

  Returns
  -------
  content : str
  """
  with open(filename) as f:
    content = f.read()
  return content


def create_toc(file: str, max_level: int = 99) -> str:
    """ Create table of content in markdown format

    Parameters
    ----------
    file : str
    max_level : into, default = 99

    Returns
    -------
    toc : str
    """
    anchors = get_anchors(file)
    print("Anchors:", anchors)
    
    toc = "## Table of Contents\n\n"    
    for item in anchors:
        if item["level"] <= max_level:
            indent = "  " * (item["level"] - 1)
            toc += f"{indent}- [{item['heading']}](#{item['link']})\n"
    return toc


def toc_exists(file: str) -> bool:
    return False
        
    
def overwrite_toc(file: str, toc: str) -> str:
    return toc + file


def insert_toc(file: str, toc: str) -> str:
    return toc + file


def save_file(file: str, filename: str) -> str:
    return True


def get_anchors(file: str) -> list:
    """ Parse file and extract anchors. 

    Parameters
    ----------
    file : str
        File content

    Returns
    -------
    anchors : list of dicts
        Keys: heading, link, repeat, level
    """

    anchors = []
    lines = file.split("\n")

    in_code_block = False

    for line in lines:
        if "```" in line:
            in_code_block = not in_code_block
            continue

        if in_code_block or re.search(r"`.*?#.*?`", line):  
            continue

        if line.startswith("#") and "```" not in line:
            level = get_heading_level(line)
            print("level", level, "for line\n", line)
            heading = line[level:].strip()

            # Check if the header exists in anchors
            existing = [item for item in anchors if item["heading"] == heading]
            
            # TODO: check count up, but create a new entry 
            if existing:
                max_repeat = max(item["repeat"] for item in existing)
                repeat += msx_repeat + 1
            else:
                repeat = 0
            anchor = {
                "heading": heading, 
                "link": f'#{heading.lower().replace(" ", "-")}',
                "repeat": repeat,
                "level": level
            }       
            anchors.append(anchor)
    return anchors


def get_heading_level(line: str) -> int:
    """ Get level of a heading line by counting #"""
    count = 0
    for char in line:
        if char == "#":
            count += 1
        else:
            break
    return count


if __name__ == "__main__":
    main()
    
