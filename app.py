import streamlit as st
from movie_api import *

st.set_page_config(page_title="Go Movie Discovery", layout="wide")

st.title("🎬 Go Movie Discovery Platform")

# -----------------------------
# SEARCH BAR + SUGGESTIONS
# -----------------------------
query = st.text_input("🔎 Search Movie / Actor / Series")

suggestions = []

if query:
    results = search_multi(query)

    for r in results[:5]:
        if r.get("title"):
            suggestions.append(r["title"])
        elif r.get("name"):
            suggestions.append(r["name"])

selected = None

if suggestions:
    selected = st.selectbox("Suggestions", suggestions)

final_query = selected if selected else query


# -----------------------------
# SEARCH RESULT
# -----------------------------
if final_query:

    results = search_multi(final_query)

    if results:

        item = results[0]
        media = item.get("media_type")

        # 🎬 MOVIE
        if media == "movie":

            movie_id = item["id"]

            m = get_movie_details(movie_id)

            col1, col2 = st.columns([1,2])

            with col1:
                st.image(m["poster"])

            with col2:
                st.title(m["title"])
                st.write("⭐ Rating:", m["rating"])
                st.write(m["overview"])

            # 🎥 TRAILER
            trailer = get_trailer(movie_id)

            if trailer:
                st.subheader("🎥 Trailer")
                st.video(trailer)

            # 📺 OTT
            st.subheader("📺 Watch On")

            providers = get_ott(movie_id)

            if providers:

                for p in providers:

                    if "Netflix" in p:
                        st.link_button("Watch on Netflix", "https://www.netflix.com")

                    elif "Amazon" in p:
                        st.link_button("Watch on Prime", "https://www.primevideo.com")

                    elif "Hotstar" in p:
                        st.link_button("Watch on Hotstar", "https://www.hotstar.com")

                    else:
                        st.write(p)

            else:
                st.write("No OTT data available")


        # 👨‍🎤 ACTOR SEARCH
        elif media == "person":

            st.title(item.get("name"))

            movies = get_actor_movies(item["id"])

            st.subheader("🎬 Movies")

            cols = st.columns(5)

            for i, m in enumerate(movies[:5]):

                with cols[i]:

                    if m.get("poster_path"):
                        st.image("https://image.tmdb.org/t/p/w500" + m["poster_path"])

                    st.caption(m.get("title"))


        # 📺 TV / ANIME
        elif media == "tv":

            st.title(item.get("name"))

            if item.get("poster_path"):
                st.image("https://image.tmdb.org/t/p/w500" + item["poster_path"])

            st.write(item.get("overview"))

    else:
        st.error("❌ No results found")


# -----------------------------
# HOMEPAGE
# -----------------------------
else:

    st.subheader("🔥 Trending Movies")

    movies = get_trending()

    cols = st.columns(5)

    for i, m in enumerate(movies[:5]):

        with cols[i]:

            if m.get("poster_path"):
                st.image("https://image.tmdb.org/t/p/w500" + m["poster_path"])

            st.caption(m.get("title"))
