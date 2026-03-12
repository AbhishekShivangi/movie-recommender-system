import requests

API_KEY="624e1be491b94af1717b2ac8e121b5f1"

IMG="https://image.tmdb.org/t/p/w500"


def search_movie(query):

    url=f"https://api.themoviedb.org/3/search/multi?api_key={API_KEY}&query={query}"

    return requests.get(url).json().get("results",[])


def get_movie_details(movie_id):

    url=f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"

    data=requests.get(url).json()

    return data


def get_trailer(movie_id):

    url=f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={API_KEY}"

    data=requests.get(url).json()

    for v in data.get("results",[]):

        if v["type"]=="Trailer" and v["site"]=="YouTube":

            return "https://youtube.com/watch?v="+v["key"]

    return None


def trending():

    url=f"https://api.themoviedb.org/3/trending/movie/week?api_key={API_KEY}"

    return requests.get(url).json().get("results",[])


def upcoming():

    url=f"https://api.themoviedb.org/3/movie/upcoming?api_key={API_KEY}"

    return requests.get(url).json().get("results",[])


def indian(lang):

    url=f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&with_original_language={lang}"

    return requests.get(url).json().get("results",[])


def tv():

    url=f"https://api.themoviedb.org/3/discover/tv?api_key={API_KEY}"

    return requests.get(url).json().get("results",[])


def anime():

    url=f"https://api.themoviedb.org/3/discover/tv?api_key={API_KEY}&with_genres=16"

    return requests.get(url).json().get("results",[])
    

def search_multi(query):

    url = f"https://api.themoviedb.org/3/search/multi?api_key={API_KEY}&query={query}"

    data = requests.get(url).json()
    

def get_actor_movies(actor_id):

    url = f"https://api.themoviedb.org/3/person/{actor_id}/movie_credits?api_key={API_KEY}"

    data = requests.get(url).json()

    return data.get("cast", [])

    return data.get("results", [])


