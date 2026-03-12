import requests

API_KEY = "624e1be491b94af1717b2ac8e121b5f1"


def search_movie(query):

    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={query}"

    data = requests.get(url).json()

    return data.get("results", [])


def get_movie_details(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"

    data = requests.get(url).json()

    return {
        "title": data.get("title"),
        "rating": data.get("vote_average"),
        "overview": data.get("overview"),
        "poster": "https://image.tmdb.org/t/p/w500" + str(data.get("poster_path"))
    }


def get_trailer(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={API_KEY}"

    data = requests.get(url).json()

    if "results" in data:

        for v in data["results"]:

            if v["type"] == "Trailer" and v["site"] == "YouTube":

                return "https://www.youtube.com/watch?v=" + v["key"]

    return None


def get_trending():

    url = f"https://api.themoviedb.org/3/trending/movie/week?api_key={API_KEY}"

    data = requests.get(url).json()

    return data.get("results", [])


def get_upcoming():

    url = f"https://api.themoviedb.org/3/movie/upcoming?api_key={API_KEY}"

    data = requests.get(url).json()

    return data.get("results", [])
