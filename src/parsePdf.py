# import pandas
# import pymupdf
# from pprint import pprint


# # Open some document, for example a PDF (could also be EPUB, XPS, etc.)
# doc = pymupdf.open("000A1HMT.pdf")

# # Load a desired page. This works via 0-based numbers
# # page = doc[2]

# data = []

# for page in doc[:2]:
#     tabs = page.find_tables()
#     if tabs.tables:
#         data.append(tabs[0].extract())


# pprint(data[0])

    
# # # Look for tables on this page and display the table count
# # tabs = page.find_tables()
# # print(f"{len(tabs.tables)} table(s) on {page}")

import fitz  # PyMuPDF
import pandas as pd
import os
import glob
import re

def extract_service_dates(text):
    """
    Extract the service dates from the page text.
    """
    match = re.search(r"Service Dates:.*", text)
    return match.group(0) if match else "Service Dates: Not Found"

def extract_tables_from_pdf(pdf_path):
    """Extract tables from a PDF and return a list of DataFrames."""
    doc = fitz.open(pdf_path)
    tables = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        page_text = page.get_text("text")
        service_dates = extract_service_dates(page_text)
        tabs = page.find_tables()
        if tabs:
            for tab in tabs:
                table_text = tab.extract()
                tables.append(table_text)
    return tables

def split_multiline_cells(table):
    """
    Split multiline cells into separate rows.
    """
    # Extract headers
    headers = table[0]
    # Initialize the new table with headers
    new_table = [headers]

    # Iterate over each row except the header
    for row in table[1:]:
        # Split each cell in the row by '\n', replacing None with ''
        split_rows = [cell.split('\n') if cell is not None else [''] for cell in row]

        # Transpose the split cells to form new rows
        for new_row in zip(*split_rows):
            new_table.append(new_row)

    return new_table

def extract_table_text(text):
    """
    Dummy function to demonstrate table extraction logic.
    Replace this with actual table extraction code.
    """
    # Dummy data assuming extracted text in table format
    dummy_table = [
        ["Header1\nLine2", "Header2\nLine2", "Header3\nLine2"],
        ["Row1Col1", "Row1Col2", "Row1Col3"],
        ["Row2Col1", "Row2Col2", "Row2Col3"]
    ]
    return [dummy_table]

def clean_header(headers):
    """
    Clean headers by removing newline characters.
    """
    return [header.replace('\n', ' ') for header in headers]

def tables_to_dataframes(tables):
    """
    Convert tables to Pandas DataFrames with cleaned headers.
    """
    dataframes = []
    for table in tables:
        table = split_multiline_cells(table)
        headers = clean_header(table[0])
        data = table[1:]
        df = pd.DataFrame(data, columns=headers)
        dataframes.append(df)
    return dataframes

def process_pdfs_in_folder(folder_path):
    """
    Process all PDF files in the specified folder.
    """
    pdf_files = glob.glob(os.path.join(folder_path, '*.pdf'))
    
    all_dataframes = []

    for pdf_file in pdf_files:
        print(f"Processing {pdf_file}...")
        tables = extract_tables_from_pdf(pdf_file)
        dataframes = tables_to_dataframes(tables)
        all_dataframes.extend(dataframes)
        #break
    return all_dataframes

# Main code
folder_path = './data'
all_dataframes = process_pdfs_in_folder(folder_path)

# Display DataFrames
for idx, df in enumerate(all_dataframes):
    print(f"Table {idx + 1}:")
    print(df)
