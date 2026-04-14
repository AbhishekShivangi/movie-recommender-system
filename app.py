import streamlit as st
import requests

# -----------------------------
# CONFIG
# -----------------------------
API_KEY = "624e1be491b94af1717b2ac8e121b5f1"
IMG = "https://image.tmdb.org/t/p/w500"

st.set_page_config(page_title="Go Movie Discovery", layout="wide")

# -----------------------------
# CSS (simple animation)
# -----------------------------
st.markdown("""
<style>
img {
    border-radius:10px;
    transition:0.3s;
}
img:hover {
    transform:scale(1.08);
}
</style>
""", unsafe_allow_html=True)

st.title("🎬 Go Movie Discovery Platform")

# -----------------------------
# FUNCTIONS
# -----------------------------
def search_movie(query):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={query}"
    return requests.get(url).json().get("results", [])

def search_actor(query):
    url = f"https://api.themoviedb.org/3/search/person?api_key={API_KEY}&query={query}"
    return requests.get(url).json().get("results", [])

def get_trailer(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={API_KEY}"
    data = requests.get(url).json()
    for v in data.get("results", []):
        if v["type"] == "Trailer":
            return "https://youtube.com/watch?v=" + v["key"]
    return None

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

def get_actor_movies(actor_id):
    url = f"https://api.themoviedb.org/3/person/{actor_id}/movie_credits?api_key={API_KEY}"
    return requests.get(url).json().get("cast", [])

def trending():
    url = f"https://api.themoviedb.org/3/trending/movie/week?api_key={API_KEY}"
    return requests.get(url).json().get("results", [])


# -----------------------------
# SEARCH + SUGGESTIONS
# -----------------------------
query = st.text_input("🔎 Search Movie / Actor")

suggestions = []

if query:
    results = search_movie(query)

    for r in results[:5]:
        suggestions.append(r["title"])

selected = None

if suggestions:
    selected = st.selectbox("Suggestions", suggestions)

final_query = selected if selected else query


# -----------------------------
# SEARCH RESULT
# -----------------------------
if final_query:

    results = search_movie(final_query)

    if results:

        m = results[0]

        col1, col2 = st.columns([1,2])

        with col1:
            if m.get("poster_path"):
                st.image(IMG + m["poster_path"])

        with col2:
            st.title(m["title"])
            st.write("⭐ Rating:", m.get("vote_average"))
            st.write(m.get("overview"))

        # 🎥 TRAILER
        trailer = get_trailer(m["id"])

        if trailer:
            st.subheader("🎥 Trailer")
            st.video(trailer)

        # 📺 OTT
        st.subheader("📺 Watch On")

        providers = get_ott(m["id"])

        if providers:
            for p in providers:

                if "Netflix" in p:
                    st.link_button("Netflix", "https://www.netflix.com")

                elif "Amazon" in p:
                    st.link_button("Prime Video", "https://www.primevideo.com")

                elif "Hotstar" in p:
                    st.link_button("Hotstar", "https://www.hotstar.com")

                else:
                    st.write(p)
        else:
            st.write("No OTT data")

    else:
        st.error("Movie not found")

    # -----------------------------
    # ACTOR SEARCH
    # -----------------------------
    actor_results = search_actor(final_query)

    if actor_results:

        st.subheader("👨‍🎤 Actor Movies")

        movies = get_actor_movies(actor_results[0]["id"])

        cols = st.columns(5)

        for i, m in enumerate(movies[:5]):

            with cols[i]:

                if m.get("poster_path"):
                    st.image(IMG + m["poster_path"])

                st.caption(m.get("title"))


# -----------------------------
# HOMEPAGE
# -----------------------------
else:

    st.subheader("🔥 Trending Movies")

    movies = trending()

    cols = st.columns(5)

    for i, m in enumerate(movies[:5]):

        with cols[i]:

            if m.get("poster_path"):
                st.image(IMG + m["poster_path"])

            st.caption(m.get("title"))
