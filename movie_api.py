import requests

API_KEY="624e1be491b94af1717b2ac8e121b5f1"

IMG="https://image.tmdb.org/t/p/w500"


# SEARCH MOVIE / ACTOR / SERIES
def search_multi(query):

    url=f"https://api.themoviedb.org/3/search/multi?api_key={API_KEY}&query={query}"

    return requests.get(url).json().get("results",[])


# MOVIE DETAILS
def movie_details(movie_id):

    url=f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"

    return requests.get(url).json()


# TRAILER
def trailer(movie_id):

    url=f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={API_KEY}"

    data=requests.get(url).json()

    for v in data.get("results",[]):

        if v["type"]=="Trailer" and v["site"]=="YouTube":

            return "https://youtube.com/watch?v="+v["key"]

    return None


# OTT PLATFORMS
def ott(movie_id):

    url=f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={API_KEY}"

    data=requests.get(url).json()

    providers=[]

    if "results" in data and "IN" in data["results"]:

        p=data["results"]["IN"]

        if "flatrate" in p:

            for i in p["flatrate"]:

                providers.append(i["provider_name"])

    return providers


# TRENDING
def trending():

    url=f"https://api.themoviedb.org/3/trending/movie/week?api_key={API_KEY}"

    return requests.get(url).json()["results"]


# UPCOMING
def upcoming():

    url=f"https://api.themoviedb.org/3/movie/upcoming?api_key={API_KEY}"

    return requests.get(url).json()["results"]


# TOP RATED
def top_rated():

    url=f"https://api.themoviedb.org/3/movie/top_rated?api_key={API_KEY}"

    return requests.get(url).json()["results"]


# INDIAN MOVIES
def indian():

    url=f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&region=IN"

    return requests.get(url).json()["results"]


# TV SERIES
def tv():

    url=f"https://api.themoviedb.org/3/discover/tv?api_key={API_KEY}"

    return requests.get(url).json()["results"]


# ANIME
def anime():

    url=f"https://api.themoviedb.org/3/discover/tv?api_key={API_KEY}&with_genres=16"

    return requests.get(url).json()["results"]
