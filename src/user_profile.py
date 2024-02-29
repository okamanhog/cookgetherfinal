import streamlit as st
from src.helper import connect_to_deta, fetch_data

# create database in deta
base_name = "snake-demo"
base_name2 = "recipe-database"

db = connect_to_deta(base_name)
db2 = connect_to_deta(base_name2)


# function to fetch specific profile from detabase and turn it into a dictionary, so it is easier to work with
def fetch_profile(user_name):
    user_data = fetch_data(db)
    user_profile = {
        "username": user_name,
        # values[0] is used in order to get the value standalone without any meta information
        "aboutme": user_data.loc[user_data['user_name'] == user_name]["aboutme"].values[0],
        "cookinglevel": user_data.loc[user_data['user_name'] == user_name]["cookinglevel"].values[0],
        "favouritecuisine": user_data.loc[user_data['user_name'] == user_name]["favouritecuisine"].values[0],
        "dietarypreferences": user_data.loc[user_data['user_name'] == user_name]["dietarypreferences"].values[0],
        "location": user_data.loc[user_data['user_name'] == user_name]["location"].values[0],
        "recipes": user_data.loc[user_data['user_name'] == user_name]["recipes"].values[0]
    }
    return user_profile


def update_aboutme(username, new_profile_info):
    user_data = fetch_data(db)
    # the update function only works with the key assigned by the detabase, so we find out this key by the username
    # reference for .to_string(index=False).strip(): the Digital Media Lab Tutor Moritz
    key = user_data.loc[user_data['user_name'] == username]["key"].to_string(index=False).strip()
    db.update(new_profile_info, key)

def show_user_profile(username):
    user_profile_data = fetch_profile(username)

    st.subheader('About Me', divider='rainbow')

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(user_profile_data["aboutme"])

    with col2:
        st.markdown(f"**Cooking Level: :green[{user_profile_data['cookinglevel']}]**")
        st.markdown(f"**Favourite Cuisine: :green[{user_profile_data['favouritecuisine']}]**")
        st.markdown(f"**Diet: :green[{user_profile_data['dietarypreferences']}]**")

    # only allows to edit the users own profile
    if username == st.session_state.get('current_username'):
        with st.expander("Edit Profile"):
            with st.form('edit_profile_form'):
                new_aboutme = st.text_area("About Me:", value=user_profile_data['aboutme'])
                cuisine = st.selectbox(
                    'Which cuisine do you prefer the most?',
                    ('Italian 🤌🇮🇹',
                     'Chinese 🍚🇨🇳',
                     'Japanese 🍣🇯🇵',
                     'Mexican 🌮🇲🇽',
                     'Indian 🍛🇮🇳',
                     'Thai 🍜🇹🇭',
                     'French 🥐🇫🇷',
                     'Greek 🥙🇬🇷',
                     'Spanish 🥘🇪🇸',
                     'Korean 🥢🇰🇷')
                )
                cookinglevel = st.select_slider(
                    'How would you rate your own cooking level?',
                    options=['Absolute Beginner👶', 'Basic Cooking 🍳', 'Advanced Home Cook 🔪', 'Professional Chief 👨‍🍳'])
                dietary_options = ['Vegan', 'Vegetarian', 'Pescatarian', 'Low-Fat', 'Low-Carbs', 'High Protein']

                # create an empty list to store the user's selections
                selected_dietary_preferences = []

                # iterate over the options and create a checkbox for each
                for option in dietary_options:
                    if st.checkbox(option):
                        selected_dietary_preferences.append(option)

                # join the selected options into a single string
                dietary_preferences_str = ', '.join(selected_dietary_preferences)
                submit_button = st.form_submit_button(label='Submit')

                # new profile information is collected into a dictionary, for the update function
                new_profile_info = {
                    "aboutme": new_aboutme,
                    "cookinglevel": cookinglevel,
                    "favouritecuisine": cuisine,
                    "dietarypreferences": dietary_preferences_str
                }

                if submit_button:
                    update_aboutme(username, new_profile_info)
                    st.success('About Me updated successfully!')
                    st.rerun()

    # generated recipes
    st.subheader('History of recipes:', divider='rainbow')
    for recipe in user_profile_data["recipes"]:
        with st.expander("Show the input used for this recipe:"):
            st.write(recipe['prompt'])
        st.markdown(f"**{recipe['name']}**   \n **Cooked on the:** {recipe['date']}  \n **Instructions:** {recipe['instructions']}")
        st.divider()


def user_profile_page():
    if 'current_username' in st.session_state:
        current_user = st.session_state['current_username']
        st.title(f"Welcome Back, {current_user}")
        show_user_profile(current_user)
    else:
        st.write("No current username in session state.")