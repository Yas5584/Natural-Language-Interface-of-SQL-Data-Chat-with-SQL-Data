import sqlite3

connection=sqlite3.connect("student.db")

cursor=connection.cursor()

table_info="""
 create table STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),SECTION VARCHAR(25),MARKS INT)
"""

cursor.execute(table_info)

cursor.execute('''INSERT Into STUDENT values('YASH','DATASCIENCE','A',90)''')
cursor.execute('''INSERT Into STUDENT values('RAM','NLP','A',100)''')
cursor.execute('''INSERT Into STUDENT values('MOHAN','DATASCIENCE','C',70)''')
cursor.execute('''INSERT Into STUDENT values('SOHAN','DATASCIENCE','A',76)''')
cursor.execute('''INSERT Into STUDENT values('ANJALI','DATASCIENCE','A',90)''')

print("Showing all Data from tables")
data=cursor.execute('''select * from STUDENT''')
for row in data:
    print(row)

connection.commit()
connection.close()
