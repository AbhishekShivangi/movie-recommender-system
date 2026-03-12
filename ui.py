import streamlit as st


# ---------- PAGE STYLE ----------
def apply_custom_css():

    st.markdown("""
    <style>

    body {
        background-color:#0e1117;
        color:white;
    }

    .main-title{
        text-align:center;
        font-size:50px;
        font-weight:bold;
        color:#ff4b4b;
    }

    .subtitle{
        text-align:center;
        color:gray;
        font-size:18px;
        margin-bottom:30px;
    }

    .movie-card{
        background-color:#111;
        padding:10px;
        border-radius:10px;
        text-align:center;
        transition:0.3s;
    }

    .movie-card:hover{
        transform:scale(1.05);
    }

    .poster{
        border-radius:10px;
    }

    .stButton>button{
        background-color:#ff4b4b;
        color:white;
        font-size:16px;
        border-radius:8px;
        padding:8px 20px;
    }

    </style>
    """, unsafe_allow_html=True)


# ---------- HERO BANNER ----------
def hero_section():

    st.markdown("""
    <div style="
        background-image:linear-gradient(to right,#000000,#141414);
        padding:40px;
        border-radius:12px;
        text-align:center;
    ">
        <h1 style="color:#ff4b4b;">🎬 Go Movie Discovery</h1>
        <p style="color:#ccc;">Find movies, trailers, ratings and recommendations</p>
    </div>
    """, unsafe_allow_html=True)


# ---------- SEARCH BAR ----------
def search_bar():

    return st.text_input("🔎 Search Movie")


# ---------- MOVIE DETAILS ----------
def show_movie_details(details):

    col1, col2 = st.columns([1,2])

    with col1:
        st.image(details["poster"], width=250)

    with col2:

        st.subheader(details["title"])
        st.write("⭐ Rating:", details["rating"])
        st.write("🔥 Popularity:", details["popularity"])

        st.write(details["overview"])


# ---------- MOVIE CARD ----------
def movie_card(title, poster):

    st.markdown("<div class='movie-card'>", unsafe_allow_html=True)

    st.image(poster, use_column_width=True)

    st.caption(title)

    st.markdown("</div>", unsafe_allow_html=True)


# ---------- RECOMMENDATION GRID ----------
def recommendation_grid(names, posters):

    cols = st.columns(5)

    for i in range(5):

        with cols[i]:

            movie_card(names[i], posters[i])


# ---------- MOVIE NOT FOUND ----------
def movie_not_found():

    st.error("❌ Movie not found")

    st.image("https://via.placeholder.com/300x450?text=Movie+Not+Found")