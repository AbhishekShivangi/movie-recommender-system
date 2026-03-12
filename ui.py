import streamlit as st

def hero_banner():

    st.markdown(
    """
    <div class='hero-banner'>
        <h1 style='color:red'>🎬 Go Movie Discovery</h1>
        <h3 style='color:white'>
        Discover movies, series, anime and actors
        </h3>
    </div>
    """,
    unsafe_allow_html=True
    )

def trailer_preview(url):

    if url:

        html=f"""
        <iframe width="100%" height="400"
        src="{url}?autoplay=1&mute=1"
        frameborder="0"
        allow="autoplay">
        </iframe>
        """

        st.markdown(html,unsafe_allow_html=True)
