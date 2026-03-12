import requests

API_KEY="YOUR_TMDB_API_KEY"

def get_movie_details(movie_id):

    url=f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

    data=requests.get(url).json()

    return {
        "title":data.get("title"),
        "rating":data.get("vote_average"),
        "overview":data.get("overview"),
        "popularity":data.get("popularity"),
        "poster":"https://image.tmdb.org/t/p/w500"+str(data.get("poster_path"))
    }


def get_trailer(movie_id):

    url=f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={API_KEY}"

    data=requests.get(url).json()

    if "results" in data:

        for video in data["results"]:

            if video["type"]=="Trailer" and video["site"]=="YouTube":

                return "https://www.youtube.com/watch?v="+video["key"]

    return None


def get_trending():

    url=f"https://api.themoviedb.org/3/trending/movie/week?api_key={API_KEY}"

    data=requests.get(url).json()

    return data.get("results",[])
