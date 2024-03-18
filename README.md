# MD-TOC

A command line tool to automatically create tables of content (TOC) for markdown files with the file extension `.md`. 

<!-- MD-TOC START LEVEL 3 -->
<!-- MD-TOC INCLUDE test/plm.md LEVEL 3 -->

## Table of Contents

  - [Usage](#usage)
    - [Prepare Markdown File](#prepare-markdown-file)
    - [Run Script](#run-script)
  - [Examples](#examples)
  - [Author](#author)

### test/plm.md
  - [BOM Navigator](test/plm.md#bom-navigator)
  - [Commissions](test/plm.md#commissions)
  - [Multi-where-used-analysis](test/plm.md#multi-where-used-analysis)
  - [API](test/plm.md#api)
    - [Items](test/plm.md#items)
    - [Boms](test/plm.md#boms)
  - [Web Application](test/plm.md#web-application)
  - [Files](test/plm.md#files)
    - [app.py](test/plm.md#apppy)
    - [start_server.py](test/plm.md#start_serverpy)
    - [wabtec_erp.py](test/plm.md#wabtec_erppy)
    - [wabtec_commissions.py](test/plm.md#wabtec_commissionspy)
    - [wabtec_itemno.py](test/plm.md#wabtec_itemnopy)
    - [erptest.py](test/plm.md#erptestpy)
    - [find_high_runner_assy.py](test/plm.md#find_high_runner_assypy)
    - [find_double_references.py](test/plm.md#find_double_referencespy)
  - [Usage and examples](test/plm.md#usage-and-examples)
  - [Author](test/plm.md#author)


<!-- MD-TOC END -->

## Usage

### Prepare Markdown File

The _MD-TOC_ script browses through the markdown file and search for (not printed) tokens. These tokens mark beginning and end of an existing table of content. 
If the tokens are found, _MD-TOC_ starts parsing after the end token. So any heading before the TOC - including the title - will not be included to the new TOC.
If not set, the tokens are automatically added by the script and the TOC is placed at the beginning of the file. 
Alternatively, the start and end tokens can be placed in the file manually. Level specifies the number of heading levels to be included to the TOC:

```bash
<!-- MD-TOC START LEVEL 3 -->

All text between the tokens will be overwritten by the new table of content.

<!-- MD-TOC END -->
```

### Run Script

Copy `md_toc.py` to main path of local directory:
```bash
wget https://raw.githubusercontent.com/RalfTischer/md-toc/main/md_toc.py
```

Start _MD-TOC_ from command line. 
```bash
python ./md_toc.py -f README.md
```

Options:
* `-f` or `--files`: list of files, optional
* `-p` or `--paths`: list of paths, optional
* `-s` or `--sub`: if set, browse all paths sub-directories, optional
* `-l` or `--level`: maximum level of headings to be included to TOC, optional, default=99

When finished, delete the local copy of _MD-TOC_:
```bash
rm md_toc.py
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

Ralf Tischer, 2024
