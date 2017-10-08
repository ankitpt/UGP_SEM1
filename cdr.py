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
df = pandas.read_excel('cdr_raw.xlsx',header=3)
ndf=df[['StartDate', 'CALL TIME','FIRST_CELL_ID','LAST_CELL_ID']].copy()
ndf=ndf.dropna() 
#sql_command = """INSERT INTO CDR (Date, Time of communication, Mode of communication,Initial Cell ID,Final Cell ID)
 #   VALUES ( df['StartDate'], df['CALL TIME'],df['TYPE OF CONNECTION'],df['FIRST_CELL_ID'],df['LAST_CELL_ID'] );"""
#cursor.execute(sql_command)
#connection.close()

ndf.to_sql("CDR", connection, if_exists="replace")





sql_command = """SELECT DISTINCT First_Cell_ID FROM CDR;""" 
cursor.execute(sql_command)
init_cell=cursor.fetchall()
print('Distinct Initial Cell IDs are')
print(init_cell)
print(' ')
sql_command = """SELECT DISTINCT Last_Cell_ID FROM CDR;""" 
cursor.execute(sql_command)
fin_cell=cursor.fetchall()
print('Distinct Final Cell IDs are')
print(fin_cell)
print(' ')
print('Total Distinct Cell IDs are')
comb=init_cell + fin_cell
print list(set(comb))
connection.close()    

    

