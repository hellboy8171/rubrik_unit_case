import pandas as pd
import sys

def filter_and_process_csv(input_file_path, output_file_path, clusterName):
    try:
        # Read the CSV file
        df = pd.read_csv(input_file_path)

        # Define and apply the filters
        filtered_df = df[(df['Task Status'].isin(['Succeeded', 'Succeeded with Warnings']) ) &
                         (df['Cluster Name'].str.lower() == clusterName) &
                         (df['Task Type'].isin(['Log Backup', 'Backup']))]
        # Select only the columns needed
        columns_to_keep = ['Cluster Name', 'Task Type', 'Task Status', 'Object Name', 'Object Type', 'Location', 'Duration']
        filtered_df = filtered_df[columns_to_keep]
        filtered_df.to_csv("abc.csv", index=False)

        # Drop duplicates based on 'Object Type'
        unique_filtered_df = filtered_df.drop_duplicates(subset=['Object Type'])
        print(unique_filtered_df)

        # Define a function to return appropriate values based on 'Object Type'
        def get_values(row):
            if row['Object Type'] == 'vSphere VM':
                return pd.Series({'Object Type': row['Object Type'], 'Hostname': row['Object Name'], 'Duration': row['Duration']})
            else:
                return pd.Series({'Object Type': row['Object Type'], 'Hostname': row['Location'], 'Duration': row['Duration']})

        # Apply the function to the DataFrame
        result_df = unique_filtered_df.apply(get_values, axis=1)

        # Save the result to a new CSV file
        result_df.to_csv(output_file_path, index=False)

        print("Filtered and processed data saved to:", output_file_path)

    except FileNotFoundError:
        print("Error: Input file not found.")
    except Exception as e:
        print("An error occurred:", str(e))

# Example usage:
input_path = "duration_report.csv"
output_path = "output.csv"
clusterName = "pdctestrubrik01"

filter_and_process_csv(input_path, output_path, clusterName)