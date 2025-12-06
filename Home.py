import streamlit as st
from hashing import hash_password, validate_password
from app_model.db import get_connection
from app_model.users import add_user, get_user
conn = get_connection()


st.set_page_config(
    page_title="Home Page",
    page_icon="🏠",
    layout="wide"
)

st.title("Welcome to the Main Page")


if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False


tab_login, tab_register = st.tabs(["Login", "Register"])


with tab_login:
    login_username = st.text_input(
        "Username",
        key="login_username"
    )

    login_password = st.text_input(
        "Password",
        type="password",
        key="login_password"
    )

    if st.button("Log In", key="login_button"):
        id, user_name, user_hash = get_user(conn, login_username)
        if login_username == user_name and validate_password(login_password, user_hash):
            st.session_state["logged_in"] = True
            st.success("Logged in successfully")
            st.switch_page("pages/1_Dashboard.py")
        st.success("Logged in successfully")

with tab_register:
    register_username = st.text_input(
        "New Username",
        key="register_username"
    )

    register_password = st.text_input(
        "New Password",
        type="password",
        key="register_password"
    )

    if st.button("Register", key="register_button"):
        if not register_username or not register_password:
            st.error("Username and password are required")
        else:
            conn = get_connection()
            hashed_password = hash_password(register_password)
            add_user(conn, register_username, hashed_password)
            st.success("Registration successful! You can now log in.")
