import pymupdf

# Open some document, for example a PDF (could also be EPUB, XPS, etc.)
doc = pymupdf.open("input.pdf")

# Load a desired page. This works via 0-based numbers
page = doc[0]  # this is the first page

# Look for tables on this page and display the table count
tabs = page.find_tables()
print(f"{len(tabs.tables)} table(s) on {page}")