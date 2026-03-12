import streamlit as st
import pickle
import pandas as pd
import zipfile
import os
from sklearn.metrics.pairwise import cosine_similarity

st.title("Movie Recommender Debug")

# extract zip
if not os.path.exists("movie_vectors.pkl"):
    if os.path.exists("movie_vectors.zip"):
        with zipfile.ZipFile("movie_vectors.zip","r") as zip_ref:
            zip_ref.extractall()

# load data
movies = pickle.load(open("movies_list.pkl","rb"))
movies = pd.DataFrame(movies)

vectors = pickle.load(open("movie_vectors.pkl","rb"))

st.write("Movies shape:", movies.shape)
st.write("Vectors shape:", vectors.shape)

similarity = cosine_similarity(vectors)

movie_list = movies['title'].values

selected_movie = st.selectbox("Select movie", movie_list)

if st.button("Recommend"):

    try:

        index = movies[movies['title']==selected_movie].index[0]

        distances = similarity[index]

        movie_indices = sorted(
            list(enumerate(distances)),
            reverse=True,
            key=lambda x:x[1]
        )[1:6]

        for i in movie_indices:
            st.write(movies.iloc[i[0]].title)

    except Exception as e:
        st.error(e)
