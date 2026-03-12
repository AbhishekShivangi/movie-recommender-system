import streamlit as st
from movie_api import *
from recommender import recommend

st.set_page_config(page_title="Go Movie Discovery",layout="wide")

# load css
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)

# hero
st.markdown("""
<div class='hero'>
<h1 style='color:red'>🎬 Go Movie Discovery</h1>
<p style='color:white'>Discover movies, actors, anime and series</p>
</div>
""",unsafe_allow_html=True)

query = st.text_input("🔎 Search Movie, Actor, Series, Anime")

if query:

    results = search_multi(query)

    if results:

        item = results[0]

        media = item["media_type"]

        # MOVIE
        if media == "movie":

            movie_id = item["id"]

            details = get_movie_details(movie_id)

            st.image("https://image.tmdb.org/t/p/w500"+str(details["poster_path"]))

            st.title(details["title"])

            st.write("⭐ Rating:", details["vote_average"])

            st.write(details["overview"])

        # ACTOR
        elif media == "person":

            st.title(item["name"])

            actor_id = item["id"]

            movies = get_actor_movies(actor_id)

            st.subheader("Movies")

            cols = st.columns(5)

            for i,m in enumerate(movies[:5]):

                with cols[i]:

                    poster="https://image.tmdb.org/t/p/w500"+str(m["poster_path"])

                    st.image(poster)

                    st.caption(m["title"])

        # TV / SERIES
        elif media == "tv":

            st.title(item["name"])

            poster="https://image.tmdb.org/t/p/w500"+str(item["poster_path"])

            st.image(poster)

            st.write(item["overview"])

# trending
st.subheader("🔥 Trending Movies")

cols=st.columns(5)

for i,m in enumerate(trending()[:5]):

    with cols[i]:

        st.image("https://image.tmdb.org/t/p/w500"+str(m["poster_path"]))

        st.caption(m["title"])

# upcoming
st.subheader("🎬 Upcoming Movies")

cols=st.columns(5)

for i,m in enumerate(upcoming()[:5]):

    with cols[i]:

        st.image("https://image.tmdb.org/t/p/w500"+str(m["poster_path"]))

        st.caption(m["title"])

# indian sections
st.subheader("🇮🇳 Bollywood")

cols=st.columns(5)

for i,m in enumerate(indian("hi")[:5]):

    with cols[i]:

        st.image("https://image.tmdb.org/t/p/w500"+str(m["poster_path"]))

        st.caption(m["title"])

st.subheader("🎬 Tollywood")

cols=st.columns(5)

for i,m in enumerate(indian("te")[:5]):

    with cols[i]:

        st.image("https://image.tmdb.org/t/p/w500"+str(m["poster_path"]))

        st.caption(m["title"])

st.subheader("🌟 Sandalwood")

cols=st.columns(5)

for i,m in enumerate(indian("kn")[:5]):

    with cols[i]:

        st.image("https://image.tmdb.org/t/p/w500"+str(m["poster_path"]))

        st.caption(m["title"])

# tv
st.subheader("📺 TV Series")

cols=st.columns(5)

for i,m in enumerate(tv()[:5]):

    with cols[i]:

        st.image("https://image.tmdb.org/t/p/w500"+str(m["poster_path"]))

        st.caption(m["name"])

# anime
st.subheader("🍥 Anime")

cols=st.columns(5)

for i,m in enumerate(anime()[:5]):

    with cols[i]:

        st.image("https://image.tmdb.org/t/p/w500"+str(m["poster_path"]))

        st.caption(m["name"])

