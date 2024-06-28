from dotenv import load_dotenv
import os
import streamlit as st
import sqlite3
import google.generativeai as genai


# load_dotenv()  # to load the variables added in the .env file for local


# genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
os.environ["GOOGLE_API_KEY"] = st.secrets.db_credentials.GOOGLE_API_KEY

genai.configure(api_key=st.secrets.db_credentials.GOOGLE_API_KEY)


def response_gemini(question, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content([prompt[0], question])
    return response.text


def sql_retrieve(sql, db):
    db = sqlite3.connect(db)
    cursor = db.cursor()
    cursor.execute(sql)
    output = cursor.fetchall()

    return output


prompt = [
    """
    You are an expert in converting English questions to SQL queries!
    The SQL database has the name `user` and has the following columns - `firstname`, `familyname`, `gender`, `city`, `country`, `email`.

    For example,
    Example 1 - How many entries of records are present?, 
    the SQL command will be something like this: SELECT COUNT(*) FROM user;

    Example 2 - List all users from the USA?, 
    the SQL command will be something like this: SELECT * FROM user WHERE country='USA';
    
    Please ensure the SQL code does not have ``` at the beginning or end, and the word "sql" is not in the output.
    """
]


# Streamlit app
st.title("SQL Query Generator")

# Input form
question = st.text_input("Ask your question:")

if st.button("Submit"):
    if question:
        # Generate SQL query
        sql_query = response_gemini(question, prompt).strip()
        st.write("Generated SQL Query:")
        st.code(sql_query, language='sql')

        # Retrieve and display data
        try:
            results = sql_retrieve(sql_query, "database.db")
            st.write("Query Results:")
            if results:
                for row in results:
                    st.write(row)
            else:
                st.write("No results found.")
        except Exception as e:
            st.write(f"Error: {e}")

if st.checkbox("Show prompt"):
    st.write(prompt[0])
