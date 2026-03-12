import streamlit as st
from movie_api import *

st.set_page_config(page_title="Go Movie Discovery", layout="wide")

st.title("🎬 Go Movie Discovery Platform")

mode = st.radio(
    "Search Type",
    ["Movie", "Actor"]
)

# ---------- MOVIE SEARCH ----------
if mode == "Movie":

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

            trailer = get_trailer(movie_id)

            if trailer:

                st.subheader("🎥 Trailer")

                st.video(trailer)

            # OTT
            st.subheader("📺 Watch On")

            providers = get_ott(movie_id)

            if providers:

                st.write(providers)

            else:

                st.write("OTT info not available")

        else:

            st.error("Movie not found")


# ---------- ACTOR SEARCH ----------
if mode == "Actor":

    actor = st.text_input("👨‍🎤 Search Actor")

    if actor:

        results = search_actor(actor)

        if results:

            actor_data = results[0]

            actor_id = actor_data["id"]

            st.subheader(actor_data["name"])

            movies = get_actor_movies(actor_id)

            st.subheader("🎬 Movies")

            cols = st.columns(5)

            for i, m in enumerate(movies[:10]):

                with cols[i % 5]:

                    poster = "https://image.tmdb.org/t/p/w500" + str(m["poster_path"])

                    st.image(poster)

                    st.caption(m["title"])

        else:

            st.error("Actor not found")
