import streamlit as st
import pickle
import pandas as pd

from movie_api import get_movie_details,get_trailer,get_trending,get_upcoming
from recommender import recommend
from ui import hero,show_movie,recommendation_grid,movie_not_found
from movie_api import get_kannada_movies


st.set_page_config(
page_title="Go Movie Discovery",
layout="wide"
)

hero()

movies = pickle.load(open("movies_list.pkl","rb"))
movies = pd.DataFrame(movies)

movie_titles = movies['title'].values

search = st.text_input("🔎 Search Movie")

matches=[m for m in movie_titles if search.lower() in m.lower()]

if search:

    if matches:

        selected_movie=st.selectbox("Select Movie",matches)

        movie_id=movies[movies['title']==selected_movie].iloc[0].id

        details=get_movie_details(movie_id)

        show_movie(details)

        trailer=get_trailer(movie_id)

        if trailer:

            st.subheader("🎥 Trailer")

            st.video(trailer)

        if st.button("⭐ Recommend Similar Movies"):

            names,ids=recommend(selected_movie)

            posters=[]

            for i in ids:

                movie=get_movie_details(i)

                posters.append(movie["poster"])

            st.subheader("🍿 Recommended Movies")

            recommendation_grid(names,posters)

    else:

        movie_not_found()


# ---------- Trending Movies ----------

st.subheader("🔥 Trending Movies")

trending=get_trending()

cols=st.columns(5)

for i,movie in enumerate(trending[:5]):

    with cols[i]:

        poster="https://image.tmdb.org/t/p/w500"+str(movie["poster_path"])

        st.image(poster)

        st.caption(movie["title"])


# ---------- Upcoming Movies ----------

st.subheader("🎬 Upcoming Movies")

upcoming=get_upcoming()

cols=st.columns(5)

for i,movie in enumerate(upcoming[:5]):

    with cols[i]:

        poster="https://image.tmdb.org/t/p/w500"+str(movie["poster_path"])

        st.image(poster)

        st.caption(movie["title"])

# ---------- Kannada Movies ----------
st.subheader("🌟 Sandalwood (Kannada) Movies")

kannada_movies = get_kannada_movies()

cols = st.columns(5)

for i,movie in enumerate(kannada_movies[:10]):

    with cols[i%5]:

        poster="https://image.tmdb.org/t/p/w500"+str(movie["poster_path"])

        st.image(poster)

        st.caption(movie["title"])

