import pandas

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
df = pandas.read_excel('cdr_new.xlsx',header=3)
ndf=df[['StartDate', 'CALL TIME','FIRST_CELL_ID','LAST_CELL_ID']].copy()
ndf=ndf.dropna() 

ndf.to_sql("CDR", connection, if_exists="replace")


sql_command = """SELECT DISTINCT First_Cell_ID FROM CDR;""" 
cursor.execute(sql_command)
init_cell=cursor.fetchall()
print('Distinct Initial Cell IDs are')
new_init = [element for tupl in init_cell for element in tupl]
print(new_init)
print(' ')
sql_command = """SELECT DISTINCT Last_Cell_ID FROM CDR;""" 
cursor.execute(sql_command)
fin_cell=cursor.fetchall()

print('Distinct Final Cell IDs are')
new_fin = [element for tupl in fin_cell for element in tupl]
print(new_fin)
print(' ')
print('Total Distinct Cell IDs are')
comb=new_init + new_fin
print set(comb)
connection.close()

    



    

