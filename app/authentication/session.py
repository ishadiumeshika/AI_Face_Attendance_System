import streamlit as st


def login_user(user):

    st.session_state.logged_in = True
    st.session_state.user_id = user["id"]
    st.session_state.name = user["name"]
    st.session_state.role = user["role"]



def logout_user():

    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.name = None
    st.session_state.role = None



def is_logged_in():

    return st.session_state.get(
        "logged_in",
        False
    )