import streamlit as st

from app.database.user import login_user



def login_page():


    st.title("🔐 Login")


    email = st.text_input(
        "Email"
    )


    password = st.text_input(
        "Password",
        type="password"
    )



    if st.button("Login"):


        user = login_user(
            email,
            password
        )


        if user:


            st.session_state.logged_in = True

            st.session_state.user_id = user["id"]

            st.session_state.name = user["name"]

            st.session_state.role = user["role"]


            st.balloons()

            st.success(
            f"Welcome {user['name']}"
        )


            st.rerun()


        else:


            st.error(
                "Invalid email or password"
            )