import pickle
import pandas as pd
from fetch_api import fetch_movie_details

# Load data
movies_dict = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(movie):
    """Get movie recommendations based on similarity scores."""
    try:
        index = movies[movies['title'] == movie].index[0]
    except IndexError:
        return [], [], [], [], []

    distances = similarity[index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:15]

    movie_ids, recommended_movies = [], []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        movie_ids.append(movie_id)
        recommended_movies.append(movies.iloc[i[0]].title)
        if len(movie_ids) == 5:  # Limit to 5 recommendations
            break

    # Fetch details in bulk
    movies_data = fetch_movie_details(movie_ids)
    recommended_posters, recommended_trailers, recommended_ratings, recommended_genres = zip(*movies_data)

    return recommended_movies, recommended_posters, recommended_trailers, recommended_ratings, recommended_genres
