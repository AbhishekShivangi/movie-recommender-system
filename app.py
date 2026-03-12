import streamlit as st
from api import *
from ui import *
from charts import *
from components.cards import movie_row_scroll

st.set_page_config(page_title="Go Movie Discovery",layout="wide")

# load CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)

hero_banner()

query=st.text_input("🔎 Search movie, actor, anime, series")

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

            trailer_url=trailer(item["id"])

            trailer_preview(trailer_url)

            st.subheader("📺 OTT Platforms")

            providers=ott(item["id"])

            if providers and "flatrate" in providers:

                for p in providers["flatrate"]:
                    st.write(p["provider_name"])

            movie_row_scroll("🍿 Recommended",recommendations(item["id"]))

        if item["media_type"]=="person":

            st.title(item["name"])

            movie_row_scroll("🎬 Movies",actor_movies(item["id"]))


movie_row_scroll("🔥 Trending Movies",trending())

movie_row_scroll("⭐ Popular Movies",popular())

movie_row_scroll("🇮🇳 Bollywood",indian("hi"))

movie_row_scroll("🎬 Tollywood",indian("te"))

movie_row_scroll("🌟 Sandalwood",indian("kn"))

movie_row_scroll("📺 TV Series",tv())

movie_row_scroll("🍥 Anime",anime())

st.header("📊 Popularity Chart")

popularity_chart(trending())
