import streamlit as st
import plotly.express as px

st.title("Global Development Explorer")
st.write("Life expectancy and income for 142 countries, 1952–2007.")

df = px.data.gapminder()
st.dataframe(df)
