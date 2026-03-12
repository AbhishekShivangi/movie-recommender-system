import requests

API_KEY = "624e1be491b94af1717b2ac8e121b5f1"

def trending():

    url = f"https://api.themoviedb.org/3/trending/movie/week?api_key={API_KEY}"

    data = requests.get(url).json()

    return data.get("results",[])


def popular():

    url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}"

    data = requests.get(url).json()

    return data.get("results",[])


def indian(lang):

    url=f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&with_original_language={lang}"

    data=requests.get(url).json()

    return data.get("results",[])
