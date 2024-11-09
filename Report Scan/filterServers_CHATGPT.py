# hostname = ['172.20.233.197:/A5T-NFS-sapmnt', '\\156.82.232.169\smbtest', '172.20.233.197:/AET-NFS-sapmnt', '\\scussmb04-4702.corp.pep.pvt\NAB-keymaster', '\\scussmb10-5f5c.corp.pep.pvt\edap-ar-prod', '\\bkr-usrdcisilon01.corp.pep.pvt\hdcrossdockdev$', 'pepxap01204-bkr.corp.pep.pvt' ]


import re

# Input list of hostnames
hostname = [
    '//172.20.233.197:/A5T-NFS-sapmnt',
    '\\156.82.232.169\\smbtest',
    '172.20.233.197:/AET-NFS-sapmnt',
    '\\scussmb04-4702.corp.pep.pvt\\NAB-keymaster',
    '\\scussmb10-5f5c.corp.pep.pvt\\edap-ar-prod',
    '\\bkr-usrdcisilon01.corp.pep.pvt\\hdcrossdockdev$',
    'pepxap01204-bkr.corp.pep.pvt',
    'pepxap01204-bk.corp.pep.pvt',
    'pepxap01204-BK.corp.pep.pvt',
    'pepxap01204-BKR.corp.pep.pvt',
    'BK-pepxap01204-BKR.corp.pep.pvt',
    'BKr-pepxap01204-BKR.corp.pep.pvt',
    '172.20.233.197///./A5T-NFS-sapmnt',
    '172.20.233.197\\--/A5T-NFS-sapmnt'
]


# Function to extract the required parts
def extract_parts(data):
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
    # Remove duplicates while preserving order
    result = list(dict.fromkeys(result))
    return result
result = extract_parts(hostname)
print(result)


# import re

# first_part = re.sub(r'-bk|-bkr|\\|//|bkr-', '', str(entry).lower().split('.')[0])
# first_part = first_part[:-1] if first_part and first_part[-1] in {'r', 'p'} else first_part



# output = ['172.20.233.197', '156.82.232.169', '172.20.233.197', 'scussmb04-4702', 'scussmb10-5f5c', 'usrdcisilon01', 'pepxap01204']






