import os
import json 
import streamlit as st

# Function to load users from JSON
def load_users():
    if not os.path.exists('users.json'):
        with open('users.json', 'w') as f:
            json.dump({}, f)
    with open('users.json', 'r') as f:
        return json.load(f)

# Function to save users to JSON
def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f)


# Enhanced login function
def login(username, password, users):
    return username in users and users[username] == password

# Signup function
def signup(username, password, users):
    if username not in users:
        users[username] = password
        save_users(users)
        return True
    return False

def authenticate():
    users = load_users()

    # Session state to track login status
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    # Centered container for login and signup
    with st.container():
        st.title("Liver Tumor Classification and Segmentation")
        col1, col2 = st.tabs(['Login', 'SignUp'])

        # Login UI
        with col1:
            # st.write("### Login")
            login_username = st.text_input("Username", key="login_username")
            login_password = st.text_input("Password", type="password", key="login_password")
            if st.button("Login"):
                if login(login_username, login_password, users):
                    st.session_state['logged_in'] = True

                    os.system('streamlit run main.py')

                else:
                    st.error("Incorrect username or password")

        # Signup UI
        with col2:
            # st.write("### Signup")
            new_username = st.text_input("Username", key="signup_username")
            new_password = st.text_input("Password", type="password", key="signup_password")
            if st.button("Signup"):
                if signup(new_username, new_password, users):
                    st.success("Signup successful, you can now login")
                else:
                    st.error("Username already exists")



authenticate()