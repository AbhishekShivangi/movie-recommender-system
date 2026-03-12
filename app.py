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

# ---------- Extract ZIP if needed ----------

if not os.path.exists("movie_vectors.pkl"):

    if os.path.exists("movie_vectors.zip"):
        with zipfile.ZipFile("movie_vectors.zip", "r") as zip_ref:
            zip_ref.extractall()

    # search for movie_vectors.pkl inside extracted folders
    for root, dirs, files in os.walk("."):
        if "movie_vectors.pkl" in files:
            os.rename(os.path.join(root, "movie_vectors.pkl"), "movie_vectors.pkl")
            break

# ---------- Load Data ----------

movies = pickle.load(open("movies_list.pkl","rb"))
movies = pd.DataFrame(movies)

vectors = pickle.load(open("movie_vectors.pkl","rb"))

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

    index = movies[movies['title']==movie].index[0]

    distances = similarity[index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x:x[1]
    )[1:6]

    names=[]
    posters=[]

    for i in movie_list:
        movie_id = movies.iloc[i[0]].id
        names.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))

    return names, posters


# ---------- UI ----------

selected_movie = st.selectbox(
    "Select a movie",
    movie_list
)

if st.button("Recommend Movies"):

    names, posters = recommend(selected_movie)

    col1,col2,col3,col4,col5 = st.columns(5)

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
