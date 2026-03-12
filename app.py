import streamlit as st
from movie_api import *
import plotly.express as px

st.set_page_config(page_title="Go Movie Discovery",layout="wide")

st.title("🎬 Go Movie Discovery")

# SEARCH
query=st.text_input("🔎 Search Movie / Actor / Series")

# -----------------------
# SEARCH RESULT
# -----------------------

if query:

    results=search_multi(query)

    if results:

        item=results[0]

        if item["media_type"]=="movie":

            m=movie_details(item["id"])

            col1,col2=st.columns([1,2])

            with col1:

                st.image(IMG+m["poster_path"])

            with col2:

                st.header(m["title"])

                st.write("⭐ Rating:",m["vote_average"])

                st.write(m["overview"])

            # TRAILER
            t=trailer(item["id"])

            if t:

                st.video(t)

            # OTT
            st.subheader("📺 Available On")

            providers=ott(item["id"])

            if providers:

                for p in providers:

                    st.write("•",p)

            else:

                st.write("No OTT data")

    else:

        st.error("Movie not found")

# -----------------------
# HOMEPAGE
# -----------------------

else:

    # TRENDING
    st.subheader("🔥 Trending")

    cols=st.columns(6)

    for i,m in enumerate(trending()[:6]):

        with cols[i]:

            st.image(IMG+m["poster_path"])

            st.caption(m["title"])


    # UPCOMING
    st.subheader("🎬 Upcoming")

    cols=st.columns(6)

    for i,m in enumerate(upcoming()[:6]):

        with cols[i]:

            st.image(IMG+m["poster_path"])

            st.caption(m["title"])


    # TOP RATED
    st.subheader("⭐ Top Rated")

    cols=st.columns(6)

    for i,m in enumerate(top_rated()[:6]):

        with cols[i]:

            st.image(IMG+m["poster_path"])

            st.caption(m["title"])


    # INDIAN MOVIES
    st.subheader("🇮🇳 Indian Movies")

    cols=st.columns(6)

    for i,m in enumerate(indian()[:6]):

        with cols[i]:

            st.image(IMG+m["poster_path"])

            st.caption(m["title"])


    # TV
    st.subheader("📺 TV Series")

    cols=st.columns(6)

    for i,m in enumerate(tv()[:6]):

        with cols[i]:

            st.image(IMG+m["poster_path"])

            st.caption(m["name"])


    # ANIME
    st.subheader("🍥 Anime")

    cols=st.columns(6)

    for i,m in enumerate(anime()[:6]):

        with cols[i]:

            st.image(IMG+m["poster_path"])

            st.caption(m["name"])


    # POPULARITY CHART
    st.subheader("📊 Popularity Chart")

    movies=trending()[:10]

    names=[m["title"] for m in movies]

    scores=[m["popularity"] for m in movies]

    fig=px.bar(x=names,y=scores)

    st.plotly_chart(fig)
