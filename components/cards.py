import streamlit as st

IMG = "https://image.tmdb.org/t/p/w500"

def movie_row_scroll(title, movies):

    st.subheader(title)

    html = "<div class='movie-row'>"

    for m in movies[:20]:

        if m.get("poster_path"):

            poster = IMG + m["poster_path"]

            html += f"""
            <div class="movie-card">
                <img src="{poster}">
                <p style="color:white;text-align:center">
                {m.get("title") or m.get("name")}
                </p>
            </div>
            """

    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)
