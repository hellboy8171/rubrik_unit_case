#### Version 3 notes #### Last Modified Date: August 13th, 2024 ###
## Rubrik Input file changed from CDM to RSC so, we need to modify the Column names in the Rubrik sections
# This is the last version modified by Nacho on August 13 2024 

import pandas as pd
import numpy as np
import re
import glob

## Get Rubrik Object Protection input ##
# rubrik_objects_input = input("Enter Rubrik object report file path ...")
# DDSFS_objects_input= input("Enter DD SFS folder path ...")


rubrik_objects_input = 'C:\\rajat\\Rubrik Object Capacity Report_Dashboard'
DDSFS_objects_input= 'C:\\rajat\\merifile\\'

## Parse Rubrik input file 
rubrik_DB_objects_df = pd.read_csv(rubrik_objects_input, usecols = ['Cluster','ObjectName','ObjectType','Location','LocalStorage','ArchiveStorage'])
rubrik_VM_objects_df = pd.read_csv(rubrik_objects_input, usecols = ['Cluster','ObjectName','ObjectType','Location','LocalStorage','ArchiveStorage'])



### Process Rubrik input file for DBs only, in other section SQL and VMs will be processed
rubrik_DB_objects_df.Location = rubrik_DB_objects_df.Location.astype(str)
rubrik_DB_objects_df = rubrik_DB_objects_df[rubrik_DB_objects_df.ObjectType.isin(["SQL Server DB","Oracle DB","SAP HANA Database"])]
rubrik_DB_objects_df['hostname'] = rubrik_DB_objects_df['Location'].str.extract(r"^([^\.]+)")
rubrik_DB_objects_df['hostname'] = rubrik_DB_objects_df['hostname'].str.replace('-bk','').str.replace('-bkr','')
rubrik_DB_objects_df['hostname'] = rubrik_DB_objects_df['hostname'].apply(lambda x: x[:-1] if x[-1] == 'r' else x)
rubrik_DB_objects_df['hostname'] = rubrik_DB_objects_df['hostname'].apply(lambda x: x[:-1] if x[-1] == 'p' else x)
rubrik_DB_objects_df['hostname'] = rubrik_DB_objects_df['hostname'].str.upper()
rubrik_DB_objects_df.to_excel(r'C:\Users\80319757\OneDrive - Pepsico\Reports\Billing\cost_per_server-July2024\output\rbk_db_objects.xlsx', index=False)
cost_per_db_df_summary = rubrik_DB_objects_df.groupby('hostname').agg({'LocalStorage': 'sum'}).reset_index()
cost_per_db_df_summary.to_excel(r'C:\Users\80319757\OneDrive - Pepsico\Reports\Billing\cost_per_server-July2024\output\cost_db_servers.xlsx', index=False)

## Process Rubrik input file for VMs only
rubrik_VM_objects_df.ObjectName = rubrik_VM_objects_df.ObjectName.astype(str)
rubrik_VM_objects_df = rubrik_VM_objects_df[rubrik_VM_objects_df.ObjectType.isin(["vSphere VM"])]
rubrik_VM_objects_df['hostname'] = rubrik_VM_objects_df['ObjectName'].str.extract(r"^([^\.]+)")
rubrik_VM_objects_df['hostname'] = rubrik_VM_objects_df['hostname'].str.replace('-bk','').str.replace('-bkr','')
rubrik_VM_objects_df['hostname'] = rubrik_VM_objects_df['hostname'].apply(lambda x: x[:-1] if x[-1] == 'r' else x)
rubrik_VM_objects_df['hostname'] = rubrik_VM_objects_df['hostname'].apply(lambda x: x[:-1] if x[-1] == 'p' else x)
rubrik_VM_objects_df['hostname'] = rubrik_VM_objects_df['hostname'].str.upper()
cost_per_vm_df_summary = rubrik_VM_objects_df.groupby('hostname').agg({'LocalStorage': 'sum'}).reset_index()
cost_per_vm_df_summary.to_excel(r'C:\Users\80319757\OneDrive - Pepsico\Reports\Billing\cost_per_server-July2024\output\cost_vm_servers.xlsx', index=False)

## Concatenate all Rubrik objects
rbk_cost_per_server_df = pd.concat([cost_per_db_df_summary,cost_per_vm_df_summary])
rbk_cost_per_server_df['Backup GB'] = rbk_cost_per_server_df['LocalStorage']/1024/1024/1024
rbk_cost_per_server_df_summary = rbk_cost_per_server_df.groupby('hostname').agg({'Backup GB': 'sum'}).reset_index()
rbk_cost_per_server_df_summary.to_excel(r'C:\Users\80319757\OneDrive - Pepsico\Reports\Billing\cost_per_server-July2024\output\bkp_cost_per_server.xlsx', index=False)

##################  DD SFS  #########################

# DD SFS clients extraction from input files and simple list creation

all_ddsfs_files = glob.glob(DDSFS_objects_input + "/*.xlsx")
ddfs_list = []
for filename in all_ddsfs_files:
    df_ddsfs = pd.read_excel(filename, index_col= None, header=0)
    ddfs_list.append(df_ddsfs)

ddsfs_objects_df = pd.concat(ddfs_list, axis=0, ignore_index=True)
print(ddsfs_objects_df)
## replace "." "-" "_" by "/" in name column
ddsfs_objects_df['name2'] = ddsfs_objects_df['name'].str.replace(r'[._]', '/')
print(ddsfs_objects_df['name2'])
## this regex get the fourth match of substring between 2 / ##
ddsfs_objects_df['hostname'] = ddsfs_objects_df['name2'].str.extract(r"^(?:\/[^\/]+){3}\/([^\/]+)")
ddsfs_objects_df['hostname'] = ddsfs_objects_df['hostname'].str.split('_').str[0]
ddsfs_objects_df['Backup GB'] = ddsfs_objects_df['post_lc_size']/1024/1024/1024
ddsfs_objects_df_summary = ddsfs_objects_df.groupby('hostname').agg({'Backup GB': 'sum'}).reset_index()

# #### Concatenate both Rubrik and DD SFS then, get the summary.
bkp_cost_server_df = pd.concat([rbk_cost_per_server_df_summary,ddsfs_objects_df_summary])
bkp_cost_server_df['Backup cost'] = bkp_cost_server_df['Backup GB']*0.096
bkp_cost_server_df.to_excel(r'C:\Users\80319757\OneDrive - Pepsico\Reports\Billing\cost_per_server-July2024\output\BKP_cost_summary-July2024.xlsx', index=False)

