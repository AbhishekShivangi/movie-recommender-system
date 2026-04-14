import requests

API_KEY = "YOUR_API_KEY"

IMG = "https://image.tmdb.org/t/p/w500"


# 🔎 SEARCH (movie + actor + tv)
def search_multi(query):
    url = f"https://api.themoviedb.org/3/search/multi?api_key={API_KEY}&query={query}"
    return requests.get(url).json().get("results", [])


# 🎬 MOVIE DETAILS
def get_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
    data = requests.get(url).json()

    return {
        "title": data.get("title"),
        "rating": data.get("vote_average"),
        "overview": data.get("overview"),
        "poster": IMG + str(data.get("poster_path"))
    }


# 🎥 TRAILER
def get_trailer(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={API_KEY}"
    data = requests.get(url).json()

    for v in data.get("results", []):
        if v["type"] == "Trailer" and v["site"] == "YouTube":
            return "https://www.youtube.com/watch?v=" + v["key"]

    return None


# 📺 OTT PROVIDERS (India)
def get_ott(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={API_KEY}"
    data = requests.get(url).json()

    providers = []

    if "IN" in data.get("results", {}):
        p = data["results"]["IN"]

        if "flatrate" in p:
            for i in p["flatrate"]:
                providers.append(i["provider_name"])

    return providers


# 🔥 TRENDING
def get_trending():
    url = f"https://api.themoviedb.org/3/trending/movie/week?api_key={API_KEY}"
    return requests.get(url).json().get("results", [])


# 👨‍🎤 ACTOR MOVIES
def get_actor_movies(actor_id):
    url = f"https://api.themoviedb.org/3/person/{actor_id}/movie_credits?api_key={API_KEY}"
    return requests.get(url).json().get("cast", [])
