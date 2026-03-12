import streamlit as st

IMG="https://image.tmdb.org/t/p/w500"

def hero():
    st.markdown(
        """
        <div style="background:black;padding:40px;border-radius:10px">
        <h1 style="color:red">🎬 Go Movie Discovery</h1>
        <p style="color:white">Discover movies, actors, series, anime</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def movie_row(title,movies):

    st.subheader(title)

    cols=st.columns(5)

    for i,m in enumerate(movies[:10]):

        with cols[i%5]:

            if m.get("poster_path"):

                st.image(IMG+m["poster_path"])

                st.caption(m.get("title") or m.get("name"))
