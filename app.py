import streamlit as st
from api import *
from components.cards import movie_row

st.set_page_config(page_title="Go Movie Discovery",layout="wide")

# load css
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)


st.markdown(
"""
<div class='hero'>
<h1 style='color:red'>🎬 Go Movie Discovery</h1>
<p style='color:white'>Discover movies, actors, anime and series</p>
</div>
""",
unsafe_allow_html=True
)

query=st.text_input("🔎 Search movie or actor")


if query:

    results=search(query)

    if results:

        item=results[0]

        if item["media_type"]=="movie":

            m=movie(item["id"])

            col1,col2=st.columns([1,2])

            with col1:
                st.image("https://image.tmdb.org/t/p/w500"+str(m["poster_path"]))

            with col2:
                st.title(m["title"])
                st.write("⭐ Rating:",m["vote_average"])
                st.write(m["overview"])

            movie_row("🍿 Recommended",recommendations(item["id"]))

        if item["media_type"]=="person":

            st.title(item["name"])

            movie_row("🎬 Movies",actor_movies(item["id"]))


movie_row("🔥 Trending Movies",trending())

movie_row("⭐ Popular Movies",popular())

movie_row("🇮🇳 Bollywood",indian("hi"))

movie_row("🎬 Tollywood",indian("te"))

movie_row("🌟 Sandalwood",indian("kn"))

movie_row("📺 TV Series",tv())

movie_row("🍥 Anime",anime())
