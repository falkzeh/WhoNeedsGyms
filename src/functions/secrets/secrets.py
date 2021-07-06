import os
import streamlit as st

## YouTube API ##
# https://console.developers.google.com/
yt_api_key = os.environ["yt_api_key"]

## PostgresDB ##
db_name = os.environ["db_name"]
db_user = os.environ["db_user"]
db_password = os.environ["db_password"]
db_host = os.environ["db_host"]
db_port = os.environ["db_port"]

## Added for Streamlit Cloud
yt_api_key = st.secrets["yt_api_key"]
db_name = st.secrets["db_name"]
db_user = st.secrets["db_user"]
db_password = st.secrets["db_password"]
db_host = st.secrets["db_host"]
db_port = st.secrets["db_port"]
