import streamlit as st
from datetime import datetime
from openai import OpenAI
from src.helper import connect_to_deta, fetch_data

# Initialize OpenAI client with API key from Streamlit's secrets management and connect to databases
client = OpenAI(api_key=st.secrets['open_api_key'])
db = connect_to_deta("snake-demo")
db2 = connect_to_deta("recipe-database")


def recipe_generator_page():
    user_data = fetch_data(db)

    st.title("Recipe Generator")

    # Collect user inputs for recipe generation in variables, the sliders etc. itself are self-explanatory
    ingredients = st.multiselect(
        'Which ingredients do you have at hand?',
        ['Tomatoes 🍅', 'Lettuce 🥬', 'Cheese 🧀', 'Chicken 🍗', 'Beef 🥩',
         'Fish 🐟', 'Eggs 🥚', 'Onions 🧅', 'Garlic 🧄', 'Mushrooms 🍄',
         'Potatoes 🥔', 'Carrots 🥕', 'Rice 🍚', 'Pasta 🍝', 'Bread 🍞']
    )
    additional_ingredients = st.text_input("Any other ingredients you have at hand?")
    cuisine = st.selectbox(
        'Which cuisine do you prefer the most?',
        ['Italian 🤌🇮🇹', 'Chinese 🍚🇨🇳', 'Japanese 🍣🇯🇵', 'Mexican 🌮🇲🇽',
         'Indian 🍛🇮🇳', 'Thai 🍜🇹🇭', 'French 🥐🇫🇷', 'Greek 🥙🇬🇷',
         'Spanish 🥘🇪🇸', 'Korean 🥢🇰🇷']
    )
    cooking_appliances = st.multiselect(
        'Which cooking appliances do you have in your kitchen and would use for cooking?',
        ['Oven', 'Air Fryer', 'Microwave', 'Blender', 'Toaster',
         'Slow Cooker', 'Pressure Cooker', 'Food Processor', 'Grill', 'Stove']
    )
    number_of_people = st.number_input("How many people are you cooking for?", min_value=1, max_value=None, value=1,
                                       step=1)
    cooking_time = st.select_slider(
        'How much time would you spent on Cooking today?',
        options=['5 minutes', '15 minutes', '30 minutes', '45 minutes', '60 minutes', '90 minutes',
                 'More than 90 minutes']
    )
    cooking_level = st.select_slider(
        'How would you rate your own cooking level?',
        options=['Absolute Beginner👶', 'Basic Cooking 🍳', 'Advanced Home Cook 🔪', 'Professional Chef 👨‍🍳']
    )

    dietary_options = ['Vegan', 'Vegetarian', 'Pescatarian', 'Low-Fat', 'Low-Carbs', 'High Protein']
    # generates checkboxes based on the list above, then puts it into a readable format
    selected_dietary_preferences = [option for option in dietary_options if st.checkbox(option)]
    dietary_preferences_str = ', '.join(selected_dietary_preferences)

    if st.button("Generate Recipe"):
        recipe_prompt = f"""
        Please generate one detailed recipe with step-by-step instructions that meets all of the following requirements:
        Ingredients: Include as many as possible of: {', '.join(ingredients + [additional_ingredients])}
        Dietary Preferences: {dietary_preferences_str}
        Cuisine Preference: {cuisine}
        Timeframe: The recipe should take around {cooking_time} minutes from start to finish.
        Serving Size: The recipe should serve {number_of_people} people.
        Cooking Level: The recipe should be appropriate for someone at a {cooking_level} cooking level.
        Cooking Appliances: Only use the following appliances: {', '.join(cooking_appliances)}
        Format: Start with a detailed ingredients list then provide step-by-step instructions for preparing the recipe.
        """

        # hand the recipe prompt to ChatGPT, idea by: https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps
        response = client.chat.completions.create(model="gpt-3.5-turbo",
                                                  messages=[{"role": "system", "content": recipe_prompt}])
        recipe_output = response.choices[0].message.content


        # there is another generation prompt just for the title, as you can't seperate the title from the recipe response reliably
        name_prompt = f"Generate a short name for the following recipe with the following format: 3 emojis (country flag, two food related emojis), the Recipe Title, the same emojis in opposite order. Consider that it is a {cuisine} recipe for your title. The recipe: {recipe_output}"
        name_response = client.chat.completions.create(model="gpt-3.5-turbo",
                                                       messages=[{"role": "system", "content": name_prompt}])
        name_output = name_response.choices[0].message.content

        st.info(f"**{name_output}**   \n   \n{recipe_output}")

        # collects the most basic information about the recipe for download purposes
        today = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        topic = f"Based on your ingredients: {', '.join(ingredients)} I created this recipe for you: \n{recipe_output}"
        filename = f"Recipe_from_{today}.txt"
        st.download_button(label="Download Recipe", data=topic, file_name=filename)

        # summarizes the user input so the user can trace back how the recipe was made in his profile
        input_summary = (
            f"**Selected Ingredients:** {', '.join(ingredients)}   \n"
            f"**Additional Ingredients:** {additional_ingredients}   \n"
            f"**Preferred Cuisine:** {cuisine}   \n"
            f"**Available Cooking Appliances:** {', '.join(cooking_appliances)}   \n"
            f"**Number of People:** {number_of_people}   \n"
            f"**Cooking Time:** {cooking_time}   \n"
            f"**Cooking Level:** {cooking_level}   \n"
            f"**Dietary Preferences:** {dietary_preferences_str}   \n"
        )

        new_recipe = {
            "date": today,
            "name": name_output,
            "ingredients": ingredients,
            "instructions": recipe_output,
            "prompt": input_summary
        }
        # additional safety measure so recipes get only uploaded to the profile if the user is logged in
        current_user = st.session_state['current_username']
        if current_user:
            # the update function only works with the key assigned by the detabase, so we find out this key by the username
            # reference for .to_string(index=False).strip(): the Digital Media Lab Tutor Moritz
            key = user_data.loc[user_data['user_name'] == current_user]["key"].to_string(index=False).strip()
            db.update({"recipes": db.util.append(new_recipe)}, key)
            st.success("The Recipe got automatically saved in your profile, so you can check it out later.")