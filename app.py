import streamlit as st
from pathlib import Path
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain.sql_database import SQLDatabase
from langchain.agents import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq
from langchain.agents import create_sql_agent
import os
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Langchain Chat with sql db",page_icon="🦜")
st.title("Langchain Chat with sql db")
LOCALDB="USE_LOCALDB"
MYSQL="USE_MYSQL"

radio_opt=["USE sqlite 3 databases-sqlite3.db","connect to your SQL database"]
select_opt=st.sidebar.radio(label="choose the db which you want to connect",options=radio_opt)
if radio_opt.index(select_opt)==1:
    db_uri=MYSQL
    mysql_host=st.sidebar.text_input("Provide mysql  host ")
    mysql_user=st.sidebar.text_input("Mysql User")
    mysql_password=st.sidebar.text_input("Mysql password",type="password")
    mysql_db=st.sidebar.text_input("Mysql database")

else:
    db_uri=LOCALDB
api_key=st.sidebar.text_input("Enter your groq api key",type="password")
llm=ChatGroq(groq_api_key=api_key,model="Llama3-8b-8192")
if not db_uri:
    st.info("please enter the database info and uri")

if not api_key:
    st.info("Please enter your groq api key")
@st.cache_resource(ttl="2h")
def configure_db(db_uri,mysql_host=None,mysql_user=None,mysql_password=None,mysql_db=None):
    if db_uri==LOCALDB:
        dbfilepath=(Path(__file__).parent/"employee.db").absolute()
        print(dbfilepath)
        creator=lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro",uri=True)
        return SQLDatabase(create_engine("sqlite:///",creator=creator))
    elif db_uri==MYSQL:
        if not (mysql_host and mysql_user and mysql_password and mysql_db):
            st.error("Please provide all mysql connection details")
            st.stop()
        return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))
if db_uri==MYSQL:
    db=configure_db(db_uri,mysql_host,mysql_user,mysql_password,mysql_db)
else:
    db=configure_db(db_uri)

toolkit=SQLDatabaseToolkit(db=db,llm=llm)
agent=create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

if "message" not in   st.session_state or st.sidebar.button("clear message history"):
    st.session_state['messages']=[{"role":"assistant","content":"how can i help you"}]
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg['content'])

user_query=st.chat_input(placeholder="Ask anything from database")
if user_query:
    st.session_state.messages.append({"role":"user","content":user_query})
    st.chat_message("user").write(user_query)
    with st.chat_message("assistant"):
        st_cb=StreamlitCallbackHandler(st.container())
        response=agent.run(user_query,callbacks=[st_cb])
        st.session_state.messages.append({"role":"assistant","content":response})
        st.write(response)

