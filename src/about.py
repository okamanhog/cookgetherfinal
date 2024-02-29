import streamlit as st


# Reference: We used ChatGPT to make our about page better readable.
def about_page():
    st.title("About Cookgether")
    st.markdown("""
    **Cookgether** is a cutting-edge platform designed for cooking enthusiasts. It fosters a vibrant community where members can generate AI-powered personalized recipes, share their culinary creations and engage with others over shared food interests. 

    ### Features Include:
    - **AI Recipe Generator**: Tailor-made recipes based on your input such as available ingredients, preferred cuisine, cooking appliances, and more.
    - **Community Sharing**: A space to share your recipes with the community, rate, and review others' contributions.
    - **Food Share**: An initiative to share leftover food, promoting sustainability and community support.
    - **User Profile**: Personalized profiles to showcase your cooking adventures, favorite recipes, and culinary preferences.

    ### How to Get Started:
    - **Online Access**: Visit our public link at [https://cookgether-project.streamlit.app/](https://cookgether-project.streamlit.app/) to start your Cookgether journey.
    - **Local Setup**: Clone or download the app, set up your environment with Streamlit and other dependencies, and run the app locally for a more personalized experience.

    Built by [Sum](https://github.com/SumSumarie) and [Lennart](https://github.com/okamanhog).""")
