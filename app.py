import streamlit as st
from api import *

st.set_page_config(page_title="Go Movie Discovery",layout="wide")

st.title("🎬 Go Movie Discovery Platform")

query=st.text_input("🔎 Search movie or actor")

if query:

    results=search_multi(query)

    if results:

        item=results[0]

        # ---------- MOVIE ----------
        if item["media_type"]=="movie":

            movie_id=item["id"]

            movie=get_movie(movie_id)

            poster="https://image.tmdb.org/t/p/w500"+str(movie["poster_path"])

            col1,col2=st.columns([1,2])

            with col1:
                st.image(poster,width=250)

            with col2:

                st.subheader(movie["title"])

                st.write("⭐ Rating:",movie["vote_average"])

                st.write(movie["overview"])

            trailer=get_trailer(movie_id)

            if trailer:
                st.video(trailer)

            # ---------- OTT ----------
            st.subheader("📺 Available On")

            ott=get_ott(movie_id)

            if ott:

                if "flatrate" in ott:

                    for p in ott["flatrate"]:

                        st.write(p["provider_name"])

            else:

                st.write("OTT info not available")

            # ---------- RECOMMENDED ----------
            st.subheader("🍿 Recommended Movies")

            rec=get_movie_recommendations(movie_id)

            cols=st.columns(5)

            for i,m in enumerate(rec[:10]):

                with cols[i%5]:

                    poster="https://image.tmdb.org/t/p/w500"+str(m["poster_path"])

                    st.image(poster)

                    st.caption(m["title"])


        # ---------- ACTOR ----------
        if item["media_type"]=="person":

            actor_id=item["id"]

            st.subheader(item["name"])

            movies=get_actor_movies(actor_id)

            st.subheader("🎬 Movies by this actor")

            cols=st.columns(5)

            for i,m in enumerate(movies[:10]):

                with cols[i%5]:

                    poster="https://image.tmdb.org/t/p/w500"+str(m["poster_path"])

                    st.image(poster)

                    st.caption(m["title"])

    else:

        st.error("Not found")
