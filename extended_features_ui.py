import streamlit as st
from fetch_api import fetch_movie_details

# Sample movie ID to feature (e.g., Avatar = 19995)
featured_movie_id = 19995  # You can replace this with any movie_id from your dataset

# Fetch movie details
poster_url, trailer_url, rating, genres = fetch_movie_details([featured_movie_id])[0]

# Set page layout
st.set_page_config(layout="wide")

# Navigation to other UI
st.markdown("""
    <a href="http://localhost:8502" target="_blank">
        <button style='padding: 0.5rem 1rem; border-radius: 8px; background: #ff4b2b; color: white; border: none; margin-bottom: 1rem;'>
            🚀 Explore More Features
        </button>
    </a>
""", unsafe_allow_html=True)

# Hero Section
if poster_url:
    hero_style = f"""
        <style>
        .hero-container {{
            position: relative;
            background-image: url('{poster_url}');
            background-size: cover;
            background-position: center;
            height: 500px;
            border-radius: 15px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.6);
        }}
        .overlay-content {{
            position: absolute;
            bottom: 30px;
            left: 40px;
            color: white;
            text-shadow: 1px 1px 2px black;
        }}
        .watch-button {{
            background: linear-gradient(to right, #ff416c, #ff4b2b);
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            border: none;
            font-weight: bold;
            margin-right: 10px;
            cursor: pointer;
            text-decoration: none;
        }}
        .add-button {{
            background: rgba(255,255,255,0.2);
            border: 2px solid white;
            padding: 10px 15px;
            border-radius: 50%;
            color: white;
            font-size: 18px;
            cursor: pointer;
        }}
        </style>
        <div class="hero-container">
            <div class="overlay-content">
                <h1>Featured: Avatar</h1>
                <p>Rating: ⭐ {rating} | Genres: {genres}</p>
                <a href="{trailer_url}" target="_blank" class="watch-button">▶ Watch Now</a>
                <button class="add-button">+</button>
            </div>
        </div>
    """
    st.markdown(hero_style, unsafe_allow_html=True)
else:
    st.warning("Poster not available.")
