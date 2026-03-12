import streamlit as st
import pickle
import requests
import certifi
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Movie Recommender System", page_icon="🎬", layout="wide")

st.title("🎬 Movie Recommender System")
st.write("Find movies similar to your favorite ones")

# Load data
movies = pickle.load(open("movies_list.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))   # small file instead of similarity.pkl

movies_list = movies['title'].values


# Fetch movie poster
@st.cache_data
def fetch_poster(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"

    try:
        data = requests.get(url, verify=certifi.where()).json()
        poster_path = data.get("poster_path")

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"

    except:
        return "https://via.placeholder.com/500x750?text=Error"


def recommend(movie):

    index = movies[movies['title'] == movie].index[0]

    similarity = cosine_similarity([vectors[index]], vectors)[0]

    movie_list = sorted(list(enumerate(similarity)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:

        movie_id = movies.iloc[i[0]]['id']

        recommended_movies.append(movies.iloc[i[0]]['title'])
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters


selected_movie = st.selectbox("Select a movie", movies_list)

if st.button("Recommend Movies"):

    names, posters = recommend(selected_movie)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.image(posters[i])
            st.caption(names[i])

