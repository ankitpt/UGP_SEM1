import sqlite3
import pandas as pd

connection = sqlite3.connect("ct3_id.db")

cursor = connection.cursor()


df = pd.read_csv('idea_towers_stations2.csv')
				

ndf=df[['CGI1', 'Lat','Long','up','down','ID']].copy()

#ndf=df[['StartDate', 'CALL TIME','FIRST_CELL_ID','LAST_CELL_ID']].copy()
#ndf=ndf.dropna() 

ndf.to_sql("TT", connection, if_exists="replace")     

l=set(comb)
l=tuple(l);

placeholder= '?' # For SQLite. See DBAPI paramstyle.
placeholders= ', '.join(placeholder for unused in l)
query= 'SELECT * FROM TT WHERE CGI1 IN (%s)' % placeholders
cursor.execute(query, l)



l2 = cursor.fetchall()
labels=['temp','Cell_ID','Lat','Long','Track_ID','Station_1','Station_2']

connection.close()

df = pd.DataFrame.from_records(l2,columns=labels)
del df['temp']
#df.to_csv('result.csv',index=False)

writer = pd.ExcelWriter('result.xlsx')
df.to_excel(writer,'Sheet1',index=False)
writer.save()