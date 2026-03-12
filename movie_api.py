import requests

API_KEY="624e1be491b94af1717b2ac8e121b5f1"


def search_multi(query):

    url=f"https://api.themoviedb.org/3/search/multi?api_key={API_KEY}&query={query}"

    data=requests.get(url).json()

    return data.get("results",[])


def get_movie(movie_id):

    url=f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"

    return requests.get(url).json()


def get_movie_recommendations(movie_id):

    url=f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations?api_key={API_KEY}"

    data=requests.get(url).json()

    return data.get("results",[])


def get_actor_movies(actor_id):

    url=f"https://api.themoviedb.org/3/person/{actor_id}/movie_credits?api_key={API_KEY}"

    data=requests.get(url).json()

    return data.get("cast",[])


def get_trailer(movie_id):

    url=f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={API_KEY}"

    data=requests.get(url).json()

    if "results" in data:

        for v in data["results"]:

            if v["type"]=="Trailer" and v["site"]=="YouTube":

                return "https://youtube.com/watch?v="+v["key"]

    return None


def get_ott(movie_id):

    url=f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={API_KEY}"

    data=requests.get(url).json()

    return data.get("results",{}).get("IN",{})
