import pdfplumber
import pandas as pd
import argparse
import os

def extract_tables_from_pdf(file_path):
    extracted_text = []
    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            texts = page.extract_text_lines()
            extracted_txt = [i.get("text") for i in texts]
            tables_ = []
            for j, table in enumerate(tables):
                df = pd.DataFrame(table)
                columns_string = ' '.join(df.iloc[0].astype(str))
                tables_.append(columns_string)
            extracted_text.append((extracted_txt,tables_))        
    return extracted_text

def separate_text_and_table(data_col):
    # Find the index where the table starts
    data,col = data_col
    table_start_index = None
    for i, item in enumerate(data):
        if col[0] in item:
            table_start_index = i
            break

    if table_start_index is not None:
        # Separate text and table
        text = data[:table_start_index]
        table = data[table_start_index:]
        return text, table
    else:
        # If the table start is not found, return None
        return None, None

# Example data
def main():
    parser = argparse.ArgumentParser(description="Convert PDF to Excel")
    parser.add_argument("path_doc", type=str, help="Path to input PDF file")
    parser.add_argument("output_path", type=str, help="Path to output Excel file")
    args = parser.parse_args()

    # Check if the input file is a PDF and output file has the .xlsx extension
    if not args.path_doc.lower().endswith('.pdf'):
        print("Error: Input file must be a PDF.")
        return
    if not args.output_path.lower().endswith('.xlsx'):
        print("Error: Output file must have a .xlsx extension.")
        return

    # Check if input PDF file exists
    if not os.path.exists(args.path_doc):
        print("Error: Input PDF file not found.")
        return
    
    path_doc = args.path_doc
    output_path = args.output_path

    table_df = []
    list_data = extract_tables_from_pdf(path_doc)
    table_text = []
    for data_col in list_data:

        # Separate text and table
        text, table = separate_text_and_table(data_col)

        # Print the separated text and table
        if text is not None and table is not None:
            text_line = text[0]
            columns = table[0].split()  # Extract column names from the first element
            rows = [line.split() for line in table[1:]]  # Split each line to create rows
            df = pd.DataFrame(rows, columns=columns)
            if table_df:
                if "Continued" in text_line:
                    length = len(table_df)
                    merged_df = pd.concat([table_df[length-1], df], ignore_index=True)
                    table_df[length-1] = merged_df
                else:
                    table_df.append(df)
                    table_text.append(text_line)

            else:
                table_df.append(df)
                table_text.append(text_line)
                
        else:
            print("Table start not found in data.")


    excel_writer = pd.ExcelWriter(output_path, engine='xlsxwriter')

    # Iterate through each DataFrame and corresponding sheet name
    for df, sheet_name in zip(table_df, table_text):
        # Write the DataFrame to Excel
        df.to_excel(excel_writer, sheet_name=sheet_name, index=False)

    # Save the Excel file
    excel_writer.close()

if __name__ == "__main__":
    main()

#python pdf_to_excel_converter.py "C:/Users/PrasanaKumar/Documents/cmp_src/EmployeeDetails2.pdf" "C:/Users/PrasanaKumar/Documents/cmp_src/Output.xlsx"



# convert the output in sheet xlsx
# sheet name is table name
# terminal args path - output and input
