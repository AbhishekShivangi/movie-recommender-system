import streamlit as st
import pickle
import requests
import certifi

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

st.title("🎬 Movie Recommender System")
st.write("Find movies similar to your favorite ones")

# Load files
movies = pickle.load(open("movies_list.pkl","rb"))
similarity = pickle.load(open("similarity.pkl","rb"))

movie_list = movies['title'].values


@st.cache_data
def fetch_poster(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"

    try:
        data = requests.get(url, verify=certifi.where()).json()
        poster_path = data.get("poster_path")

        return "https://image.tmdb.org/t/p/w500/" + poster_path

    except:
        return "https://via.placeholder.com/500x750"


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


selected_movie = st.selectbox("Select movie", movie_list)

if st.button("Recommend Movies"):

    names, posters = recommend(selected_movie)

    cols = st.columns(5)

    for i in range(5):

        with cols[i]:

            st.image(posters[i])
            st.caption(names[i])
