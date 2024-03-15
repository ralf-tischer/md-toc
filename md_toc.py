"""
Browse through the specified files and create table of contents (TOC) in each file.
If already existing, update the TOC.

Parameters:
-----------
-f or --files: list of files, default=None
-p or --paths: list of paths, default=None
-s or --sub: if set, browse all paths sub-directories

Examples
--------
python .\md_toc.py -f README.md -p "Level1_test\Level2_test"
"""

import argparse
import re
import os

MAX_LEVEL_DEFAULT = 99          # Defualt levels of TOC
CR_QTY_AFTER_TOC = 2            # Number of `/n` after TOC

HEADING_TO_LINK_FROM = ",;:| "  # Chars to be replaced by `-` in a heading to create the link
TOC_HEADING = "Table of Contents"
MD_TOC_TOKEN = "<!-- MD-TOC START LEVEL %L -->\n\n"
MD_TOC_TOKEN_START = "<!-- MD-TOC START LEVEL "
MD_TOC_TOKEN_END = "<!-- MD-TOC END -->"

def main():
    filenames, paths, sub, max_level = parse_command_line()
    
    if paths:
        filenames_from_paths = []
        for path in paths:
            filenames_from_paths += get_all_files_from_path(path, sub)
        filenames += filenames_from_paths

    # Update table of content
    files_updated = 0
    if filenames:
        for filename in filenames:
            if update_toc(filename, max_level):
                files_updated += 1

    print(f"{files_updated} files updated.")


def parse_command_line() -> tuple:
    """ Parse command line. 

    Returns
    -------
    filenames : list of str
    paths : list of paths
    sub : bool
        True if all subdirectories are included
    level : int
        Maximum level to be included in TOC
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--files", nargs="+", default=[])
    parser.add_argument("-l", "--level", type=int, default=MAX_LEVEL_DEFAULT)
    parser.add_argument("-p", "--paths", nargs="+", default=[])
    parser.add_argument("-s", "--sub", action="store_true")

    args = parser.parse_args()

    filenames = args.files
    paths = args.paths
    sub = args.sub
    level = args.level
    return filenames, paths, sub, level


def update_toc(filename: str, max_level : int) -> bool:
    """ Update table of content of a single file.

    Parameters
    ----------
    filename : str
        Including path, if required
    max_level : int
        Maximum level to be included in TOC

    Returns
    -------
    was_updated : bool
    """

    file = read_file(filename)
    level = get_existing_toc_level(file)
    toc = create_toc(file, level)

    print("-" * len("TOC for " + filename))
    print(f"TOC for {filename}")
    print("-" * len("TOC for " + filename))
    print(toc)

    if level > 0:
        # Overwrite if TOC exists
        newfile = overwrite_toc(file, toc)
        if file != newfile:
            # Save, if updated
            save_file(newfile, filename)
        else:
            return False
    else:
        # Create new
        file = insert_toc(file,toc)
        save_file(file, filename)
    
    return True


def create_toc(file: str, max_level: int = 99) -> str:
    """ Create table of content in markdown format.

    Parameters
    ----------
    file : str
    max_level : into, default = 99

    Returns
    -------
    toc : str
    """

    anchors = get_anchors(file)
    
    toc = MD_TOC_TOKEN.replace("%L", str(max_level)) + "# " + TOC_HEADING + "\n\n"
    for item in anchors:
        if item["level"] <= max_level and item["heading"] != TOC_HEADING:
            indent = "  " * (item["level"] - 1)
            toc += f"{indent}- [{item['heading']}]({item['link']})\n"
    toc += "\n" + MD_TOC_TOKEN_END + "\n" * CR_QTY_AFTER_TOC
    return toc


def get_existing_toc_level(file: str) -> int:
    """ Check if file already has a md-toc. 
    
    If yes, return the max level.

    Parameters
    ----------
    file : str

    Returns:
    --------
    get_existing_toc_level : bool 
    """

    lines = file.split("\n")
    for line in lines:
        if line.startswith(MD_TOC_TOKEN_START):
            match = re.search(r"LEVEL\s+(\d+)", line)   # Check for token `LEVEL`
            if match: 
                return int(match.group(1))
            else:
                return MAX_LEVEL_DEFAULT
    return 0
        
    
def overwrite_toc(file: str, toc: str) -> str:
    """ Overwrite exsiting TOC.

    Find start and end token, delete everything in between and put in new content.

    Parameters
    ----------
    file : str
    toc : str

    Returns:
    --------
    updated_file : str 
    """

    lines = file.split("\n")
    start = None
    end = None

    # Find start and end tokens
    for index, line in enumerate(lines):
        if line.startswith(MD_TOC_TOKEN_START):
            start = index
        elif line.startswith(MD_TOC_TOKEN_END):
            end = index + CR_QTY_AFTER_TOC
            break

    if start and end:
        # Slice lines list from start to end
        #file = lines[:start] + toc + lines[end+1:]
        file = "\n".join(lines[:start] + [toc] + lines[end+1:])

    return file


def insert_toc(file: str, toc: str) -> str:
    return toc + file


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
            heading = line[level:].strip()

            # Check if the header exists in anchors
            existing = [item for item in anchors if item["heading"] == heading]
            
            # TODO: check count up, but create a new entry 
            if existing:
                max_repeat = max(item["repeat"] for item in existing)
                repeat += max_repeat + 1
            else:
                repeat = 0
            anchor = {
                "heading": heading, 
                "link": f'#{clean_link(heading)}',
                "repeat": repeat,
                "level": level
            }       
            anchors.append(anchor)
    return anchors


def clean_link(heading: str) -> str:
    """ Clean link to md format.

    Parameters
    ----------
    heading : str

    Returns
    -------
    cleaned_link : str
    """

    # Lowercase
    result = heading.lower()

    # Replace special charcters as defined in HEADING_TO_LINK_FROM to `-`
    result = re.sub(r'\s*[' + re.escape(HEADING_TO_LINK_FROM) + r']\s*', '-', result.strip())
    return result


def get_heading_level(line: str) -> int:
    """ Get level of a heading line by counting `#`"""

    count = 0
    for char in line:
        if char == "#":
            count += 1
        else:
            break
    return count


def read_file(filename: str) -> str:
  """ Read the content of a file from the local directory.
  
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


def save_file(file: str, filename: str) -> bool:
    """ Save file on the local directory.
  
    Parameters
    ----------
    file : str
        Content to be saved
    filename : str
        Including path, if required

    Returns
    -------
    success : bool
    """
    with open(filename, 'w') as f:
        # Write the string to the file
        f.write(file)

    return True


def get_all_files_from_path(directory: str, sub: bool = False) -> str:
    """ Provide a list of all files inside a directory including sub-directories.

    Parameters
    ----------
    directory : str
    sub : bool
        If set browse all sub-directories
    """

    files = []
    for entry in os.scandir(directory):
        if entry.is_file():
            if entry.name.lower().endswith(".md"):
                files.append(os.path.join(directory, entry.name))
        elif entry.is_dir() and sub:  
            files.extend(get_all_files_from_path(entry.path, sub))
    return files


if __name__ == "__main__":
    main()
    
