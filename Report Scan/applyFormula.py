import pandas as pd
filePath = 'C:\\rajat\\ReportFile.xlsx'
outFilePath = 'C:\\rajat\\ReportFile_output.xlsx'

fileData = pd.read_excel(filePath)
print(fileData)
fileData['Last written date'] = (((fileData['mtime']/1000000000)+(-6*3600))/86400)+25569
fileData['Last written date'] = pd.to_datetime(fileData['Last written date'], origin='1899-12-30', unit='D')
fileData['Last written date'] = fileData['Last written date'].dt.strftime('%d-%m-%Y')

## conversion for column K
fileData['Global compression'] = fileData.apply(lambda row: 0 if row['pre_lc_size'] == 0 else row['size'] / row['pre_lc_size'], axis=1).round(1)

## conversion for column L
fileData['Local compression'] = fileData.apply(lambda row: 0 if row['post_lc_size'] == 0 else row['pre_lc_size'] / row['post_lc_size'], axis=1).round(1)
fileData['Overall compression'] = (fileData['Global compression'] * fileData['Local compression']).round(1)

# save file
fileData.to_excel(outFilePath, index= False)

