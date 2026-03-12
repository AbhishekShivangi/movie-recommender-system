import streamlit as st
import pickle
import requests
import certifi
import zipfile
import os

# Page configuration
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# Title
st.title("🎬 Movie Recommender System")
st.write("Find movies similar to your favorite ones")

# ---------- Load Data ----------

# Load movies list
movies = pickle.load(open("movies_list.pkl", "rb"))

# Extract similarity.pkl if zipped
if not os.path.exists("similarity.pkl"):
    with zipfile.ZipFile("similarity.zip", "r") as zip_ref:
        zip_ref.extractall()

# Load similarity matrix
similarity = pickle.load(open("similarity.pkl", "rb"))

movies_list = movies['title'].values


# ---------- Fetch Poster ----------
@st.cache_data
def fetch_poster(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"

    try:
        response = requests.get(url, verify=certifi.where(), timeout=5)
        data = response.json()

        poster_path = data.get("poster_path")

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"

    except:
        return "https://via.placeholder.com/500x750?text=Error"


# ---------- Recommendation Function ----------
def recommend(movie):

    index = movies[movies['title'] == movie].index[0]

    distances = similarity[index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:

        movie_id = movies.iloc[i[0]]['id']

        recommended_movies.append(movies.iloc[i[0]]['title'])

        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters


# ---------- UI Dropdown ----------
selected_movie = st.selectbox(
    "Select a movie",
    movies_list
)


# ---------- Button ----------
if st.button("Recommend Movies"):

    names, posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image(posters[0])
        st.caption(names[0])

    with col2:
        st.image(posters[1])
        st.caption(names[1])

    with col3:
        st.image(posters[2])
        st.caption(names[2])

    with col4:
        st.image(posters[3])
        st.caption(names[3])

    with col5:
        st.image(posters[4])
        st.caption(names[4])
