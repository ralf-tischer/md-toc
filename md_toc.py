"""
Browse through the specified files and create table of contents (TOC) in each file.
If already existing, update the TOC.

Parameters:
-----------
python .\md-toc.py -f README.md -p "mypath/" 
    -f or --files: list of files, default=None
    -p or --paths: list of paths, default=None

Examples
--------
-f README.md
"""

import argparse
import re

HEADING_TO_LINK_FROM = ",;:| "  # Chars to be replaced by `-` in a heading to create the link
TOC_HEADING = "Table of Contents"
MD_TOC_TOKEN = "<!-- MD-TOC START LEVEL %L -->\n\n"
MD_TOC_TOKEN_START = "<!-- MD-TOC START LEVEL "
MD_TOC_TOKEN_END = "<!-- MD-TOC END -->"
CR_QTY_AFTER_TOC = 2            # Number of `/n` after TOC

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
    """ Update table of content of a single file.

    Parameters
    ----------
    filename : str
        Including path, if required

    Returns
    -------
    was_updated : bool
    """

    file = read_file(filename)
    max_level = 99  # TODO: max_level
    toc = create_toc(file, max_level)
    print(toc)

    if toc_exists(file):
        file = overwrite_toc(file, toc)
    else:
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
    print("Anchors:", anchors)
    
    toc = MD_TOC_TOKEN.replace("%L", str(max_level)) + "# " + TOC_HEADING + "\n\n"
    for item in anchors:
        if item["level"] <= max_level and item["heading"] != TOC_HEADING:
            indent = "  " * (item["level"] - 1)
            toc += f"{indent}- [{item['heading']}]({item['link']})\n"
    toc += "\n" + MD_TOC_TOKEN_END + "\n" * CR_QTY_AFTER_TOC
    return toc


def toc_exists(file: str) -> bool:
    """ Check if file already has a md-toc.

    Parameters
    ----------
    file : str

    Returns:
    --------
    toc_exists : bool 
    """

    lines = file.split("\n")

    for line in lines:
        if line.startswith(MD_TOC_TOKEN_START):
            return True
    return False
        
    
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
    
    print(f"Overwriting TOC between {start} and {end}")

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


if __name__ == "__main__":
    main()
    
