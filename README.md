
# Content-Based Movie Recommender

A personalized movie recommendation system powered by content-based filtering — built with Python and Streamlit.  
Inspired by Netflix, this project lets you discover similar movies based on content, genre, cast, and more!

## 🔥 Features

- 🎬 **Hero Card Style UI** – Like Netflix tiles
- ⭐ **Movie Ratings** – View average votes from users
- 📺 **Trailers** – Watch YouTube trailers right inside the app
- 📂 **Watchlist** – Save movies you want to check out later
- 🎭 **Genre Filters** – Filter recommendations by genre
- ⚡ **Streamlit Web App** – Fast, interactive, and clean UI

## 🧠 Tech Stack

- `Python 3`
- `Pandas`, `Scikit-learn`, `NumPy`
- `Streamlit`
- `TMDB 5000 Movies Dataset`
- `TMDB 5000 Credits Dataset`
- `Content-Based Filtering (NLP + Cosine Similarity)`

## 📊 Datasets Used

- **tmdb_5000_movies.csv** – Contains movie titles, genres, keywords, overview, and other metadata.
- **tmdb_5000_credits.csv** – Includes cast and crew details (used to extract actors and directors).

These are merged and cleaned for the recommendation model.

## 🚀 How to Run It Locally

1. **Clone the repo:**
   ```bash
   git clone https://github.com/YogeshCruz/content-based-movie-recommender.git
   cd content-based-movie-recommender
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app:**
   ```bash
   streamlit run app.py
   ```

## 🧠 How it Works

- Extracts features like cast, director, genre, keywords.
- Converts them into vectors using **CountVectorizer**.
- Measures similarity using **cosine similarity**.
- Recommends movies based on user selection.

## 📸 Preview
![UI Preview](assets/image.png)
![Another Preview](assets/ui.jpg)



## 🤝 Contribution

## 🤝 Contribution

Pull requests are welcome! If you have ideas, found bugs, or want to contribute in any way, feel free to open an issue or submit a pull request. 

You can also connect with me on [LinkedIn](https://www.linkedin.com/in/yogeshwaran-k-363800210/) to discuss or share feedback. 😊


