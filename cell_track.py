
import sqlite3
import pandas


df = pandas.read_excel('try3.xlsx')
ndf=df[['Cell_ID', 'Latitude','Longitude','Track ID','Station 1','Station 2']].copy()
ndf=ndf.dropna()

connection = sqlite3.connect("ct_id.db")
cursor = connection.cursor()

# delete 
#cursor.execute("""DROP TABLE  CT_ID;""")



sql_command = """
CREATE TABLE if not exists CT_ID (
Cell_ID VARCHAR(50),
Latitude REAL,
Longitude REAL,
Track_ID INTEGER,
Station_1 TEXT,
Station_2 TEXT 
);"""

cursor.execute(sql_command)




ndf.to_sql("CT_ID", connection, if_exists="replace")
connection.close()