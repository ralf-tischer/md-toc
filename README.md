# MD-TOC

A command line tool to automatically create a table of content (TOC) for markdown files with file extension `.md`. 

<!-- MD-TOC START LEVEL 99 -->

# Table of Contents

- [djkjf](#djkjf)
- [First Headline](#first-headline)
  - [Subchapter with Attitude](#subchapter-with-attitude)
  - [Subchapter](#subchapter)
    - [Subchapter](#subchapter)
- [Fun vs. No Fun](#fun-vs.-no-fun)
- [Second, but great Headline](#second-but-great-headline)

<!-- MD-TOC END -->

## Usage

### Prepare Markdown File

The md-toc script will browse through the markdown file and search for (not printed) tokens. These tokens marks beginning and end of an existing table of content. 
The tokens will be added automatically by the script when the TOC is placed at the beginning of the file. 
Alternatively, the start and end tokens can be placed in the file manually. Level specifies the number of heading levels to be included to the TOC:

```bash
<!-- MD-TOC START LEVEL 3 -->

Between the tokens everything will be overwritten.

<!-- MD-TOC END -->
```

### Run Script

Copy `md_toc.py` to main path of local directory:
```bash
wget https://raw.githubusercontent.com/RalfTischer/md-toc/main/md_toc.py
```

Start md-toc from command line. 
```bash
python ./md_toc.py -f README.md
```

Options:
* `-f` or `--files`: list of files, optional
* `-p` or `--paths`: list of paths, optional
* `-s` or `--sub`: if set, browse all paths sub-directories, optional
* `-l` or `--level`: maximum level of headings to be included to TOC, optional, default=99

When finished, delete the local copy of md-toc:
```bash
rm md_toc.py
```

## Examples

Create TOC for `README.md` and `describe.py` to level 3:
```bash
python ./md_toc.py -f README.md describe.py --level 3
```

Create TOC for all .md files in current directory with all levels:
```bash
python ./md_toc.py -p "."
```

Create TOC for all .md files in `path/` directory including all subdirectories with all levels:
```bash
python ./md_toc.py -p "path/" -s
```

# Test Data
fblösd jkldsf bla dhjkf
ksdfjksd
d dlfkoädf
 sdkfjsd


# First Headline
Bal dksj
adlkpoöds

## Subchapter with Attitude
sdfdsf Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.

* Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna 
* aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem 
* ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.

## Subchapter

sdfsd
dsfsdf sfdh sdfjn
Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.

### Subchapter

```bash
dfkjlkfd
sdkjlkdf
ödsf
f #
dsfksdklf
```

# Fun vs. No Fun

sdfsd
dsfsdf sfdh sdfjn
Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.


# Second, but great Headline

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.

```python
# Test
sfdkljlkfd
sdflkjfsd
```

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.
