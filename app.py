import streamlit as st
import requests

# ---------------- CONFIG ----------------
API_KEY = "624e1be491b94af1717b2ac8e121b5f1"
IMG = "https://image.tmdb.org/t/p/w500"

st.set_page_config(page_title="Go Movie Discovery", layout="wide")

# ---------------- CSS ----------------
st.markdown("""
<style>
.poster:hover {
    transform: scale(1.1);
    transition: 0.3s;
}
</style>
""", unsafe_allow_html=True)

st.title("🎬 Go Movie Discovery Platform")

# ---------------- FUNCTIONS ----------------
def search_multi(query):
    url = f"https://api.themoviedb.org/3/search/multi?api_key={API_KEY}&query={query}"
    return requests.get(url).json().get("results", [])

def get_details(id, type="movie"):
    url = f"https://api.themoviedb.org/3/{type}/{id}?api_key={API_KEY}"
    return requests.get(url).json()

def get_trailer(id, type="movie"):
    url = f"https://api.themoviedb.org/3/{type}/{id}/videos?api_key={API_KEY}"
    data = requests.get(url).json()
    for v in data.get("results", []):
        if v["type"] == "Trailer":
            return "https://youtube.com/watch?v=" + v["key"]
    return None

def get_ott(id):
    url = f"https://api.themoviedb.org/3/movie/{id}/watch/providers?api_key={API_KEY}"
    data = requests.get(url).json()
    providers = []
    if "IN" in data.get("results", {}):
        for p in data["results"]["IN"].get("flatrate", []):
            providers.append(p["provider_name"])
    return providers

def trending():
    url = f"https://api.themoviedb.org/3/trending/all/week?api_key={API_KEY}"
    return requests.get(url).json().get("results", [])

# ---------------- SESSION ----------------
if "selected" not in st.session_state:
    st.session_state.selected = None

# ---------------- SEARCH ----------------
query = st.text_input("🔎 Search Movie / Series / Actor")

if query:
    results = search_multi(query)

    suggestions = [r.get("title") or r.get("name") for r in results[:5]]

    if suggestions:
        selected_name = st.selectbox("Suggestions", suggestions)
    else:
        selected_name = query

    # Find selected item
    selected_item = None
    for r in results:
        name = r.get("title") or r.get("name")
        if name == selected_name:
            selected_item = r
            break

    if selected_item:
        st.session_state.selected = selected_item

# ---------------- DETAIL PAGE ----------------
if st.session_state.selected:

    item = st.session_state.selected

    media = item["media_type"]
    id = item["id"]

    details = get_details(id, media)

    title = details.get("title") or details.get("name")

    st.header(title)

    col1, col2 = st.columns([1,2])

    with col1:
        if details.get("poster_path"):
            st.image(IMG + details["poster_path"])

    with col2:
        st.write("⭐ Rating:", details.get("vote_average"))
        st.write(details.get("overview"))

    # Trailer
    t = get_trailer(id, media)

    if t:
        st.subheader("🎥 Trailer")
        st.video(t)

    # OTT only for movies
    if media == "movie":
        st.subheader("📺 Watch On")

        providers = get_ott(id)

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

    if st.button("⬅ Back"):
        st.session_state.selected = None

# ---------------- HOMEPAGE ----------------
else:

    st.subheader("🔥 Trending")

    movies = trending()

    cols = st.columns(5)

    for i, m in enumerate(movies[:10]):

        with cols[i % 5]:

            title = m.get("title") or m.get("name")

            if m.get("poster_path"):
                st.image(IMG + m["poster_path"])

            if st.button(title, key=i):
                st.session_state.selected = m
