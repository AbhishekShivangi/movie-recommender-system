import streamlit as st
import pickle
import pandas as pd
import requests
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Go Movie Recommender", page_icon="🎬", layout="wide")

# ---------- Custom CSS ----------
st.markdown("""
<style>

.title{
text-align:center;
font-size:50px;
font-weight:bold;
color:#ff4b4b;
}

.subtitle{
text-align:center;
font-size:18px;
color:gray;
margin-bottom:30px;
}

.stButton>button{
background-color:#ff4b4b;
color:white;
font-size:18px;
border-radius:10px;
padding:10px 20px;
}

.poster{
border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">🎬 Go Movie Recommender</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Search a movie and discover similar ones</p>', unsafe_allow_html=True)

# ---------- Load Data ----------
movies = pickle.load(open("movies_list.pkl","rb"))
movies = pd.DataFrame(movies)

vectors = pickle.load(open("movie_vectors.pkl","rb"))

similarity = cosine_similarity(vectors)

movie_titles = movies['title'].values


# ---------- Detect ID column ----------
if "movie_id" in movies.columns:
    id_column = "movie_id"
else:
    id_column = "id"


# ---------- Poster Function ----------
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


# ---------- Recommend ----------
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


# ---------- Search ----------
search_movie=st.text_input("🔎 Type Movie Name")

matches=[title for title in movie_titles if search_movie.lower() in title.lower()]


if search_movie:

    if matches:

        selected_movie=st.selectbox("Select Movie",matches)

        movie_id=movies[movies['title']==selected_movie].iloc[0][id_column]

        poster=fetch_poster(movie_id)

        st.subheader("Selected Movie")

        col1,col2=st.columns([1,2])

        with col1:
            st.image(poster,width=250)

        with col2:
            st.markdown(f"### {selected_movie}")
            st.write("Click recommend to see similar movies.")

        if st.button("🎬 Recommend Movies"):

            with st.spinner("Finding similar movies..."):

                names,posters=recommend(selected_movie)

            st.subheader("Recommended Movies")

            col1,col2,col3,col4,col5=st.columns(5)

            with col1:
                st.image(posters[0])
                st.caption(names[0])

            with col2:
                st.image(posters[1])
                st.caption(names[1])

            with col3:
                st.image(posters[2])
                st.caption(names[2])

            with col4:
                st.image(posters[3])
                st.caption(names[3])

            with col5:
                st.image(posters[4])
                st.caption(names[4])

    else:

        st.error("❌ Movie not found")

        st.image("https://via.placeholder.com/300x450?text=Movie+Not+Found")
