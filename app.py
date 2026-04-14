import streamlit as st
from movie_api import *

st.set_page_config(page_title="Go Movie Discovery", layout="wide")

st.title("🎬 Go Movie Discovery Platform")

# -------------------------
# SEARCH BAR
# -------------------------
query = st.text_input("🔎 Search Movie / Actor / Series")

# -------------------------
# SEARCH SECTION (SAFE)
# -------------------------
if query:

    results = search_multi(query)

    if not results:
        st.error("❌ No results found")
    else:

        item = results[0]

        media = item.get("media_type")

        # -------------------------
        # MOVIE
        # -------------------------
        if media == "movie":

            movie_id = item.get("id")

            m = movie_details(movie_id)

            if m:

                col1, col2 = st.columns([1,2])

                with col1:
                    if m.get("poster_path"):
                        st.image(IMG + m["poster_path"])
                    else:
                        st.write("No poster")

                with col2:
                    st.title(m.get("title","No title"))
                    st.write("⭐ Rating:", m.get("vote_average","N/A"))
                    st.write(m.get("overview","No description"))

                # Trailer
                t = trailer(movie_id)
                if t:
                    st.subheader("🎥 Trailer")
                    st.video(t)

                # OTT
                st.subheader("📺 Available On")

                providers = ott(movie_id)

                if providers:
                    for p in providers:
                        st.write("•", p)
                else:
                    st.write("No OTT data")

        # -------------------------
        # ACTOR
        # -------------------------
        elif media == "person":

            st.title(item.get("name","Actor"))

            actor_movies = get_actor_movies(item["id"])

            st.subheader("🎬 Movies")

            cols = st.columns(5)

            for i, m in enumerate(actor_movies[:5]):

                with cols[i]:

                    if m.get("poster_path"):
                        st.image(IMG + m["poster_path"])

                    st.caption(m.get("title","No title"))

        # -------------------------
        # TV / ANIME
        # -------------------------
        elif media == "tv":

            st.title(item.get("name","Series"))

            if item.get("poster_path"):
                st.image(IMG + item["poster_path"])

            st.write(item.get("overview","No description"))

# -------------------------
# HOMEPAGE (NO SEARCH)
# -------------------------
else:

    st.subheader("🔥 Trending Movies")

    cols = st.columns(5)

    for i, m in enumerate(trending()[:5]):

        with cols[i]:

            if m.get("poster_path"):
                st.image(IMG + m["poster_path"])

            st.caption(m.get("title"))

    st.subheader("🎬 Upcoming Movies")

    cols = st.columns(5)

    for i, m in enumerate(upcoming()[:5]):

        with cols[i]:

            if m.get("poster_path"):
                st.image(IMG + m["poster_path"])

            st.caption(m.get("title"))

    st.subheader("🇮🇳 Indian Movies")

    cols = st.columns(5)

    for i, m in enumerate(indian()[:5]):

        with cols[i]:

            if m.get("poster_path"):
                st.image(IMG + m["poster_path"])

            st.caption(m.get("title"))

    st.subheader("📺 TV Series")

    cols = st.columns(5)

    for i, m in enumerate(tv()[:5]):

        with cols[i]:

            if m.get("poster_path"):
                st.image(IMG + m["poster_path"])

            st.caption(m.get("name"))

    st.subheader("🍥 Anime")

    cols = st.columns(5)

    for i, m in enumerate(anime()[:5]):

        with cols[i]:

            if m.get("poster_path"):
                st.image(IMG + m["poster_path"])

            st.caption(m.get("name"))
