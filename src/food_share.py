import streamlit as st
from PIL import Image
from deta import Deta
from src.user_profile import fetch_profile  # Assuming functionality can be reused
from src.helper import connect_to_deta, fetch_data  # Assuming these can be reused
from io import BytesIO

# Initialize Deta with the secret key
deta = Deta(st.secrets["data_key"])

# Database and drive setup for food sharing
food_database_name = "leftover-food"
db = connect_to_deta(food_database_name)
food_drive_name = 'food-images'
drive = deta.Drive(food_drive_name)


def submit_food_share():
    if 'current_username' in st.session_state:
        current_username = st.session_state['current_username']

    st.title("Leftover Food Sharing Page")

    food_name = st.text_input("Food Name")
    food_gram = st.number_input("Gram (in grams)", step=50)
    expiry_date = st.date_input("Expiry Date")
    uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    contact_email = st.text_input("Contact Email")
    location = st.text_input("Location")

    # file is set in a format that can be submitted to drive, idea by: https://stackoverflow.com/a/74430715
    bytes_data = uploaded_image.getvalue() if uploaded_image is not None else None

    if st.button("Share Food"):
        if bytes_data is not None:
            # Save the image to Deta Drive with a unique name
            image_name = f"{current_username}_{expiry_date}_{food_name}"
            drive.put(image_name, data=bytes_data)
        else:
            image_name = None  # Handle cases where no image is uploaded

        db.put({
            "user_name": current_username,
            "food_name": food_name,
            "gram": food_gram,
            "expiry_date": str(expiry_date),
            "contact_email": contact_email,
            "image_name": image_name,
            "location": location
        })
        st.success('Your leftover food share has been successfully posted.')


def show_food_shares():
    leftover_food_database = fetch_data(db)
    st.title("Shared Leftover Food")

    num_columns = 3
    num_rows = len(leftover_food_database) // num_columns + (len(leftover_food_database) % num_columns > 0)

    for row in range(num_rows):
        columns = st.columns(num_columns)

        for col in range(num_columns):
            food_index = row * num_columns + col
            if food_index < len(leftover_food_database):
                with columns[col]:
                    food_share = leftover_food_database.iloc[food_index]
                    food_name = food_share['food_name']
                    food_gram = food_share['gram']
                    expiry_date = food_share['expiry_date']
                    contact_email = food_share['contact_email']
                    location = food_share['location']
                    image_name = food_share['image_name']

                    if image_name:
                        food_image = drive.get(image_name)
                        if food_image:
                            # Converts the image stored in Deta Drive back to a viewable format
                            # idea by: https://discuss.streamlit.io/t/get-an-image-from-mysql-database-and-display-via-st-image/35963/2
                            bytes_data = BytesIO(food_image.read())
                            image = Image.open(bytes_data)
                            st.image(image)
                        else:
                            st.image("images/error.jpg")

                    st.markdown(f"**{food_name} - {food_gram}g**")
                    st.markdown(f"Expiry Date: {expiry_date}")
                    st.markdown(f"Location: {location}")
                    st.markdown(f"Contact Email: {contact_email}")