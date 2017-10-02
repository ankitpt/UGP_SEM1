import pandas

import sqlite3
connection = sqlite3.connect("cdr_read.db")

cursor = connection.cursor()

# delete 
cursor.execute("""DROP TABLE CDR;""")

sql_command = """
CREATE TABLE CDR (
Date DATE,
Time_of_communication TIME,
Initial_Cell_ID INTEGER,
Final_Cell_ID INTEGER 
);"""

cursor.execute(sql_command)
df = pandas.read_excel('cdr_raw.xlsx',header=3)
ndf=df[['StartDate', 'CALL TIME','FIRST_CELL_ID','LAST_CELL_ID']].copy()

#sql_command = """INSERT INTO CDR (Date, Time of communication, Mode of communication,Initial Cell ID,Final Cell ID)
 #   VALUES ( df['StartDate'], df['CALL TIME'],df['TYPE OF CONNECTION'],df['FIRST_CELL_ID'],df['LAST_CELL_ID'] );"""
#cursor.execute(sql_command)
#connection.close()

for row in ndf.iterrows():
    format_str = """INSERT INTO CDR VALUES ("{first}", "{last}", "{birthdate}","{random}");"""

    sql_command = format_str.format(first=row[1][0], last=row[1][1], birthdate = row[1][2],random=row[1][3])
    cursor.execute(sql_command)
    connection.commit()

sql_command = """SELECT DISTINCT Initial_Cell_ID FROM CDR;""" 
cursor.execute(sql_command)
init_cell=cursor.fetchall()
print('Distinct Initial Cell IDs are')
print(init_cell)

sql_command = """SELECT DISTINCT Final_Cell_ID FROM CDR;""" 
cursor.execute(sql_command)
fin_cell=cursor.fetchall()
print('Distinct Final Cell IDs are')
print(fin_cell)

print('Total Distinct Cell IDs are')
comb=init_cell + fin_cell
print list(set(comb))
connection.close()    

    

