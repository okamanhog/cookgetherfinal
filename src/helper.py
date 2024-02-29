from deta import Deta
import streamlit as st
import pandas as pd


def connect_to_deta(base_name):
    """This connect to deta and creates a data base to store our data"""

    # fetches the secret key
    deta = Deta(st.secrets["data_key"])

    # create a database
    db = deta.Base(base_name)
    return db


def fetch_data(db):
    return pd.DataFrame(db.fetch().items)