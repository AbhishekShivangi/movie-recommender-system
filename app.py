import streamlit as st
import pickle
import pandas as pd

from recommender import recommend
from movie_api import get_movie_details, get_trailer
from ui import apply_custom_css, hero_section, search_bar, show_movie_details, recommendation_grid, movie_not_found


# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Go Movie Discovery",
    page_icon="🎬",
    layout="wide"
)

# ---------- UI STYLE ----------
apply_custom_css()

# ---------- HERO INTRO ----------
hero_section()

# ---------- LOAD DATA ----------
movies = pickle.load(open("movies_list.pkl", "rb"))
movies = pd.DataFrame(movies)

movie_titles = movies["title"].values


# ---------- SEARCH ----------
search = search_bar()

matches = [m for m in movie_titles if search.lower() in m.lower()]


if search:

    if matches:

        selected_movie = st.selectbox("Select Movie", matches)

        movie_id = movies[movies["title"] == selected_movie].iloc[0].id

        # ---------- MOVIE DETAILS ----------
        details = get_movie_details(movie_id)

        show_movie_details(details)

        # ---------- TRAILER ----------
        trailer = get_trailer(movie_id)

        if trailer:

            st.subheader("🎥 Trailer")

            st.video(trailer)

        # ---------- RECOMMEND BUTTON ----------
        if st.button("⭐ Recommend Similar Movies"):

            with st.spinner("Finding similar movies..."):

                names, ids = recommend(selected_movie)

            posters = []

            for i in ids:

                movie = get_movie_details(i)

                posters.append(movie["poster"])

            st.subheader("🍿 Recommended Movies")

            recommendation_grid(names, posters)

    else:

        movie_not_found()


# ---------- SIDEBAR ----------
st.sidebar.title("🎬 Go Movie Discovery")

st.sidebar.write("Movie Recommender Platform")

st.sidebar.write("Features:")

st.sidebar.write("⭐ Movie Search")
st.sidebar.write("🎥 Trailers")
st.sidebar.write("🍿 Recommendations")
st.sidebar.write("🔥 Trending Movies (coming soon)")
