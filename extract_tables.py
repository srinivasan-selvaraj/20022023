import pdfplumber
import pandas as pd


def extract_tables_from_pdf(file_path):
    extracted_tables = {}
    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            # Extract tables from the page
            tables = page.extract_tables()
            page_no = f'page_{i+1}'
            tables_dict = {}
            # Iterate through the tables and append them to the list
            for j, table in enumerate(tables):
                df = pd.DataFrame(table)
                df = df.rename(columns=df.iloc[0]).drop(df.index[0]).reset_index(drop=True)
                table_no = f'table_{j+1}'
                tables_dict[table_no] = df
            extracted_tables[page_no] = tables_dict
    return extracted_tables


def get_sheet_names(filename):
    # Read the first few rows of the CSV file to determine the headers
    with open(filename, 'r') as file:
        # Read the first few lines to identify headers
        headers = []
        for _ in range(5):  # Read the first 5 rows
            line = file.readline().strip()
            if line:  # Skip empty lines
                headers.append(line)
            else:
                break

    return headers

# dict_pdf_tables = extract_tables_from_pdf("C:/Users/PrasanaKumar/Documents/cmp_src/source_tables.pdf")
# print(dict_pdf_tables)

def extract_tables_from_csv(filename):
    # Read the first sheet
    df = pd.read_csv(filename)
    print(df.head())
    return True


dict_csv_tables = extract_tables_from_csv("C:/Users/PrasanaKumar/Documents/cmp_src/test_csv.csv")
print(dict_csv_tables)
