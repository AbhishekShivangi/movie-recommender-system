import streamlit as st
import pickle
import pandas as pd
import requests
import zipfile
import os
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Movie Recommender", layout="wide")

st.title("🎬 Movie Recommender System")

# ---------- Extract movie_vectors.zip ----------

if not os.path.exists("movie_vectors.pkl"):
    if os.path.exists("movie_vectors.zip"):
        with zipfile.ZipFile("movie_vectors.zip","r") as zip_ref:
            zip_ref.extractall()
    else:
        st.error("movie_vectors.zip not found in repository")
        st.stop()

# ---------- Load Data ----------

movies = pickle.load(open("movies_list.pkl","rb"))
movies = pd.DataFrame(movies)

vectors = pickle.load(open("movie_vectors.pkl","rb"))

similarity = cosine_similarity(vectors)

movie_list = movies['title'].values


# ---------- Detect ID column ----------

if "movie_id" in movies.columns:
    id_column = "movie_id"
elif "id" in movies.columns:
    id_column = "id"
else:
    st.error("Movie ID column not found")
    st.stop()


# ---------- Fetch Poster ----------

def fetch_poster(movie_id):

    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
        data = requests.get(url).json()

        poster_path = data.get("poster_path")

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/300x450"

    except:
        return "https://via.placeholder.com/300x450"


# ---------- Recommend Function ----------

def recommend(movie):

    index = movies[movies['title']==movie].index[0]

    distances = similarity[index]

    movie_indices = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x:x[1]
    )[1:6]

    names=[]
    posters=[]

    for i in movie_indices:

        movie_id = movies.iloc[i[0]][id_column]

        names.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))

    return names, posters


# ---------- UI ----------

selected_movie = st.selectbox(
    "Search Movie",
    movie_list
)

movie_id = movies[movies['title']==selected_movie].iloc[0][id_column]

poster = fetch_poster(movie_id)

st.subheader("Selected Movie")
st.image(poster, width=250)


if st.button("Recommend Movies"):

    names, posters = recommend(selected_movie)

    st.subheader("Recommended Movies")

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.image(posters[i])
            st.caption(names[i])
