import streamlit as st
import pickle
import requests
import certifi
import pandas as pd

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

st.title("🎬 Movie Recommender System")
st.write("Find movies similar to your favorite ones")

# Load movies data
movies = pickle.load(open("movies_list.pkl","rb"))
movies = pd.DataFrame(movies)

movie_list = movies['title'].values


@st.cache_data
def fetch_poster(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"

    try:
        data = requests.get(url, verify=certifi.where()).json()
        poster_path = data.get("poster_path")

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750"

    except:
        return "https://via.placeholder.com/500x750"


selected_movie = st.selectbox(
    "Select a movie",
    movie_list
)

if st.button("Show Movie Poster"):

    movie_id = movies[movies['title']==selected_movie].iloc[0].id

    poster = fetch_poster(movie_id)

    st.image(poster)
