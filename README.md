# mytaxi-scraper
*A tool that scrapes metadata out of mytaxi receipt pdfs.*

## Problem
If you use taxis a lot in germany, and use mytaxi for this purpose, these receipts will appear familiar to you:

![Demo](demo.png)


This tool extracts meta information from these PDF receipts for further analysis

## Usage

### Extract data

1. Make sure you have python3
2. Install `pdfminer.six` (`pip3 install pdfminer.six`)
3. Prepare a directory that contains your pdf files
4. `python3 write_json.py <<path/to/directory/with/trailing/slash/>>`
5. You have a `metadata.json` file with the metadata for all your taxi rides


### Show time/ride frequency

Exactly as the extract script, but
`python3 analyze.py <<path/to/directory/with/trailing/slash/>>`


### Use as library in your own program
Copy the file `extract.py` into your python project, then:

```
from extract import parse_bill

metadata = parse_bill('path/to/my/bill.pdf')
print(metadata) 

```
