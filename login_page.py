import streamlit as st
from src.main_page import  main_page
from src.helper import connect_to_deta, fetch_data

# set the page config info
st.set_page_config(
    page_title="Cookgether",
    page_icon="🥘",
    layout="wide"
)

# create a placeholder variable, so I can delete the form widget after using it
placeholder = st.empty()
# create a flag which will once is True, will let the user go the game
credentials_check = False

# create some session variables to keep track of if this is the first time the user is clicking on a button
if 'login_count' not in st.session_state:
    st.session_state.login_count = 0
if 'register_count' not in st.session_state:
    st.session_state.register_count = 0
if 'cookgether_count' not in st.session_state:
    st.session_state.cookgether_count = 0


# this is the definition that will add one to the counter every time the user clicks on it
def increment_login_counter():
    st.session_state.login_count += 1

def increment_register_counter():
    st.session_state.register_count += 1


# create a deta db to store and check my data
base_name = "snake-demo"

base_name2 = "recipe-database"
db2 = connect_to_deta(base_name2)

db = connect_to_deta(base_name)

# if you need to create the structure of the base - you can delete this row of data later
# db.insert({"user_name": "", "password": ""})


# create the log in form - this only gets created in the snake game has not been activated
if st.session_state.cookgether_count < 1:
    with placeholder.form("Login"):
        st.markdown(f'<p style="font-size: 20px; color:grey">Hello! Please enter your log in info.'
                    f'<br>If this is your first time on my app then please click on the Register Button.</p>',
                    unsafe_allow_html=True)
        user_name = st.text_input("Username", placeholder="Please enter your user name").lower()
        password = st.text_input("Password", placeholder="Please enter your password", type="password")
        login_button = st.form_submit_button("Login")
        register_button = st.form_submit_button("Register")

        # fetch the user data to carry out validations
        user_data = fetch_data(db)  # fetching all the data I have stored on my user
        user_names = list(user_data.user_name)  # identifying the list of users

        if login_button:
            increment_login_counter()  # keep track of the number of times the user comes on this button
            # if it's the users first time dont print anything
            if st.session_state.login_count > 1:
                # if user name exists in user name - change credentials check flag to True
                if user_name in user_names:
                    # this selects the password of the user that is entering information
                    registered_password = list(user_data[user_data.user_name == user_name].password)[0]

                    if password == registered_password:
                        credentials_check = True
                        st.session_state['current_username'] = user_name
                    else:
                        st.error("The username/password is not correct")
                else:
                    st.error("Please provide correct user name or click on register as new user")

        if register_button:
            increment_register_counter()  # keep track of the number of times the user comes on this button
            # if it's the users first time dont print anything
            if st.session_state.register_count > 1:
                if len(user_name) == 0 and len(password) == 0:
                    st.warning('Please enter username and password', icon="⚠️")
                elif len(user_name) == 0:
                    st.warning('Please enter username', icon="⚠️")
                elif len(password) == 0:
                    st.warning('Please enter password', icon="⚠️")
                elif user_name in user_names:
                    st.warning('This user name already exists. Please create another user name or click on Login',
                               icon="⚠️")
                else:
                    # write the data to the database and update the credentials check flag
                    db.put({
                        "user_name": user_name,
                        "password": password,
                        "email": "Not yet selected",  # This can be prompted for or set later
                        "aboutme": "Not yet selected",
                        "cookinglevel": "Not yet selected",
                        "favouritecuisine": "Not yet selected",
                        "dietarypreferences": "Not yet selected",
                        "location": "Berlin",  # This can be dynamic or set later
                        "recipes": []
                    })
                    credentials_check = True
                    st.session_state['current_username'] = user_name


    # once this flag has been updated, then we can go to the game
    if credentials_check:
        # delete all the form widgets we created
        placeholder.empty()
        # update the snake count to 1
        st.session_state.cookgether_count = 1

# if the snake count is greater than 0, this means the user has successfully passed the login checks
# place the widgets
# call the snake game definition
if st.session_state.cookgether_count > 0:
    main_page()