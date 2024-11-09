import pandas as pd
import sys
import re


# Function to extract the required parts
def extract_servers(data):
    result = []
    for entry in data:
        # Extract IP address if present
        entry= str(entry).strip('/\\')
        ip_match = re.match(r'(.+\d+\.\d+\.\d+\.\d+)', entry)
        if ip_match:
            result.append(ip_match.group(1))
        else:
            # Split by '.' or '\\' and take the first part
           first_part = re.sub(r'-bk|-bkr|\\|//|bkr-|bk-', '', str(entry).lower().split('.')[0])
           first_part = first_part[:-1] if first_part and first_part[-1] in {'r', 'p'} else first_part
            # first_part = entry.split('.')[0].split('\\')[0]
           result.append(first_part)
    result = list(dict.fromkeys(result))
    return result


def get_unique_values(file_path, cluster_name):
    try:
        # Load the CSV file
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        sys.exit(1)
    except pd.errors.ParserError:
        print("Error: The file could not be parsed.")
        sys.exit(1)

    # Required columns
    required_columns = [
        "Cluster Name",
        "Object Type",
        "Object Name",
        "Location",
        "Task Type",
    ]
    
    # Check for required columns
    if not all(column in df.columns for column in required_columns):
        print("Error: The CSV file does not contain the required columns.")
        sys.exit(1)

    # Filter DataFrame for the given cluster name and task type
    df_cluster = df[
        (df["Cluster Name"].str.lower() == cluster_name.lower()) & 
        (df["Task Type"].isin(["Backup", "Log Backup"]))
    ]

    # Get unique object names for VMs
    unique_vm_objectnames = df_cluster[df_cluster["Object Type"] == "vSphere VM"]["Object Name"].dropna().unique()

    # Get unique locations for non-VMs
    unique_non_vm_locations = df_cluster[df_cluster["Object Type"] != "vSphere VM"]["Location"].dropna().unique()

    # Combine results
    combined_results = list(unique_vm_objectnames) + list(unique_non_vm_locations)

    result = extract_servers(combined_results)
    return result



def main():
    file_path = sys.argv[1]
    cluster_name = sys.argv[2]
    results = get_unique_values(file_path, cluster_name)
    print(",".join(results))

if __name__ == "__main__":
    main()