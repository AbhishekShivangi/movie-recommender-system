import plotly.express as px
import pandas as pd
import streamlit as st

def popularity_chart(movies):

    data=[]

    for m in movies[:10]:

        data.append({
            "title":m.get("title") or m.get("name"),
            "popularity":m["popularity"]
        })

    df=pd.DataFrame(data)

    fig=px.bar(df,x="title",y="popularity")

    st.plotly_chart(fig)
