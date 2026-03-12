import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

movies = pickle.load(open("movies_list.pkl","rb"))
movies = pd.DataFrame(movies)

vectors = pickle.load(open("movie_vectors.pkl","rb"))

similarity = cosine_similarity(vectors)

def recommend(movie):

    index=movies[movies['title']==movie].index[0]

    distances=similarity[index]

    movie_indices=sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x:x[1]
    )[1:6]

    movie_titles=[]
    movie_ids=[]

    for i in movie_indices:

        movie_titles.append(movies.iloc[i[0]].title)
        movie_ids.append(movies.iloc[i[0]].id)

    return movie_titles,movie_ids
