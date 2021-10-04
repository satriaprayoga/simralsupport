import pandas as pd

pd.set_option('display.float_format', lambda x: '%.2f' % x)
data=pd.read_excel('NERACA_AWAL2021.xlsx')
for index, row in data.iterrows():
    print(row['Kode '], row['Satuan Kerja'], row['Sub Unit'])
