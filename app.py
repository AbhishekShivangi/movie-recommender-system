import streamlit as st
import pickle
import pandas as pd
import requests
from sklearn.metrics.pairwise import cosine_similarity

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Go Movie Recommender", page_icon="🎬", layout="wide")

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>

body { background-color:#0e1117; }

.hero {
height:280px;
background-image: linear-gradient(to right, rgba(0,0,0,0.85), rgba(0,0,0,0.3)),
url("https://images.unsplash.com/photo-1489599849927-2ee91cede3ba");
background-size: cover;
border-radius:12px;
padding:30px;
color:white;
}

.hero h1{
font-size:48px;
margin-bottom:5px;
}

.hero p{
font-size:18px;
color:#dddddd;
}

.poster{
border-radius:10px;
transition:0.3s;
}

.poster:hover{
transform:scale(1.05);
}

.stButton>button{
background-color:#e50914;
color:white;
font-size:18px;
border-radius:8px;
padding:10px 25px;
}

.card{
text-align:center;
}

</style>
""", unsafe_allow_html=True)

# ---------- HERO INTRO ----------
st.markdown("""
<div class="hero">
<h1>🎬 Go Movie Recommender</h1>
<p>Discover movies and series you'll love. Type a title to start exploring!</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------- LOAD DATA ----------
movies = pickle.load(open("movies_list.pkl","rb"))
movies = pd.DataFrame(movies)

vectors = pickle.load(open("movie_vectors.pkl","rb"))

similarity = cosine_similarity(vectors)

movie_titles = movies['title'].values

# detect movie id column
if "movie_id" in movies.columns:
    id_column = "movie_id"
else:
    id_column = "id"


# ---------- POSTER FUNCTION ----------
@st.cache_data
def fetch_poster(movie_id):
    try:
        url=f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
        data=requests.get(url,timeout=5).json()

        poster=data.get("poster_path")

        if poster:
            return "https://image.tmdb.org/t/p/w500/"+poster

        return "https://via.placeholder.com/300x450?text=No+Poster"

    except:
        return "https://via.placeholder.com/300x450?text=Error"


# ---------- RECOMMEND ----------
def recommend(movie):

    index=movies[movies['title']==movie].index[0]

    distances=similarity[index]

    movie_indices=sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x:x[1]
    )[1:6]

    names=[]
    posters=[]

    for i in movie_indices:

        movie_id=movies.iloc[i[0]][id_column]

        names.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))

    return names,posters


# ---------- SIDEBAR ----------
st.sidebar.title("🎥 Options")

show_trending = st.sidebar.checkbox("Show Trending Movies")

if show_trending:
    st.sidebar.write("Trending movies feature coming soon!")


# ---------- SEARCH ----------
search_query = st.text_input("🔎 Search Movie or Series")

matches = [m for m in movie_titles if search_query.lower() in m.lower()]

if search_query:

    if matches:

        selected_movie = st.selectbox("Select Movie", matches)

        movie_id = movies[movies['title']==selected_movie].iloc[0][id_column]

        poster = fetch_poster(movie_id)

        st.subheader("Selected Movie")

        col1,col2 = st.columns([1,2])

        with col1:
            st.image(poster,width=260)

        with col2:
            st.markdown(f"### {selected_movie}")
            st.write("Click recommend to discover similar movies.")

        if st.button("🎬 Recommend Movies"):

            with st.spinner("Finding similar movies..."):

                names,posters = recommend(selected_movie)

            st.subheader("Recommended Movies")

            c1,c2,c3,c4,c5 = st.columns(5)

            with c1:
                st.image(posters[0], use_column_width=True)
                st.caption(names[0])

            with c2:
                st.image(posters[1], use_column_width=True)
                st.caption(names[1])

            with c3:
                st.image(posters[2], use_column_width=True)
                st.caption(names[2])

            with c4:
                st.image(posters[3], use_column_width=True)
                st.caption(names[3])

            with c5:
                st.image(posters[4], use_column_width=True)
                st.caption(names[4])

    else:

        st.error("❌ Movie not found")

        st.image("https://via.placeholder.com/300x450?text=Movie+Not+Found")
