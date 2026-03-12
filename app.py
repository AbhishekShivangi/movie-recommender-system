import streamlit as st
import pickle
import requests
import pandas as pd
import zipfile
import os
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

st.title("🎬 Movie Recommender System")
st.write("Find movies similar to your favorite ones")

# ---------- Extract vectors ----------

if not os.path.exists("movie_vectors.pkl"):
    if os.path.exists("movie_vectors.zip"):
        with zipfile.ZipFile("movie_vectors.zip", "r") as zip_ref:
            zip_ref.extractall()

# ---------- Load Data ----------

try:
    movies = pickle.load(open("movies_list.pkl","rb"))
    movies = pd.DataFrame(movies)
except:
    st.error("movies_list.pkl not found or corrupted")
    st.stop()

try:
    vectors = pickle.load(open("movie_vectors.pkl","rb"))
except:
    st.error("movie_vectors.pkl not found after extraction")
    st.stop()

# Calculate similarity
similarity = cosine_similarity(vectors)

movie_list = movies['title'].values


# ---------- Fetch Poster ----------

@st.cache_data
def fetch_poster(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"

    try:
        data = requests.get(url).json()
        poster_path = data.get("poster_path")

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750"

    except:
        return "https://via.placeholder.com/500x750"


# ---------- Recommendation ----------

def recommend(movie):

    try:
        index = movies[movies['title'] == movie].index[0]
    except:
        st.error("Movie not found in dataset")
        return [], []

    distances = similarity[index]

    movie_indices = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    names = []
    posters = []

    for i in movie_indices:

        try:
            movie_id = movies.iloc[i[0]].id
        except:
            movie_id = None

        names.append(movies.iloc[i[0]].title)

        if movie_id:
            posters.append(fetch_poster(movie_id))
        else:
            posters.append("https://via.placeholder.com/500x750")

    return names, posters


# ---------- UI ----------

selected_movie = st.selectbox("Select a movie", movie_list)

if st.button("Recommend Movies"):

    names, posters = recommend(selected_movie)

    if len(names) == 0:
        st.error("Recommendation failed.")
    else:

        cols = st.columns(5)

        for i in range(5):
            with cols[i]:
                st.image(posters[i])
                st.caption(names[i])
