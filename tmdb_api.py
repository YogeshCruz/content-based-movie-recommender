import requests

TMDB_API_KEY = "bc793e1c279b8489fcd3f0b3e36559d1"  # Replace with your actual API key

def get_trending_movies():
    url = f"https://api.themoviedb.org/3/trending/movie/week?api_key={TMDB_API_KEY}"
    response = requests.get(url).json()
    
    trending_movies = []
    for movie in response['results'][:5]:  # Get top 5 trending movies
        trending_movies.append((movie['title'], f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"))
    
    return trending_movies

def get_movie_trailer(movie_title):
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_title}"
    search_response = requests.get(search_url).json()
    
    if search_response['results']:
        movie_id = search_response['results'][0]['id']
        video_url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={TMDB_API_KEY}"
        video_response = requests.get(video_url).json()

        for video in video_response['results']:
            if video['type'] == 'Trailer' and video['site'] == 'YouTube':
                return f"https://www.youtube.com/watch?v={video['key']}"

    return None  # No trailer found
