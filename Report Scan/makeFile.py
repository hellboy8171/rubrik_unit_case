import re
import pandas as pd

def parse_log_file(log_file_path):
    # Define a list to store the extracted data
    data = []

    # Regex pattern to match each file entry in the log
    pattern = re.compile(r"(?P<name>\/data\/col1\/[^\s]+):(?P<timestamp>\d+):(?P<type>[^:]+):(?P<field1>\d+):(?P<field2>\d+):.*mtime: (?P<mtime>\d+) fileid: (?P<fileid>\d+) size: (?P<size>\d+) type: (?P<type_num>\d+) seg_bytes: (?P<seg_bytes>\d+) seg_count: (?P<seg_count>\d+) redun_seg_count: (?P<redun_seg_count>\d+) \(\d+%\) pre_lc_size: (?P<pre_lc_size>\d+) post_lc_size: (?P<post_lc_size>\d+) \(\d+%\) mode: (?P<mode>\d+)")

    with open(log_file_path, 'r') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                data.append(match.groupdict())

    # Convert data to a DataFrame
    df = pd.DataFrame(data)
    
    # Convert specific columns to numeric values for correct data types
    numeric_columns = ['timestamp', 'mtime', 'fileid', 'size', 'seg_bytes', 'seg_count', 'redun_seg_count', 'pre_lc_size', 'post_lc_size', 'mode']
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric)
    return df



def apply_formula(fileData, output_file_path):
    # Specify the columns to drop
    columns_to_drop = ['timestamp', 'type', 'field1', 'field2', 'type_num', 'mode'] 

    # Drop the specified columns
    fileData = df.drop(columns=columns_to_drop, errors='ignore')
    # fileData = df
    fileData['Last written date'] = (((fileData['mtime']/1000000000)+(-6*3600))/86400)+25569
    fileData['Last written date'] = pd.to_datetime(fileData['Last written date'], origin='1899-12-30', unit='D')
    fileData['Last written date'] = fileData['Last written date'].dt.strftime('%d-%m-%Y')
    ## conversion for column K
    fileData['Global compression'] = fileData.apply(lambda row: 0 if row['pre_lc_size'] == 0 else row['size'] / row['pre_lc_size'], axis=1).round(1)

    ## conversion for column L
    fileData['Local compression'] = fileData.apply(lambda row: 0 if row['post_lc_size'] == 0 else row['pre_lc_size'] / row['post_lc_size'], axis=1).round(1)
    fileData['Overall compression'] = (fileData['Global compression'] * fileData['Local compression']).round(1)

    # Save to Excel
    try:
        fileData.to_excel(output_file_path, index=False)
        print(f"Data successfully saved to {output_file_path}")
    except Exception as e:
        print(f"An error occurred while saving to Excel: {e}")
    # fileData.to_excel(output_file_path, index= False)


# Paths to the input and output files
log_file_path = "C:\\Users\\rajat\\OneDrive\\Desktop\\VS code\\Report Scam\\report.log"
output_file_path = 'output.xlsx'

retention_frame = ['GOLD','SILVER']


# Parse the log file and save to Excel
df = parse_log_file(log_file_path)
if not df.empty:
    apply_formula(df, output_file_path)
else:
    print("No data extracted; skipping Excel save.")
