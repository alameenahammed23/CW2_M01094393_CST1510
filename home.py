import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="My App",
    page_icon="🫳",
    layout="wide"
)

with st.sidebar:
    st.header("Navigation")
    options = st.selectbox("Choose", ['a','b','c'])


