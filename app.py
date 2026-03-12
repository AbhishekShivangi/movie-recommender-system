import streamlit as st
import pickle
import requests
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

st.title("🎬 Movie Recommender System")
st.write("Find movies similar to your favorite ones")

# Load movie data safely
try:
    movies = pickle.load(open("movies_list.pkl","rb"))
    movies = pd.DataFrame(movies)
except:
    st.error("movies_list.pkl file not found or corrupted")
    st.stop()

# Ensure tags column exists
if 'tags' not in movies.columns:
    st.error("Dataset must contain a 'tags' column")
    st.stop()

# Convert tags to text
movies['tags'] = movies['tags'].astype(str)

movie_titles = movies['title'].values

# Vectorize tags
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(movies['tags']).toarray()

similarity = cosine_similarity(vectors)


@st.cache_data
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
        data = requests.get(url).json()
        poster_path = data.get("poster_path")
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    except:
        return "https://via.placeholder.com/500x750"


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]

    movie_indices = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    names = []
    posters = []

    for i in movie_indices:
        movie_id = movies.iloc[i[0]].id
        names.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))

    return names, posters


selected_movie = st.selectbox("Select a movie", movie_titles)

if st.button("Recommend Movies"):
    names, posters = recommend(selected_movie)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.image(posters[i])
            st.caption(names[i])
