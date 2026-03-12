import streamlit as st

def hero():

    st.markdown(
    """
    <h1 style='text-align:center;color:#ff4b4b'>
    🎬 Go Movie Discovery Platform
    </h1>
    """,
    unsafe_allow_html=True
    )

    st.write("Search movies, watch trailers and get recommendations.")


def show_movie(details):

    col1,col2=st.columns([1,2])

    with col1:
        st.image(details["poster"],width=250)

    with col2:

        st.subheader(details["title"])

        st.write("⭐ Rating:",details["rating"])

        st.write("🔥 Popularity:",details["popularity"])

        st.write(details["overview"])


def recommendation_grid(names,posters):

    cols=st.columns(5)

    for i in range(5):

        with cols[i]:

            st.image(posters[i])

            st.caption(names[i])


def movie_not_found():

    st.error("Movie not found")

    st.image("https://via.placeholder.com/300x450?text=Movie+Not+Found")
