import streamlit as st
from movie_api import *
from recommender import recommend

st.set_page_config(page_title="Go Movie Discovery", layout="wide")

st.title("🎬 Go Movie Discovery Platform")

# SEARCH BAR
query = st.text_input("🔎 Search Movie, Actor, Series")

# ------------------------------------
# IF USER SEARCHES
# ------------------------------------

if query:

    results = search_multi(query)

    if results:

        item = results[0]

        if item["media_type"] == "movie":

            movie_id = item["id"]

            details = get_movie_details(movie_id)

            col1, col2 = st.columns([1,2])

            with col1:
                st.image("https://image.tmdb.org/t/p/w500"+str(details["poster_path"]))

            with col2:
                st.title(details["title"])
                st.write("⭐ Rating:", details["vote_average"])
                st.write(details["overview"])

            trailer = get_trailer(movie_id)

            if trailer:
                st.subheader("🎥 Trailer")
                st.video(trailer)

            # RECOMMENDATIONS
            st.subheader("🍿 Recommended Movies")

            try:

                names, ids = recommend(details["title"])

                cols = st.columns(5)

                for i in range(5):

                    with cols[i]:

                        movie = get_movie_details(ids[i])

                        st.image("https://image.tmdb.org/t/p/w500"+str(movie["poster_path"]))

                        st.caption(names[i])

            except:
                st.write("No recommendation available.")

    else:
        st.error("Movie not found")

# ------------------------------------
# IF NO SEARCH → HOMEPAGE
# ------------------------------------

else:

    st.subheader("🔥 Trending Movies")

    trending_movies = trending()

    cols = st.columns(5)

    for i,m in enumerate(trending_movies[:5]):

        with cols[i]:

            poster = "https://image.tmdb.org/t/p/w500"+str(m["poster_path"])

            st.image(poster)

            st.caption(m["title"])

    st.subheader("🎬 Upcoming Movies")

    upcoming_movies = upcoming()

    cols = st.columns(5)

    for i,m in enumerate(upcoming_movies[:5]):

        with cols[i]:

            poster = "https://image.tmdb.org/t/p/w500"+str(m["poster_path"])

            st.image(poster)

            st.caption(m["title"])
