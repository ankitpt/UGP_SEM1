import sqlite3
import pandas as pd

connection = sqlite3.connect("ct_id.db")

cursor = connection.cursor()

l=[1417,1418,1419]

sql_query = 'select * from CT_ID where CELL_ID in (' + ','.join(map(str, l)) + ')'

cursor.execute(sql_query)

l = cursor.fetchall()


connection.close()

df = pd.DataFrame({'col':l})