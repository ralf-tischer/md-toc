# MD-TOC

| Ralf Tischer 2024-2025

A command line tool to automatically create tables of content (TOC) for markdown files with the file extension `.md`. 

<!-- MD-TOC START LEVEL 99 -->

## Table of Contents

  - [Usage](#usage)
    - [Clone Script](#clone-script)
    - [Run Script](#run-script)
    - [Prepare Markdown File](#prepare-markdown-file)
    - [Include External TOCs](#include-external-tocs)
  - [Examples](#examples)
  - [Author](#author)

<!-- MD-TOC END -->

## Usage

### Clone Script

Copy `md_toc.py` to main path of local directory. 

* Fork

Fork this repository in GitHub and `git clone` into a local folder. 

* Standard

  ```bash
  wget https://raw.githubusercontent.com/ralf-tischer/md-toc/main/md_toc.py
  ```

* Powershell

  In Powershell use `Invoke-WebRequest -Uri` to download:

  ```bash
  Invoke-WebRequest -Uri "https://raw.githubusercontent.com/ralf-tischer/md-toc/main/md_toc.py" -OutFile "md_toc.py"
  ```
### Run Script

Start _MD-TOC_ from command line. 
```bash
python ./md_toc.py -f README.md
```

Options:
* `-f` or `--files`: list of files, optional
* `-p` or `--paths`: list of paths, optional
* `-s` or `--sub`: if set, browse all paths sub-directories, optional
* `-l` or `--level`: maximum level of headings to be included to TOC, optional, default=99
* `-v` or `--verbose`: print some details to console 

When finished, delete the local copy of _MD-TOC_:
```bash
rm md_toc.py
```

### Prepare Markdown File

The _MD-TOC_ script browses through the markdown file and search for (not printed) tokens. These tokens mark beginning and end of an existing table of content. 
If the tokens are found, _MD-TOC_ starts parsing after the end token. So any heading before the TOC - including the title - will not be included to the new TOC.
If not set, the tokens are automatically added by the script and the TOC is placed at the beginning of the file. 
Alternatively, the `START` and `END` tokens can be placed in the file manually. Level specifies the number of heading levels to be included to the TOC:

```bash
<!-- MD-TOC START LEVEL 3 -->

All text between the tokens will be overwritten by the new table of content.

<!-- MD-TOC END -->

``` 
### Include External TOCs

_MD-TOC_ can include tables of content from external files. This allows to collect anchor links from several different files in the current TOC like bookmarks.
External tables are included into the main TOC. Each has its own level of detail to be displayed. 
External TOCs are simplified in a way that further sub-TOCs will be ignored (no recursion will appear).

The invisible `INCLUDE` tokens are placed between `START` and `END` and specify filename (including relative path, if there is any) and `LEVEL`. 

```bash
<!-- MD-TOC START LEVEL 3 -->
<!-- MD-TOC INCLUDE details.md LEVEL 3 -->
<!-- MD-TOC INCLUDE more/details_db.md LEVEL 2 -->

All text between the tokens will be overwritten by the new table of content.

<!-- MD-TOC END -->
```

## Examples

Create TOC for `README.md` and `describe.py` to level 3:
```bash
python ./md_toc.py -f README.md describe.py --level 3
```

Create TOC for all `.md` files in current directory with all levels:
```bash
python ./md_toc.py -p "."
```

Create TOC for all `.md` files in `path/` directory including all subdirectories with all levels:
```bash
python ./md_toc.py -p "path/" -s
```
## Author

| Ralf Tischer, 2024-2025

