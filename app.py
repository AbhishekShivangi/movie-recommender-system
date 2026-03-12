import streamlit as st
import pickle
import pandas as pd

from movie_api import search_movie, get_movie_details, get_trailer, get_trending, get_upcoming
from recommender import recommend

st.set_page_config(page_title="Go Movie Discovery", layout="wide")

st.title("🎬 Go Movie Discovery Platform")

# ---------- Load dataset ----------
movies = pickle.load(open("movies_list.pkl","rb"))
movies = pd.DataFrame(movies)


# ---------- SEARCH ----------
query = st.text_input("🔎 Search Movie")

if query:

    results = search_movie(query)

    if results:

        movie = results[0]

        movie_id = movie["id"]

        details = get_movie_details(movie_id)

        col1, col2 = st.columns([1,2])

        with col1:
            st.image(details["poster"], width=250)

        with col2:

            st.subheader(details["title"])

            st.write("⭐ Rating:", details["rating"])

            st.write(details["overview"])

        # ---------- TRAILER ----------
        trailer = get_trailer(movie_id)

        if trailer:

            st.subheader("🎥 Trailer")

            st.video(trailer)

        # ---------- RECOMMEND ----------
        st.subheader("🍿 Recommended Movies")

        try:

            names, ids = recommend(details["title"])

            posters = []

            for i in ids:

                movie_data = get_movie_details(i)

                posters.append(movie_data["poster"])

            cols = st.columns(5)

            for i in range(5):

                with cols[i]:

                    st.image(posters[i])

                    st.caption(names[i])

        except:

            st.write("No recommendations available.")

    else:

        st.error("Movie not found")


# ---------- Trending ----------
st.subheader("🔥 Trending Movies")

trending = get_trending()

cols = st.columns(5)

for i,m in enumerate(trending[:5]):

    with cols[i]:

        poster = "https://image.tmdb.org/t/p/w500"+str(m["poster_path"])

        st.image(poster)

        st.caption(m["title"])


# ---------- Upcoming ----------
st.subheader("🎬 Upcoming Movies")

upcoming = get_upcoming()

cols = st.columns(5)

for i,m in enumerate(upcoming[:5]):

    with cols[i]:

        poster = "https://image.tmdb.org/t/p/w500"+str(m["poster_path"])

        st.image(poster)

        st.caption(m["title"])
