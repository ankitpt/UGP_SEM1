import sqlite3
import pandas as pd

connection = sqlite3.connect("ct_id.db")

cursor = connection.cursor()

l=set(comb)

sql_query = 'select * from CT_ID where CELL_ID in (' + ','.join(map(str, l)) + ')'

cursor.execute(sql_query)

l = cursor.fetchall()
labels=['temp','Cell_ID','Lat','Long','Track_ID','Station_1','Station_2']

connection.close()

df = pd.DataFrame.from_records(l,columns=labels)
del df['temp']
df.to_csv('result.csv',index=False)