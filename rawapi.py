import streamlit as st
import requests
import top_rated_products
import pandas as pd
import os
from config import RAWG_API_KEY


# Function to fetch game details from the RAWG API for specific game names
@st.cache_data
def fetch_game_details(game_name):
    api_url = f"https://api.rawg.io/api/games"
    params = {
        "key": RAWG_API_KEY,
        "search": game_name,
        "page_size": 1
    }

    response = requests.get(api_url, params=params)

    if response.status_code == 200 and response.json()["results"]:
        return response.json()["results"][0]
    else:
        return None

# Streamlit app
def main():
    st.set_page_config(
        page_title="Game Info App",
        page_icon=":video_game:",
        layout="wide",
        initial_sidebar_state="auto"
    )

    # Navbar
    st.markdown(
        """
        <style>
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            # background-image: url('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQIEdl4fUSBe5s2irQmtDVomA_89P7qbeafTw&usqp=CAU');
            background: linear-gradient(to right, #000, #0079FF);
            background-size: 100%;
            color: black;
            padding: 10px;
            # border-top: 2px solid #FE0000; 
            border-bottom: 5px solid #00235B;
            # border-left: 2px solid #FE0000;   /* Add left border */
            # border-right: 2px solid #FE0000;  /* Add right border */

            margin: 0 -20px;  /* Extend to edges of the page */
        }
        .navbar a {
            color: white;
            text-decoration: italics;
            margin: 0 10px;
            font-weight: bold;
        }
        .game-card {
            border-radius: 8px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.3), 
                        inset 0 0 40px rgba(255, 255, 255, 0.1);  /* Gradient shadow */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <style>
        body {
            background: linear-gradient(to bottom right, #000, #0079FF);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="navbar">
            <div>
                <a href="#"><img src="https://img.freepik.com/premium-photo/cyberpunk-gaming-controller-gamepad-joystick-illustration_691560-5778.jpg?size=626&ext=jpg" alt="Game Recom Logo" style="width: 50px; height: auto;"></a>
            </div>
            <div>
                <a href="#game-info">HOME</a>
            <a href="#top-games">TOP GAMES</a>
                <a href="#about-us">ABOUT US</a>
                <a href="#contact-us">CONTACT US</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<a name="game-info"></a>', unsafe_allow_html=True)
    st.title("Game Recommendation and Information App")
    with st.form("search-form"):
        search_query = st.text_input("Search for a game:", "")
        search_button = st.form_submit_button("Search")

    if search_query and search_button:
        game_data = fetch_game_details(search_query)
        if game_data:
            display_game_card(game_data)
        else:
            st.warning(f"No game details found for '{search_query}'")

    final_rating = pd.read_csv("final_rating.csv")
    interactions_matrix = pd.read_csv("interactions_matrix.csv")
    game_names = list(top_rated_products.top_n_products(final_rating, 5, 50))
    st.write("OR")
    with st.form("recommendation-form"):
        user_id = st.number_input("Enter your User ID:", min_value=0, step=1)
        recommend_button = st.form_submit_button("Recommend Games")

    if recommend_button:
        if user_id is not None and user_id != "":
            user_id = int(user_id)
            recommended_games = list(top_rated_products.recommendations(
                user_id, 5, interactions_matrix))
            st.title("Recommended Games")
            st.write(f"Recommended games for User {user_id}:")
            for idx, game_name in enumerate(recommended_games, start=1):
                rec_game_data = fetch_game_details(game_name)
                if rec_game_data:
                    st.write(f"### {idx}. {game_name}")
                    display_game_card(rec_game_data)
                    st.write("\n")
                else:
                    st.warning(f"No game details found for '{game_name}'")
        else:
            st.warning("Please enter a valid User ID.")

    st.title("Top Games")
    st.markdown('<a name="top-games"></a>', unsafe_allow_html=True)
    for idx, game_name in enumerate(game_names, start=1):
        game_data = fetch_game_details(game_name)
        if game_data:
            st.write(f"### {idx}. {game_name}")
            display_game_card(game_data)
            st.write("\n")
        else:
            st.warning(f"No game details found for '{game_name}'")


def display_game_card(game):
    with st.container():
        cols = st.columns(3)
        with cols[0]:
            if "background_image" in game:
                st.image(game["background_image"],
                         caption=game["name"], width=450)
        with cols[1]:
            st.write(f"## {game['name']}")
            if "rating" in game:
                st.write("#### Rating")
                st.write(f"⭐ {game['rating']} / 5")
        with cols[2]:
            if "genres" in game:
                st.write("#### Genres")
                genres = [genre["name"] for genre in game["genres"]]
                st.write(", ".join(genres))
            if "released" in game:
                st.write("#### Release Date")
                st.write(game["released"])
        st.write("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()

    st.markdown('<a name="about-us"></a>', unsafe_allow_html=True)
    st.title("About Us")
    st.write("We are a group of college students enthusiastic about problem solving and new technology. Our goal is to create innovative solutions that make a positive impact.")
    st.markdown('<a name="contact-us"></a>', unsafe_allow_html=True)
    st.title("Contact Us")
    st.write("Feel free to get in touch with us!")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Shubham Solanki")
        st.write("Email: [solanki.4@iitj.ac.in](mailto:solanki.4@iitj.ac.in)")
        st.write("Contact No: +91 9428173430")
        st.write("College: IIT Jodhpur")
        st.write("LinkedIn: [Shubham Solanki LinkedIn](https://www.linkedin.com/in/shubham-solanki-699baa239/)")
        st.write("GitHub: [Shubham Solanki GitHub](https://github.com/Shubham163solanki)")

    with col2:
        st.subheader("Yash Jangir")
        st.write("Email: [jangir.8@iitj.ac.in](mailto:jangir.8@iitj.ac.in)")
        st.write("Contact No: +91 9828061918")
        st.write("College: IIT Jodhpur")
        st.write("LinkedIn: [Yash Jangir LinkedIn](https://www.linkedin.com/in/yash-jangir-18b880232/)")
        st.write("GitHub: [Yash Jangir GitHub](https://github.com/yash-yj10)")


    st.markdown('<div style="margin-bottom: 20px;"></div>', unsafe_allow_html=True)
    st.markdown(
        """
        <style>
        .footer {
            text-align: center;
            padding: 10px 0;
            background-color: #333;
            color: white;
            position: fixed;
            bottom: 0;
            width: 100%;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <footer style="text-align: center; padding: 10px 0; background-color: #333; color: white; margin: 0 -20px;">
            &copy; 2023 Game Recom. All rights reserved.
        </footer>
        """,
        unsafe_allow_html=True
    )
