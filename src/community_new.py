import streamlit as st
from PIL import Image
from deta import Deta
from src.user_profile import fetch_profile, show_user_profile
from src.helper import connect_to_deta, fetch_data
from streamlit_star_rating import st_star_rating
from io import BytesIO

# Initialize Deta with the secret key
deta = Deta(st.secrets["data_key"])

# Database and drive setup
recipe_database_name = "recipe-database"
db2 = connect_to_deta(recipe_database_name)
drive_name = 'recipe-images'
drive = deta.Drive(drive_name)


def submit_recipe():
    # fetches the profile from the current user to gather all the recipes shared in his profile, so he can choose it
    if 'current_username' in st.session_state:
        current_username = st.session_state['current_username']
        current_user_profile = fetch_profile(current_username)
        recipe_list = [recipe['name'] for recipe in current_user_profile['recipes']]

        if not recipe_list:
            st.info("You also want to share recipes on this page? Tap the **❯** Button in the top left corner, "
                    "then click on **AI Recipe Generator**. Once you generated your own recipes you can come back "
                    "here and share them along with your thoughts with our community!")
            return

        # compares user selection to the recipes in his profile, then stores that recipe in "recipe_to_show"
        selected_recipe = st.selectbox('Which recipe do you want to share?', recipe_list)
        recipe_to_show = next(recipe for recipe in current_user_profile['recipes'] if recipe['name'] == selected_recipe)

        # streamlit function for rating using stars: https://discuss.streamlit.io/t/new-component-star-ratings/36829
        stars = st_star_rating("How would you rate this recipe?", 5, 5, 20)  # number of stars, default value, text size

        uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        user_text = st.text_area("What was your interesting Cookgether experience?")

        # file is set in a format that can be submitted to drive, idea by: https://stackoverflow.com/a/74430715
        bytes_data = uploaded_image.getvalue() if uploaded_image is not None else None

        if st.button("Post Recipe"):
            # the following two lines check whether the recipe already exists, idea by: https://chat.openai.com/share/1d1110df-1536-4853-8035-106b469f439c
            existing_recipes = db2.fetch({"user_name": current_username, "recipe_name": selected_recipe}).items
            if any(recipe['recipe']['date'] == recipe_to_show['date'] for recipe in existing_recipes):
                st.error("This recipe has already been uploaded.")
            else:
                # uploads an image if the user has chosen one (he doesn't have to)
                if bytes_data is not None:
                    # the left field is the file name, it consists of date and username so its identifiable later
                    drive.put(f"{recipe_to_show['date']}{current_username}", data=bytes_data)
                db2.put({
                    "user_name": current_username,
                    "recipe_name": selected_recipe,
                    "recipe": recipe_to_show,
                    "review": user_text,
                    "rating": stars
                })
                st.success('Your recipe was successfully uploaded. Please refresh the page in a few seconds, '
                           'to see your recipe on the community page!', icon="✅")


def show_community_recipes():
    recipe_database = fetch_data(db2)
    st.title("Recipe Community Page")

    num_columns = 3
    # Calculate the number of rows needed to display the recipes in a grid
    num_rows = len(recipe_database) // num_columns + (len(recipe_database) % num_columns > 0)

    for row in range(num_rows):
        recipe_columns = st.columns(num_columns)
        for col in range(num_columns):
            recipe_index = row * num_columns + col
            if recipe_index < len(recipe_database):
                with recipe_columns[col]:
                    # gather recipe data from database and split it into variables that are displayed to the user
                    db_recipe = recipe_database.iloc[recipe_index]
                    db_user_name = db_recipe['user_name']
                    db_review = db_recipe['review']
                    db_rating = db_recipe['rating']
                    db_recipe_name = db_recipe['recipe_name']
                    recipe_instructions = db_recipe['recipe']['instructions']
                    drive_image_name = f"{db_recipe['recipe']['date']}{db_user_name}"
                    recipe_image = drive.get(drive_image_name)
                    # the previously uploaded image (bytes_data) gets converted back into a viewable form using BytesIO
                    if recipe_image:
                        # idea by: https://discuss.streamlit.io/t/get-an-image-from-mysql-database-and-display-via-st-image/35963/2
                        bytes_data = BytesIO(recipe_image.read())
                        image = Image.open(bytes_data)
                        st.image(image)
                    else:
                        st.image("images/error.jpg")
                    st.markdown(f"**{db_recipe_name}**")
                    with st.expander("Show Instructions"):
                        st.write(recipe_instructions)
                    with st.expander("Show Review"):
                        if db_rating <= 2:
                            st.markdown(f":red[**{db_rating}/5 Stars**]")
                        elif db_rating == 3:
                            st.markdown(f":orange[**{db_rating}/5 Stars**]")
                        elif db_rating >= 4:
                            st.markdown(f":green[**{db_rating}/5 Stars**]")
                        else:
                            st.markdown("No Rating Found!")
                        st.write(db_review)
                    # the key is being set because streamlit does not allow two buttons with the same label
                    if st.button(f"View {db_user_name}'s Profile", key=f"{db_recipe['recipe']['date']}{db_user_name}",
                                 use_container_width=True):
                        show_user_profile(db_user_name)