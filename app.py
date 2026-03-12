import streamlit as st
import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

st.title("🎬 Movie Recommender System")

movies = pickle.load(open("movies_list.pkl","rb"))
movies = pd.DataFrame(movies)

vectors = pickle.load(open("movie_vectors.pkl","rb"))

similarity = cosine_similarity(vectors)

movie_list = movies['title'].values


def recommend(movie):

    index = movies[movies['title']==movie].index[0]

    distances = similarity[index]

    movie_indices = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x:x[1]
    )[1:6]

    names=[]

    for i in movie_indices:
        names.append(movies.iloc[i[0]].title)

    return names


selected_movie = st.selectbox("Search Movie", movie_list)

if st.button("Recommend Movies"):

    names = recommend(selected_movie)

    st.subheader("Recommended Movies")

    for name in names:
        st.write(name)
