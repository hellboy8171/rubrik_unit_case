import pandas as pd
import sys


def getDifference(dict1, dict2):
    difference = {}
    for key, values in dict1.items():
        if key not in dict2:
            difference[key] = values
        else:
            for value in values:
                if value not in dict2[key]:
                    if key not in difference:
                        difference[key] = []
                    difference[key].append(value)
    if difference:
        return False, difference
    else:
        return True, None


def checkFileCompatibility(filePath1, filePath2, clusterName, targetedVersion):
    try:
        # Load CSV Files
        dataFile1 = pd.read_csv(filePath1)
        dataFile2 = pd.read_csv(filePath2)

        # Filter DataFrame based on the cluster name
        cluster_df = dataFile1[dataFile1["Cluster Name"].str.lower() == clusterName]
        if cluster_df.empty:
            raise ValueError(f"No data found for cluster name: {clusterName}")

        # Extract the workload type from the filtered DataFrame
        workload = cluster_df["Workload Type"].iloc[0]

        # Split the workload type into individual services
        services = [service.strip() for service in workload.split(",")]

        sourceServiceValues = {}
        for service in services:
            service_column = cluster_df[service].iloc[0]
            sourceServiceValues[service] = [
                value.strip() for value in service_column.split(";")
            ]

        targetServiceValues = {}
        version_row = dataFile2.loc[dataFile2["version"] == targetedVersion]
        if version_row.empty:
            raise ValueError(f"No data found for targeted version: {targetedVersion}")

        for service in services:
            service_column = version_row[service].iloc[0]
            targetServiceValues[service] = [
                value.strip() for value in service_column.split(";")
            ]

        result, diff = getDifference(sourceServiceValues, targetServiceValues)
        if result:
            return True
        else:
            return diff
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    # variables assignment from command line arguments
    sourceFilePath = 'sourceFile.csv'
    targetFilePath = 'targetFile.csv'
    clusterName = 'pdctestrubrik01'
    fetchedTargetVersion = '9.1.3-p9-25701'
    targetVersion = fetchedTargetVersion.split("-")[0]
    result = checkFileCompatibility(
        sourceFilePath, targetFilePath, clusterName, targetVersion
    )
    print(result)
