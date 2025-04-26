import requests
import streamlit as st
import time

def fetch_movie_details(movie_ids):
    """Fetch movie details from TMDB API with retry logic and better connection handling."""
    
    api_key = st.secrets.get("tmdb", {}).get("api_key")

    if not api_key:
        st.error("API Key is missing! Check your Streamlit secrets.")
        return []

    base_url = "https://api.themoviedb.org/3/movie/"
    movies_data = []

    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    for movie_id in movie_ids:
        url = f"{base_url}{movie_id}?api_key={api_key}&language=en-US&append_to_response=videos"

        for attempt in range(3):
            try:
                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code == 429:  # Rate limit error
                    st.warning("⚠️ TMDB API Rate Limit hit. Waiting 10 seconds...")
                    time.sleep(10)
                    continue  # Retry after waiting
                
                response.raise_for_status()
                data = response.json()

                poster_path = data.get('poster_path') or data.get('backdrop_path')
                full_poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

                rating = data.get('vote_average', 'N/A')
                genres = ", ".join([genre['name'] for genre in data.get('genres', [])]) if data.get('genres') else "Unknown"

                trailer_key = next((video['key'] for video in data.get('videos', {}).get('results', []) if video['type'] == 'Trailer'), None)
                trailer_url = f"https://www.youtube.com/watch?v={trailer_key}" if trailer_key else None

                movies_data.append((full_poster_url, trailer_url, rating, genres))
                break  # Successful request, move to next movie

            except requests.exceptions.ConnectionError:
                st.warning(f"Connection lost for movie {movie_id}. Retrying in 5 seconds...")
                time.sleep(5)
            except requests.exceptions.RequestException as e:
                st.warning(f"Error fetching movie {movie_id}: {e}. Retrying in 5 seconds...")
                time.sleep(5)
        
        else:
            st.error(f"❌ Failed to fetch movie {movie_id} after 3 attempts.")
            movies_data.append((None, None, 'N/A', "Unknown"))

        time.sleep(2)  # Avoid hitting rate limits

    return movies_data
