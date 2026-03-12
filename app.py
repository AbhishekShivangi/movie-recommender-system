import streamlit as st
import pickle
import requests
import certifi
import gdown
import os

# ---------------- Page Settings ----------------
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Movie Recommender System")
st.write("Find movies similar to your favorite ones")

# ---------------- Download similarity.pkl if missing ----------------


FILE_ID = "1O4pQe4NbRTeZcbx4PyxDSzr9uClGWH6D"
URL = "https://docs.google.com/uc?export=download"

def download_file_from_google_drive(file_id, destination):
    session = requests.Session()

    response = session.get(URL, params={'id': file_id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:
                f.write(chunk)

if not os.path.exists("similarity.pkl"):
    st.write("Downloading recommendation model... please wait ⏳")
    download_file_from_google_drive(FILE_ID, "similarity.pkl")
# ---------------- Load Data ----------------

movies = pickle.load(open("movies_list.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

movies_list = movies['title'].values


# ---------------- Fetch Poster ----------------

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


# ---------------- Recommendation Function ----------------

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


# ---------------- UI ----------------

selected_movie = st.selectbox(
    "Select a movie",
    movies_list
)


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





