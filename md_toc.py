"""
Browse through the specified files and create table of contents (TOC) in each file.
If already existing, update the TOC.

Parameters:
-----------
-f or --files: list of files, default=None
-p or --paths: list of paths, default=None
-s or --sub: if set, browse all paths sub-directories
-l or --level: maximum level of headings to be included to TOC

Examples
--------
python .\md_toc.py -f README.md -p "Level1_test\Level2_test -s"
"""

# TODO: Check max_level integrity

import argparse
import re
import os

MAX_LEVEL_DEFAULT = 99          # Default levels of TOC
CR_QTY_AFTER_TOC = 2            # Number of `/n` after TOC


HEADING_TO_LINK_FROM_TO = [                         # Chars to be replaced in a heading to create the link
    {"pattern": ",;:| ", "replacement": "-"},
    {"pattern": ".", "replacement": ""}]

TOC_HEADING = "Table of Contents"
TOC_LEVEL = 2     # Number of `#` of created TOC

MD_TOC_TOKEN_START = "<!-- MD-TOC START LEVEL "
MD_TOC_TOKEN_LEVEL = "<!-- MD-TOC START LEVEL %L -->\n"
MD_TOC_TOKEN_INCLUDE_START = "<!-- MD-TOC INCLUDE "
MD_TOC_TOKEN_INCLUDE = "<!-- MD-TOC INCLUDE %I LEVEL %L -->\n"
MD_TOC_TOKEN_END = "<!-- MD-TOC END -->"


def main():
    filenames, paths, sub, max_level, verbose = parse_command_line()
    
    if paths:
        filenames_from_paths = []
        for path in paths:
            filenames_from_paths += get_all_files_from_path(path, sub)
        filenames += filenames_from_paths

    # Update table of content
    files_updated = 0
    if filenames:
        for filename in filenames:
            if update_toc(filename, verbose):
                files_updated += 1

    print(f"{len(filenames)} files analyzed, {files_updated} files updated.")

def parse_command_line() -> tuple:
    """ Parse command line. 

    Returns
    -------
    filenames : list of str
    paths : list of paths
    level : int
        Maximum level to be included in TOC
    sub : bool
        True if all subdirectories are included
    verbose : bool
        True if verbose mode is selected
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--files", nargs="+", default=[])
    parser.add_argument("-l", "--level", type=int, default=MAX_LEVEL_DEFAULT)
    parser.add_argument("-p", "--paths", nargs="+", default=[])
    parser.add_argument("-s", "--sub", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()

    filenames = args.files
    paths = args.paths
    sub = args.sub
    level = args.level
    verbose = args.verbose

    return filenames, paths, sub, level, verbose


def update_toc(filename: str, verbose: bool) -> bool:
    """ Update table of content of a single file.

    Parameters
    ----------
    filename : str
        Including path, if required
    verbose : bool
        If True print TOC

    Returns
    -------
    was_updated : bool
    """

    file = read_file(filename)
    start, end, level, includes = parse_existing_toc(file)
    toc = create_toc(file, includes, start_at_line=end, max_level=level)

    if verbose:
        print("-" * len("TOC for " + filename))
        print(f"TOC for {filename}")
        print("-" * len("TOC for " + filename))
        print(toc)

    if end:
        # Overwrite if TOC exists
        newfile = overwrite_toc(file, toc, start, end)
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


def parse_existing_toc(file: str) -> tuple:
    """
    Parameters
    ----------
    file : str

    Returns
    -------
    start : int
        `None` it not detected
    end : int
        `None` it not detected
    level : int
        `0` it not detected
    includes : list of str
        List of filenames, [] if empty 
    """

    lines = file.split("\n")
    start = None
    end = None
    level = MAX_LEVEL_DEFAULT
    includes = []    

    # Find start, end tokens and level
    in_code_block = False
    for index, line in enumerate(lines):
        if "```" in line:
            in_code_block = not in_code_block
            # Code block start or end
            continue

        if in_code_block:
            # Ignore code block
            continue

        if line.startswith(MD_TOC_TOKEN_START):
            # Start token detected
            start = index
            level = get_level_in_token(line)

        elif line.startswith(MD_TOC_TOKEN_END):
            # End token detected
            end = index + CR_QTY_AFTER_TOC  # Include added `/n`
            break

        elif line.startswith(MD_TOC_TOKEN_INCLUDE_START):
            # Include token detected
            inc_filename = get_include_in_token(line)
            inc_level = get_level_in_token(line)
            if inc_filename:
                includes.append({"filename": inc_filename, "level": inc_level})
            continue

    return start, end, level, includes


def get_level_in_token(line: str) -> int:
    """ Get level inside a line with md-toc token.

    Parameter
    ---------
    line : str

    Returns
    -------
    level : int, default=MAX_LEVEL_DEFAULT
    """

    match = re.search(r"LEVEL\s+(\d+)", line)   # Check for token `LEVEL`
    if match: 
        # Found level
        level = int(match.group(1))      
    else:
        # Found incorrect token
        level = MAX_LEVEL_DEFAULT
    
    return level


def get_include_in_token(line: str) -> str:
    """ Get include inside a line with md-toc token.

    Parameter
    ---------
    line : str

    Returns
    -------
    include : str, default=None
    """

    match = re.search(r"INCLUDE\s+(\S+)", line)   # Check for token `INCLUDE`
    if match: 
        # Found include
        include = match.group(1)
    else:
        include = None
    
    return include


def create_toc(inc_file: str, includes : list, start_at_line: int, max_level: int = MAX_LEVEL_DEFAULT) -> str:
    """ Create table of content in markdown format.

    Parameters
    ----------
    file : str
    includes: list 
        Filenames to be included
    start_at_line : int
    max_level : into, default = 99

    Returns
    -------
    toc : str
    """
    if start_at_line:
        anchors = get_anchors(inc_file, start_at_line)
    else:
        anchors = get_anchors(inc_file)

    # TOC Header
    toc = MD_TOC_TOKEN_LEVEL.replace("%L", str(max_level)) 

    # Include tokens
    if includes:
        for include in includes:
            line = MD_TOC_TOKEN_INCLUDE.replace("%I", include["filename"])
            line = line.replace("%L", str(include["level"]))
            toc += line

    # Heading
    toc += f"\n{'#' * TOC_LEVEL} {TOC_HEADING}\n"

    # Anchor links
    toc += "\n" + anchor_list(anchors, max_level)

    # Include anchors
    if includes:
        for include in includes:
            inc_filename = include["filename"]
            inc_level = include["level"]
            inc_file = read_file(inc_filename)
            _, inc_end, _, _ = parse_existing_toc(inc_file)

            if inc_end:
                inc_anchors = get_anchors(inc_file, inc_end)
            else:
                inc_anchors = get_anchors(inc_file)

            toc += f"\n{'#' * (TOC_LEVEL + 1)} {inc_filename}\n" + anchor_list(inc_anchors, inc_level, inc_filename) + "\n"

    # Close token
    toc += "\n" + MD_TOC_TOKEN_END + "\n" * (CR_QTY_AFTER_TOC)
    
    return toc


def anchor_list(anchors: list, max_level: int, source: str = None) -> str:
    """ Create list of anchors as a rough TOC

    Parameters
    ----------
    anchors : list of str
    source : str, default=None
        Source filename. Will be included to links if set

    Returns
    -------
    anchor_list : str

    """
    anchor_list = ""
    if anchors == []:
        return
    
    for item in anchors:
        if item["level"] <= max_level and item["heading"] != TOC_HEADING:
            if source:
                link = f"{source}{item['link']}"
            else:
                link = f"{item['link']}"
            indent = "  " * (item["level"] - 1)
            anchor_list += f"{indent}- [{item['heading']}]({link})\n"

    return anchor_list

    
def overwrite_toc(file: str, toc: str, start: int, end: int) -> str:
    """ Overwrite existing TOC.

    Overwrite TOC.

    Parameters
    ----------
    file : str
    toc : str
    start : int
    end : int

    Returns:
    --------
    updated_file : str 
    """

    if start and end:

        # Slice lines list from start to end
        lines = file.split("\n")
        toc = toc[:-1]
        file = "\n".join(lines[:start] + [toc] + lines[end:])

    return file


def insert_toc(file: str, toc: str) -> str:
    """ Insert TOC.

    Parameters
    ----------
    file : str
    toc : str

    Returns:
    --------
    updated_file : str 
    """

    return toc + file


def get_anchors(file: str, start_at_line: int = 0) -> list:
    """ Parse file and extract anchors. 

    Parameters
    ----------
    file : str
        File content
    start_at_line : int, default = 0
        Start parsing at this line index 

    Returns
    -------
    anchors : list of dicts
        Keys: heading, link, repeat, level
    """

    anchors = []
    lines = file.split("\n")

    in_code_block = False
    
    for i in range(start_at_line, len(lines)):
        line = lines[i]
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
    """ Clean heading to prepare anchor link for md format.

    Parameters
    ----------
    heading : str

    Returns
    -------
    cleaned_link : str
    """

    # Lowercase
    result = heading.lower()

    # Replace special characters as defined in HEADING_TO_LINK_FROM_TO
    for from_to in HEADING_TO_LINK_FROM_TO:
        pattern = from_to["pattern"]
        replacement = from_to["replacement"]
        result = re.sub(r'\s*[' + re.escape(pattern) + r']\s*', replacement, result.strip())

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
