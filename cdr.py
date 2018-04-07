import pandas as pd

import sqlite3
connection = sqlite3.connect("cdr_read.db")

cursor = connection.cursor()

# delete 


sql_command = """
CREATE TABLE if not exists CDR (
Date DATE,
Time_of_communication TIME,
Initial_Cell_ID INTEGER,
Final_Cell_ID INTEGER 
);"""

cursor.execute(sql_command)
df = pd.read_excel('9644346975 idea.xlsx',header=10)

ndf=df[['Date', 'Time','First Cell ID/LOCATION AREA CODE','Last Cell ID / PDP Address']].copy()

#ndf=df[['StartDate', 'CALL TIME','FIRST_CELL_ID','LAST_CELL_ID']].copy()
#ndf=ndf.dropna() 
ndf=ndf.rename(columns = {'Date':'StartDate'})
ndf=ndf.rename(columns = {'Time':'CALL TIME'})
ndf=ndf.rename(columns = {'First Cell ID/LOCATION AREA CODE':'FIRST_CELL_ID'})
ndf=ndf.rename(columns = {'Last Cell ID / PDP Address':'LAST_CELL_ID'})

ndf.to_sql("CDR", connection, if_exists="replace")


sql_command = """SELECT DISTINCT First_Cell_ID FROM CDR;""" 
cursor.execute(sql_command)
init_cell=cursor.fetchall()
print('Distinct Initial Cell IDs are')
new_init = [element for tupl in init_cell for element in tupl]
new_init=[str(k) for k in new_init]

new_init = [x for x in new_init if ('.' not in x and x!='None')]


        
print(new_init)
print(' ')
sql_command = """SELECT DISTINCT Last_Cell_ID FROM CDR;""" 
cursor.execute(sql_command)
fin_cell=cursor.fetchall()

print('Distinct Final Cell IDs are')
new_fin = [element for tupl in fin_cell for element in tupl]
new_fin=[str(k) for k in new_fin]
new_fin = [x for x in new_fin if ('.' not in x and x!='None')]


        

print(new_fin)
print(' ')
print('Total Distinct Cell IDs are')
comb=new_init + new_fin
print set(comb)
connection.close()

    



    

