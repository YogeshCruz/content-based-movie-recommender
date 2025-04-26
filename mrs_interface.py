import streamlit as st
import pickle
import pandas as pd
import time
from fetch_api import fetch_movie_details as raw_fetch
from streamlit_autorefresh import st_autorefresh
import random

@st.cache_data(show_spinner=False)
def fetch_movie_details(ids):
    return raw_fetch(ids)

# === LOAD DATA ===
with open("movies.pkl", "rb") as file:
    movies = pickle.load(file)

if isinstance(movies, dict):
    movies_df = pd.DataFrame(movies)
else:
    movies_df = movies

with open("similarity.pkl", "rb") as file:
    similarity = pickle.load(file)

movie_list = movies_df["title"].values

st.set_page_config(layout="wide")

# === RECOMMEND FUNCTION ===
def recommend(movie):
    index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie_titles = []
    recommended_movie_ids = []
    for i in movie_list:
        movie_id = movies_df.iloc[i[0]].movie_id
        recommended_movie_ids.append(movie_id)
        recommended_movie_titles.append(movies_df.iloc[i[0]].title)

    return recommended_movie_titles, recommended_movie_ids

# === AUTO-REFRESH HERO ONLY ===
st_autorefresh(interval=3000, key="hero_refresh")

if "hero_index" not in st.session_state:
    st.session_state.hero_index = 0

featured_ids = [19995, 27205, 155, 1726]  # Avatar, Inception, The Dark Knight, Pulp Fiction

st.session_state.hero_index = (st.session_state.hero_index + 1) % len(featured_ids)

posters_info = fetch_movie_details(featured_ids)

current_index = st.session_state.hero_index
poster_url, trailer_url, rating, genres = posters_info[current_index]
title = movies_df[movies_df['movie_id'] == featured_ids[current_index]]['title'].values[0]

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
                <h1>Featured: {title}</h1>
                <p>Rating: ⭐ {rating} | Genres: {genres}</p>
                <a href="{trailer_url}" target="_blank" class="watch-button">▶ Watch Now</a>
                <button class="add-button">+</button>
            </div>
        </div>
    """
    st.markdown(hero_style, unsafe_allow_html=True)
else:
    st.warning("Poster not available.")

# === MOVIE RECOMMENDER UI ===
st.divider()
st.subheader("🎥 Select a Movie to Get Recommendations")

selected_movie = st.selectbox("Choose a movie", movie_list)

# === SURPRISE ME BUTTON ===
if st.button("🎲 Surprise Me!"):
    random_movie = random.choice(movie_list)
    st.session_state.random_movie = random_movie
    st.success(f"Surprised! Try this one: {random_movie}")
    st.session_state.selected_detail = None  # reset detail view if any

# Use surprise movie if present
if "random_movie" in st.session_state:
    selected_movie = st.session_state.random_movie


if st.button("Recommend"):
    with st.spinner("🍿 Recommending movies... sit tight!"):
        
        recommended_titles, recommended_ids = recommend(selected_movie)
        posters = fetch_movie_details(recommended_ids)
        st.session_state.recommended_titles = recommended_titles
        st.session_state.recommended_posters = posters
        st.session_state.random_movie = None


if "recommended_titles" in st.session_state and "recommended_posters" in st.session_state:
    st.subheader("Recommended Movies")
    recommended_titles = st.session_state.recommended_titles
    posters = st.session_state.recommended_posters

    if "selected_detail" not in st.session_state:
        st.session_state.selected_detail = None

    cols = st.columns(5)
    for i, col in enumerate(cols):
        title = recommended_titles[i]
        poster_url, trailer_url, rating, genres = posters[i]
        with col:
            if st.button(f"🎬 {title}", key=f"btn_{i}"):
                st.session_state.selected_detail = {
                    "title": title,
                    "poster": poster_url,
                    "trailer": trailer_url,
                    "rating": rating,
                    "genres": genres
                }
            st.image(poster_url, use_column_width=True)
            st.markdown(f"**{title}**")
            st.markdown(f"⭐ {rating}")
            st.markdown(f"[▶ Trailer]({trailer_url})")

    if st.session_state.selected_detail:
        st.divider()
        detail = st.session_state.selected_detail
        st.subheader(f"🎥 {detail['title']}")
        cols = st.columns([1, 2])
        with cols[0]:
            st.image(detail["poster"], use_column_width=True)
        with cols[1]:
            st.markdown(f"**Rating:** ⭐ {detail['rating']}")
            st.markdown(f"**Genres:** {detail['genres']}")
            st.markdown(f"[▶ Watch Trailer]({detail['trailer']})", unsafe_allow_html=True)

# === WATCHLIST ===
# === WATCHLIST ===
# === WATCHLIST SECTION ===
# === WATCHLIST SECTION ===
st.divider()
st.subheader("🎯 Your Watchlist")

# Initialize watchlist
if "watchlist" not in st.session_state:
    st.session_state.watchlist = []

# Add or remove from watchlist from selected detail
if "selected_detail" in st.session_state and st.session_state.selected_detail:
    detail = st.session_state.selected_detail

    # Check if already in watchlist
    already_added = any(
        isinstance(m, dict) and m.get("title") == detail["title"]
        for m in st.session_state.watchlist
    )

    col1, col2 = st.columns([1, 5])
    with col1:
        if not already_added:
            if st.button("➕ Add to Watchlist", key=f"add_{detail['title']}"):
                st.session_state.watchlist.append(detail)
                st.success("Added to watchlist!")
        else:
            if st.button("❌ Remove from Watchlist", key=f"remove_{detail['title']}"):
                st.session_state.watchlist = [
                    m for m in st.session_state.watchlist
                    if not (isinstance(m, dict) and m.get("title") == detail["title"])
                ]
                st.warning("Removed from watchlist.")
                st.experimental_rerun()

# Display the watchlist
if st.session_state.watchlist:
    for i, item in enumerate(st.session_state.watchlist):
        with st.container():
            cols = st.columns([1, 2, 1])

            if isinstance(item, dict):
                with cols[0]:
                    st.image(item.get("poster", ""), width=100)
                with cols[1]:
                    st.markdown(f"**🎬 {item.get('title', 'Untitled')}**")
                    st.markdown(f"⭐ {item.get('rating', 'N/A')}  |  🎞️ {item.get('genres', 'Unknown')}")
                    st.markdown(f"[▶ Watch Trailer]({item.get('trailer', '#')})", unsafe_allow_html=True)
                with cols[2]:
                    if st.button("❌", key=f"remove_{i}"):
                        st.session_state.watchlist.pop(i)
                        st.experimental_rerun()
else:
    st.info("Your watchlist is empty. Add some movies to get started!")
