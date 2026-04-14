import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

try:
    movies = pickle.load(open("movies_list.pkl","rb"))
    movies = pd.DataFrame(movies)

    vectors = pickle.load(open("movie_vectors.pkl","rb"))

    similarity = cosine_similarity(vectors)

    DATA_READY = True

except:
    DATA_READY = False


def recommend(movie):

    if not DATA_READY:
        return [], []

    if movie not in movies['title'].values:
        return [], []

    index = movies[movies['title']==movie].index[0]

    distances = similarity[index]

    movie_indices = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x:x[1]
    )[1:6]

    names = []
    ids = []

    for i in movie_indices:
        names.append(movies.iloc[i[0]].title)
        ids.append(movies.iloc[i[0]].id)

    return names, ids
