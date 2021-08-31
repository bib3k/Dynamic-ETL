import DateTime
import datetime
import numpy as np
import pandas as pd
data_frame1= pd.read_excel(r'C:\Users\bibek\PycharmProjects\pythonProject1\department3.xlsx')
df0 = pd.DataFrame(data_frame1, columns=['Date of Manufacture', 'Container Type'])
df0['Count'] = 1
df = df0.groupby(['Date of Manufacture', 'Container Type']).Count.count().reset_index()
df1 = df.pivot(*df).fillna(0)
grp = df1.groupby(pd.Grouper(freq='Y')).sum()
print(grp)
selection ='2'
if selection == '2':
        grp.loc[grp['A1'] > 0, 'A1'] *= 2
        grp.loc[grp['B1'] > 0, 'B1'] *= 3
        grp.loc[grp['C1'] > 0, 'C1'] *= 4

grp1 = grp.reset_index(level="Date of Manufacture")
print(grp1)
grp1['Total'] = grp1['A1'] + grp1['B1'] + grp1['C1']
grp1.loc['Total'] = grp1.sum(numeric_only=True, axis=0)
grp1['Date of Manufacture'] = pd.to_datetime(grp1['Date of Manufacture']).dt.strftime('%Y')
grp1.reset_index(drop=True, inplace=True)
grp1.iloc[-1, grp1.columns.get_loc('Date of Manufacture')] = 'Total'

print(grp1)
print(grp1.info())
print(grp1['Total'].sum())
print(grp1['Total'].iloc[-1])