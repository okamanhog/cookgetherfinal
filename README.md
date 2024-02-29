# Cookgether App

## About Cookgether

Cookgether is a cutting-edge app designed for cooking enthusiasts to build a vibrant community based on AI-generated personalized recipes. It offers an innovative platform for users to try new food based on your own ingredients and preferences, share these recipes, engage with the community and make the most of leftover food. 

## Features

### 🗒️ AI Recipe Generator

- **Personalized Recipes**: Generate recipes based on your available ingredients, desired cuisine, cooking appliances, number of servings, available time, and more.
- **Downloadable Recipes**: Easily download your custom recipes for offline use.

### 🥘 Community Sharing

- **Recipe Sharing**: Share your culinary creations with the community, including ratings and reviews.
- **Engage with Peers**: Connect with fellow food enthusiasts by rating, reviewing, and discussing shared recipes.

### 🍎 Food Share

- **Sustainable Sharing**: Share leftover food with others in the community to reduce waste.
- **Local Connections**: Share and receive leftover food within your local area, detailed with food name, quantity, expiry date, and pickup instructions.

### 😀 User Profile

- **Personalized Profiles**: Showcase your cooking level, favorite cuisines, and dietary preferences.
- **Recipe Management**: Keep track of your generated and shared recipes easily.

### 📌 About

Discover the vision, mission, and community behind Cookgether.

## How to Use Cookgether

### Online Access

Visit our public link at [https://cookgether-project.streamlit.app/](https://cookgether-project.streamlit.app/) to explore and use Cookgether without any installation.

### Running Cookgether Locally

1. **Download the App**:
   - Clone or download the Cookgether repository to your local machine.

2. **Set Up Your Environment**:
   - Ensure you have Python installed on your computer.
   - Install Streamlit and the other required libraries using pip:
     ```bash
     pip install -r requirements.txt
     ```

3. **Run the App**:
   - Navigate to the app's directory in your terminal.
   - Run the app using Streamlit:
     ```bash
     streamlit run login_page.py
     ```
   - Follow the instructions in your terminal to view the app in your browser.

## Getting Started

1. **Register/Login**: Sign up for a new account or log in by simply typing your username and password. Remember that we use double click for our buttons, so you might have to click twice on each button for it to work.
2. **Main Page**: You will land on our Community Page first, where you can explore the recipes other people have generated and shared before. 
3. **Explore**: Use the sidebar to navigate through the app's features. 
4. **Create Recipes**: Use our fancy AI Recipe Generator for tailored recipe suggestions based on specific details you provide using sliders and other inputs.
5. **Profile Page**: Every generated recipe of yours gets automatically saved in your profile, where you can find it later on. On this page you can also write a bit about yourself, your favourite food and cooking level to connect with other community members. 
6. **Share Recipes**: After you created your first recipes, you can go back to our community page and start sharing those recipes. Along that you can add an image of how it looked in the end, rate it and write a few sentences to let other users know what to expect when trying this AI recipe.
7. **Participate in Food Sharing**: Contribute to sustainability by sharing or claiming leftover foods in our food sharing section.

### Common Issues and How to Deal With Them

1. **Buttons Do Not React**: We use double click for our app. If a button does not react, click again and it should work as expected.
2. **The Generated Recipe Disappears after Pressing Download**: Don't panic, the recipe is automatically saved in your profile and downloaded as a .txt file to your computer.
3. **"http.client.CannotSendRequest"**: This error is caused by deta and unfortanely out of our control as it happens irregularly. It is [known](https://discuss.streamlit.io/t/error-https-client-cannot-sendrequest-deta-database-or-google-sheet-api/42107) but there is no known solution yet. You can try rerunning the app. If that does not work, please contact us and we will reboot the app so it will work again.

Built by [Sum](https://github.com/SumSumarie) and [Lennart](https://github.com/okamanhog)
