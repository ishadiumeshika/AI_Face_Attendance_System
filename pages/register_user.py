import streamlit as st
from register import register_person

st.title("👤 Register User")

st.write("Enter a user's name, then click the button below to register their face.")

name = st.text_input("Name")

if st.button("Start Registration"):
    if not name.strip():
        st.error("Please enter a name.")
    else:
        st.info("The webcam will open. Look at the camera and press **S** to save your face, or **Q** to cancel.")
        register_person(name.strip())
        st.success(f"{name} registered successfully!")