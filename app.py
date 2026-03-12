import streamlit as st
from movie_api import *
from movie_api import IMG

st.set_page_config(page_title="Go Movie Discovery", layout="wide")

st.title("🎬 Go Movie Discovery")

# STEP 1: session memory
if "selected_movie" not in st.session_state:
    st.session_state.selected_movie = None


# SEARCH BAR
# SEARCH BAR
query = st.text_input("🔎 Search Movie")

# SEARCH RESULT
if query:

    results = search_multi(query)

    if results:

        item = results[0]

        if item["media_type"] == "movie":

            movie_id = item["id"]

            m = movie_details(movie_id)

            st.title(m["title"])

            col1, col2 = st.columns([1,2])

            with col1:
                st.image(IMG + str(m["poster_path"]))

            with col2:
                st.write("⭐ Rating:", m["vote_average"])
                st.write(m["overview"])

            # TRAILER
            t = trailer(movie_id)

            if t:
                st.subheader("🎥 Trailer")
                st.video(t)

            # OTT
            providers = ott(movie_id)

            st.subheader("📺 Available On")

            if providers:
                for p in providers:
                    st.write("•", p)
            else:
                st.write("OTT data not available")
# ----------------------------
# STEP 2: SHOW TRENDING MOVIES
# ----------------------------
if not query:

    st.subheader("🔥 Trending Movies")

    movies = trending()

    cols = st.columns(5)

    for i, m in enumerate(movies[:5]):

        with cols[i]:

            st.image(IMG + str(m["poster_path"]))

            if st.button(m["title"]):

                st.session_state.selected_movie = m["id"]

# ----------------------------------
# STEP 3: MOVIE DETAIL PAGE
# ----------------------------------

if st.session_state.selected_movie:

    movie_id = st.session_state.selected_movie

    m = movie_details(movie_id)

    st.divider()

    st.title(m["title"])

    col1, col2 = st.columns([1,2])

    with col1:
        st.image(IMG + str(m["poster_path"]))

    with col2:

        st.write("⭐ Rating:", m["vote_average"])

        st.write(m["overview"])


# ----------------------------------
# STEP 4: TRAILER
# ----------------------------------

    t = trailer(movie_id)

    if t:

        st.subheader("🎥 Trailer")

        st.video(t)


# ----------------------------------
# STEP 5: OTT PLATFORMS
# ----------------------------------

    providers = ott(movie_id)

    st.subheader("📺 Available On")

    if providers:

        for p in providers:

            st.write("•", p)

    else:

        st.write("OTT data not available")


