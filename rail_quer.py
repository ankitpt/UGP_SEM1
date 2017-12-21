import sqlite3
import pandas as pd
#Name of Excel xlsx file. SQLite database will have the same name and extension .db
filename="result" 
con=sqlite3.connect(filename+".db")
cursor = con.cursor()
wb=pd.read_excel(filename+'.xlsx',sheetname=None)
for sheet in wb:
    wb[sheet].to_sql(sheet,con, index=False,if_exists="replace")
con.commit()
sql_query = 'select Track_ID from Sheet1'
cursor.execute(sql_query)
l = cursor.fetchall()
l2 = [element for tupl in l for element in tupl]
con.close()

date="24-Feb-17"

filename="trivial_af" 
con=sqlite3.connect(filename+".db")
cursor = con.cursor()
wb=pd.read_excel(filename+'.xlsx',sheetname=None)
for sheet in wb:
    wb[sheet].to_sql(sheet,con, index=False,if_exists="replace")
con.commit()
sql_query = 'select Train_no from Sheet1 where Date="24-Feb-17" AND Track_ID in (' + ','.join(map(str, l2)) + ')'
cursor.execute(sql_query)
l3 = cursor.fetchall()
l4 = [element for tupl in l3 for element in tupl]
con.close()
