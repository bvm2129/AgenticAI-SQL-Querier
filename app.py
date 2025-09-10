# app.py

from dotenv import load_dotenv
load_dotenv() # load all the environment variables
import streamlit as st
import os
import sqlite3
import google.generativeai as genai

# configure your API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#function to load google model and provide sql query as a response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    response=model.generate_content([prompt[0], question])
    return response.text

# function to retrieve query from the database
def read_sql_query(sql, db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
   
    for row in rows:
        print(row)
    return rows

# define your prompt
prompt=[
    """
    You are an expert AI assisstant specializing in converting natural language questions to sql queries.
    The SQL Database is name **STUDENT** and contains the following columns:
    - **NAME** (VARCHAR)
    - **CLASS** (VARCHAR)
    - **SECTION** (VARCHAR)
    - **MARKS** (INT)
    Follow these guidelines when gwnerating SQL Queries:
    1. Ensure the output contains only the SQL query, do not include explanations, formatting, markdowns.
    2. Use proper SQL syntax while maintaining accuracy and efficiency.
    3. If the query involves filtering, apply appropriate "WHERE" clauses.
    4. If an aggregation is required (e.g. couting records, averaging values), use functions like COUNT(), AVG(), MIN(), MAX(), SUM().
    #### **Examples**
    - **Question** : "How many student records are present?"
    - **SQL Query** : `SELECT COUNT(*) FROM STUDENT;`
    - **Question** : "List all students in the GenAI class."
    - **SQL Query** : `SELECT * FROM STUDENT WHERE CLASS="GenAI";`
    Now, generate an SQL Query for the given question.
"""
]

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

# Streamlit app
# set page configuration with a title and icon.
st.set_page_config(page_title="SQL Query Generator", page_icon="♾️")

# display the logo and header
if os.path.exists("1_nzVjqDcMKJPYudZvcc164g.jpg"):
    st.image("1_nzVjqDcMKJPYudZvcc164g.jpg", width=200)
st.header("♾️ Your AI powered SQL Assistant")

# Data can be a dictionary, list, or DataFrame
data = {
    'Name': ['Veda', 'Srija', 'Sirisha', 'Shiva', 'Anupama'],
    'Class': ['GenAI', 'DevOPs', 'OpenCV', 'NodeJS', 'PowerBI'],
    'Section': ['A', 'B', 'B+', 'A', 'A+'],
    'Marks': [90, 68, 70, 80, 100]
}

st.subheader("Student Table in Database")
st.table(data)


st.markdown("🤖 Ask any question and I'll generate the SQL query for you!")

# taking user input for natural language query
question=st.text_input("✍🏻 Enter your query in plain English:", key="input")

# submit button with an engaging design
submit=st.button("Generate SQL Query")

# if submit button is clicked
if submit:
    response=get_gemini_response(question, prompt)
    print("Generated SQL:", response)
    
    # Clean up the response (remove markdown formatting if present)
    clean_response = response.replace("```sql", "").replace("```", "").strip()
    
    try:
        # FIXED: Use consistent database name (STUDENT.db - uppercase)
        result=read_sql_query(clean_response, "STUDENT.db")
        st.subheader("The response is")
        for row in result:
            st.write(row)
    except Exception as e:
        st.error(f"Error executing query: {e}")
        st.code(clean_response)


# # app.py

# from dotenv import load_dotenv
# load_dotenv() # load all the environment variables
# import streamlit as st
# import os
# import sqlite3
# import google.generativeai as genai

# # configure your API
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# #function to load google model and provide sql query as a response
# def get_gemini_response(question, prompt):
#     model = genai.GenerativeModel("models/gemini-1.5-flash")
#     response=model.generate_content([prompt[0], question])
#     return response.text

# # function to retrieve query from the database
# def read_sql_query(sql, db):
#     conn=sqlite3.connect(db)
#     cur=conn.cursor()
#     cur.execute(sql)
#     rows=cur.fetchall()
#     conn.commit()
#     conn.close()
   
#     for row in rows:
#         print(row)
#     return rows

# # define your prompt
# prompt=[
#     """
#     You are an expert AI assisstant specializing in converting natural language questions to sql queries.
#     The SQL Database is name **STUDENT** and contains the following columns:
#     - **NAME** (VARCHAR)
#     - **CLASS** (VARCHAR)
#     - **SECTION** (VARCHAR)
#     - **MARKS** (INT)
#     Follow these guidelines when gwnerating SQL Queries:
#     1. Ensure the output contains only the SQL query, do not include explanations, formatting, markdowns.
#     2. Use proper SQL syntax while maintaining accuracy and efficiency.
#     3. If the query involves filtering, apply appropriate "WHERE" clauses.
#     4. If an aggregation is required (e.g. couting records, averaging values), use functions like COUNT(), AVG(), MIN(), MAX(), SUM().
#     #### **Examples**
#     - **Question** : "How many student records are present?"
#     - **SQL Query** : `SELECT COUNT(*) FROM STUDENT;`
#     - **Question** : "List all students in the GenAI class."
#     - **SQL Query** : `SELECT * FROM STUDENT WHERE CLASS="GenAI";`
#     Now, generate an SQL Query for the given question.
# """
# ]

# # Streamlit app
# # set page configuration with a title and icon.
# st.set_page_config(page_title="SQL Query Generator", page_icon="♾️")

# # display the logo and header
# if os.path.exists("1_nzVjqDcMKJPYudZvcc164g.jpg"):
#     st.image("1_nzVjqDcMKJPYudZvcc164g.jpg", width=200)
# st.header("♾️ Your AI powered SQL Assistant")


# # Data can be a dictionary, list, or DataFrame
# data = {
#     'Name': ['Veda', 'Srija', 'Sirisha', 'Shiva', 'Anupama'],
#     'Class': ['GenAI', 'DevOPs', 'OpenCV', 'NodeJS', 'PowerBI'],
#     'Section': ['A', 'B', 'B+', 'A', 'A+'],
#     'Marks': [90, 68, 70, 80, 100]
# }

# st.subheader("Student Table in Database")
# st.table(data)

# st.markdown("🤖 Ask any question and I'll generate the SQL query for you!")

# # taking user input for natural language query
# question=st.text_input("✍🏻 Enter your query in plain English:", key="input")

# # submit button with an engaging design
# submit=st.button("Generate SQL Query")

# # if submit button is clicked
# if submit:
#     response=get_gemini_response(question, prompt)
#     print("Generated SQL:", response)
    
#     # Clean up the response (remove markdown formatting if present)
#     clean_response = response.replace("```sql", "").replace("```", "").strip()
    
#     try:
#         # FIXED: Use consistent database name (STUDENT.db - uppercase)
#         result=read_sql_query(clean_response, "STUDENT.db")
#         st.subheader("The response is")
#         for row in result:
#             st.write(row)
#     except Exception as e:
#         st.error(f"Error executing query: {e}")
#         st.code(clean_response)

# from dotenv import load_dotenv
# load_dotenv() # load all the environment variables
# import streamlit as st
# import os
# import sqlite3
# import google.generativeai as genai

# # configure your API
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# #function to load google model and provide sql query as a response
# def get_gemini_response(question, prompt):
#     model = genai.GenerativeModel("models/gemini-1.5-flash")
#     response=model.generate_content([prompt[0], question])
#     return response.text

# # function to retrieve query from the database
# def read_sql_query(sql, db):
#     conn=sqlite3.connect(db)
#     cur=conn.cursor()
#     cur.execute(sql)
#     rows=cur.fetchall()
#     conn.commit()
#     conn.close()
    

#     for row in rows:
#         print(row)
#     return rows

# # define your prompt
# prompt=[
#     """
#     You are an expert AI assisstant specializing in converting natural language questions to sql queries.

#     The SQL Database is name **student** and contains the following columns:
#     - **name** (VARCHAR)
#     - **class** (VARCHAR)
#     - **section** (VARCHAR)
#     - **marks** (INT)

#     Follow these guidelines when gwnerating SQL Queries:
#     1. Ensure the output contains only the SQL query, do not include explanations, formatting, markdowns.
#     2. Use proper SQL syntax while maintaining accuracy and efficiency.
#     3. If the query involves filtering, apply appropriate "WHERE" clauses.
#     4. If an aggregation is required (e.g. couting records, averaging values), use functions like COUNT(), AVG(), MIN(), MAX(), SUM().

#     #### **Examples**
#     - **Question** : "How many student records are present?"
#     - **SQL Query** : `SELECT COUNT(*) FROM student;`

#     - **Question** : "List all students in the GenAI class."
#     - **SQL Query** : `SELECT * FROM student WHERE class="GenAI";`

#     Now, generate an SQL Query for the given question.
# """
# ]

# # Streamlit app
# # set page configuration with a title and icon.

# st.set_page_config(page_title="SQL Query Generator", page_icon="♾️")

# # display the logo and header
# st.image("1_nzVjqDcMKJPYudZvcc164g.jpg", width=200)
# st.markdown("♾️ Your AI powered SQL Assisstant")
# st.markdown("🤖 Ask any question and I'll generate the SQL query for you!")

# # taking user input for natural language query
# question=st.text_input("✍🏻 Enter your query in plain English:", key="input")

# # submit button with an engaging design
# submit=st.button("Generate SQL Query")

# # if submit button is clicked
# if submit:
#     response=get_gemini_response(question, prompt)
#     print(response)
#     response=read_sql_query(response, "student.db")
#     st.subheader("The response is")

#     for row in response:
#         print(row)
#         st.header(row)
