import sqlite3

# Initialize database first (moved to top)
print("Initializing database...")
try:
    connection=sqlite3.connect("STUDENT.db")
    cursor=connection.cursor()
    
    # Check if table exists first
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='STUDENT';")
    table_exists = cursor.fetchone()
    
    if not table_exists:
        #creating the table in sql database
        table_info="""
        CREATE TABLE STUDENT(
            NAME VARCHAR(25),
            CLASS VARCHAR(25),
            SECTION VARCHAR(25),
            MARKS INT
        );
        """
        cursor.execute(table_info)
        
        # inserting example records
        cursor.execute('''INSERT INTO STUDENT VALUES('Veda', 'GenAI', 'A', 90)''')
        cursor.execute('''INSERT INTO STUDENT VALUES('Srija', 'DevOPs', 'B', 68)''')
        cursor.execute('''INSERT INTO STUDENT VALUES('Sirisha', 'OpenCV', 'B+', 70)''')
        cursor.execute('''INSERT INTO STUDENT VALUES('Shiva', 'NodeJS', 'A', 80)''')
        cursor.execute('''INSERT INTO STUDENT VALUES('Anupama', 'PowerBI', 'A+', 100)''')
        
        # commit your changes in the database
        connection.commit()
        print("Database and table created successfully!")
    else:
        print("Table already exists!")
    
    # display the records
    print("The inserted records are:")
    data=cursor.execute('''SELECT * FROM STUDENT''')
    for row in data:
        print(row)
    
    connection.close()
    
except Exception as e:
    print(f"Database error: {e}")



# connection=sqlite3.connect("student.db")

# #cursor
# cursor=connection.cursor()

# #creating the table in sql database
# table_info="""
# CREATE TABLE student(
#     name VARCHAR(25),
#     class VARCHAR(25),
#     section VARCHAR(25),
#     marks INT
# );
# """
# cursor.execute(table_info)

# # inserting example records
# cursor.execute('''INSERT INTO student VALUES('Veda', 'GenAI', 'A', 90)''')
# cursor.execute('''INSERT INTO student VALUES('Srija', 'DevOPs', 'B', 68)''')
# cursor.execute('''INSERT INTO student VALUES('Sirisha', 'OpenCV', 'B+', 70)''')
# cursor.execute('''INSERT INTO student VALUES('Shiva', 'NodeJS', 'A', 80)''')
# cursor.execute('''INSERT INTO student VALUES('Anupama', 'PowerBI', 'A+', 100)''')

# # display the records
# print("The inserted records are::")
# data=cursor.execute('''SELECT * from student''')
# for row in data:
#     print(row)


# # commit your changes in the database
# connection.commit()
# connection.close()