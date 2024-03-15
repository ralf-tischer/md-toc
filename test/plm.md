# PLM Tools

Tools for data preparation and other tasks related to PLM coded in Python.

Link: [PLM Tools](http://bocdsk0006:5555/)


<!-- MD-TOC START LEVEL 3 -->

# Table of Contents

- [PLM Tools](#plm-tools)
  - [BOM Navigator](#bom-navigator)
  - [Commissions](#commissions)
  - [Multi-where-used-analysis](#multi-where-used-analysis)
  - [API](#api)
    - [Items](#items)
    - [Boms](#boms)
  - [Web Application](#web-application)
  - [Files](#files)
    - [app.py](#app.py)
    - [start_server.py](#start_server.py)
    - [wabtec_erp.py](#wabtec_erp.py)
    - [wabtec_commissions.py](#wabtec_commissions.py)
    - [wabtec_itemno.py](#wabtec_itemno.py)
    - [erptest.py](#erptest.py)
    - [find_high_runner_assy.py](#find_high_runner_assy.py)
    - [find_double_references.py](#find_double_references.py)
  - [Usage and examples](#usage-and-examples)
  - [Author](#author)

<!-- MD-TOC END -->


## BOM Navigator

* Link: [BOM Navigator](http://bocdsk0006:5555/bomnavigator)
* Drag or enter an item number or drawing number. Wrong entries will be corrected to a certain degree.
* Left side: material information taken each night from M3/MMS001. 
* Right side: Switch the display between BOM data, where-used-anaylsis (parents on next level), commission data (taken from a static image of the commission database) or Multi-level BOM (to be loaded first).
* Click on any item number to set the focus on it.

## Commissions

* Link: [Commissions](http://bocdsk0006:5555/commissions)
* Choose your search pattern:
    * Project name/ number: [Projekt] LIKE %input% OR [Kunde] LIKE %input% OR [Projektnummer] LIKE input OR [Anmerkung] LIKE %input%
    * WABTEC item number/ drawing: [Ident-Nr] LIKE input%
    * WABTEC product type: [Produkttyp] LIKE input%
* Drag or enter your search term. The prefix "D"  for item numbers will be surpressed due to the format of the commssion data.
* Below find the commission data (taken from a static image of the commission database).

## Multi-where-used-analysis

* Link [Multi-where-used-analysis](http://bocdsk0006:5555/findref)
* Drag or enter an item number or drawing number. Wrong entries will be corrected to a certain degree.
* Choose what to do:
    * Add item to existing search (default).
    * Start a new search.

The found references on the highest level of the where-used-analysis are compared. The intersection set for all search items is provided as the result of the search. For example:

![Highest reference](<helper/Highest reference.jpg>)

## API
API ([Application Programming Interface](https://en.wikipedia.org/wiki/API)) to access some core functions remotely.

### Items
Access the internal function ´guess_wabtec_item_no´ (see in Files section below below). The API gives back a corrected version as [JSON](https://en.wikipedia.org/wiki/JSON) of a faulty item number or of a drawing number. 

Usage:

```bash
http://bocdsk0006:5555/items?itemno=123456
```

### Boms
Access the internal BOM functions. The API typically gives back a [JSON](https://en.wikipedia.org/wiki/JSON) of a list. 

Parameters:

* `itemno` : str
* `action` : str
    * `bom`: simple BOM
    * `bom_ml`: multilevel BOM
    * `where_used`: where-used-analysis
    * `references`: parents on highest level
* `maxlevel` : int, default=99
    max. BOM levels upwards or downnwards.

Usage:

```bash
http://bocdsk0006:5555/boms?itemno=D123456-100&action=bom
```
```bash
http://bocdsk0006:5555/boms?action=bom_ml&itemno=D123456-100
```
```bash
http://bocdsk0006:5555/boms?itemno=D109597-020&action=where_used&maxlevel=2
```

## Web Application

A [Flask](https://flask.palletsprojects.com/) application provides a user interface to access WABTEC data (item data, BOMs, commissions). 
The Flask app is run as a [Waitress](https://flask.palletsprojects.com/en/3.0.x/deploying/waitress/) production server. 

Start productive server `bocdsk0006`: 
```bash
python ".\start_server.py"
```

Start development server `bocdsk0006`: 
```bash
flask run -h 0.0.0.0 -p 5555 --debug
```

Client access: 
```bash
http://bocdsk0006:5555/
```


## Files
### app.py
Flask app to run API and web interface.

### start_server.py
Little script to run the `app.py` as a waitress server.

### wabtec_erp.py
Methods for Wabtec ERP data.

The ERP BOM data is imported from an Excel file or read from an SQL database. The item data is taken from an SQL database. The SQL databases are stored in the Wabtec network and automatically updated each night.

#### Classes
- `Boms`: Methods related to BOMs
- `Items`: Methods related to items 

### wabtec_commissions.py
Methods for Wabtec commission data.

Wabtec commission data was extracted to an [sqlite3](https://www.sqlite.org/) database and stored in the file system.

#### Classes
- `CommSql`: Methods related to commission data in SQL

### wabtec_itemno.py
Methods related to Wabtec item number.

#### Routines
- `guess_wabtec_item_no`: Guess correct Wabtec item number out of wrong input.

### erptest.py
Unit test for wabtec_erp.py. 
```bash
python -m unittest -v erptest                       # All
python -m unittest -v erptest.TestBoms              # Class TestBoms
python -m unittest -v erptest.TestItemNo            # Class TestItemoNo
python -m unittest -v erptest.TestBoms.test_bom_ml  # Class TestBoms: function test_bom_ml
```

### find_high_runner_assy.py
Find references in an Excel list and return a value if no further reference is found. A small tools reading item and BOM data from two Excel files defined as constants.

### find_double_references.py
Find double references on lowest BOM level. A small tool for counting unique BOM references (children) and counting duplicates for a number of items in an Excel file. 

## Usage and examples

```python
from wabtec_erp import Boms, Items
from wabtec_commissions import CommSql
from wabtec_itemno import guess_wabtec_item_no

bom_data = Boms()       # Read Boms
item_data = Items()     # Prepare item connection

# Item data
material = item_data.data(item)
if material == {}:
    item = guess_wabtec_item_no(item)
    material = item_data.data(item) # Try again with improved input

# Simple BOM
bom = sorted(bom_data.bom(item), key=lambda d: int(d["pos"]))

# Multi-level BOM
bom_ml = bom_data.bom_ml(item)
# Sort by level, root, pos
bom_ml = sorted(bom_ml, key=lambda d: int(d["pos"]))
bom_ml = sorted(bom_ml, key=lambda d: d["root"])
bom_ml = sorted(bom_ml, key=lambda d: int(d["level"]))

# Parents
parents = sorted(bom_data.parents(item), key=lambda d: d["parent"])

# Commissions
comm_data = CommSql()    # Prepare commission connection
names, commissions = comm_data.query_by_itemno(item)    # Get names and properties
# names, commissions = comm_data.query_by_project(input)
# names, commissions = comm_data.query_by_product_type(input)
```

## Author
Ralf Tischer
2023-2024
