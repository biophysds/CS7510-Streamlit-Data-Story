import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Global Development Explorer", layout="wide")

@st.cache_data
def load_data():
    return px.data.gapminder()

df = load_data()

st.title("Asia gained 24 years of life expectancy since 1952")

story, explore = st.tabs(["The story", "Explore it yourself"])

with story:
    by_continent = df.groupby(
        ["continent", "year"], as_index=False
    )["lifeExp"].mean()

    fig = px.line(
        by_continent,
        x="year",
        y="lifeExp",
        color="continent",
        labels={
            "lifeExp": "Average life expectancy (years)",
            "year": ""
        }
    )

    st.plotly_chart(fig)

    st.markdown(
        "Every continent improved, but **Asia** rose fastest: "
        "from **46.3** years in 1952 to **70.7** in 2007."
    )

    st.caption(
        "Source: Gapminder, via plotly.express. "
        "Unweighted country averages."
    )

with explore:
    left, right = st.columns([1, 3])

    continent = left.selectbox(
        "Continent",
        ["All"] + sorted(df["continent"].unique())
    )

    year = left.slider("Year", 1952, 2007, 2007, step=5)

    filtered = df[df["year"] == year]

    if continent != "All":
        filtered = filtered[filtered["continent"] == continent]

    place = "the world" if continent == "All" else continent

    left.metric(
        "Avg life expectancy",
        f"{filtered['lifeExp'].mean():.1f} yrs"
    )

    right.markdown(
        f"In **{year}**, the **{len(filtered)}** countries "
        f"in **{place}** had an average life expectancy "
        f"of **{filtered['lifeExp'].mean():.1f} years**."
    )

    fig = px.scatter(
        filtered,
        x="gdpPercap",
        y="lifeExp",
        hover_name="country",
        color="continent",
        size="pop",
        log_x=True,
        size_max=50,
        range_y=[25, 90]
    )

    right.plotly_chart(fig)
    
    with st.expander("See the data behind this chart"):
        st.dataframe(filtered, hide_index=True)

        st.download_button(
            "Download as CSV",
            data=filtered.to_csv(index=False),
            file_name=f"gapminder_{place}_{year}.csv",
            mime="text/csv"
        )
