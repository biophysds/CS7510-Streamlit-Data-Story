# I choose Client A, or Health NGO board task for the following data app
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Global Health Explorer", layout="wide")

@st.cache_data
def load_data():
    return px.data.gapminder()

df = load_data()

by_continent = df.groupby(
    ["continent", "year"], as_index=False
)["lifeExp"].mean()

first_year = int(df["year"].min())
latest_year = int(df["year"].max())

latest = by_continent[
    by_continent["year"] == latest_year
].sort_values("lifeExp")

lowest = latest.iloc[0]
priority = lowest["continent"]
latest_life = lowest["lifeExp"]

first_life = by_continent.loc[
    (by_continent["continent"] == priority) &
    (by_continent["year"] == first_year),
    "lifeExp"
].iloc[0]

gain = latest_life - first_life

st.title(
    f"{priority} had the lowest average life expectancy "
    f"in {latest_year}: {latest_life:.1f} years"
)

story, explore = st.tabs(["The story", "Explore it yourself"])

with story:
    fig = px.line(
        by_continent,
        x="year",
        y="lifeExp",
        color="continent",
        labels={
            "lifeExp": "Average life expectancy (years)",
            "year": "Year",
            "continent": "Continent"
        }
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        f"Average life expectancy in **{priority}** increased "
        f"from **{first_life:.1f} years** in {first_year} "
        f"to **{latest_life:.1f} years** in {latest_year}, "
        f"an improvement of **{gain:.1f} years**."
    )

    st.markdown(
        f"Despite this improvement, **{priority}** still had "
        "the lowest average life expectancy among the continents. "
        "This makes it a reasonable priority for further investigation "
        "and potential health funding."
    )

    st.caption(
        "Source: Gapminder (1952–2007), via Plotly Express. "
        "Continent averages are not weighted by population."
    )

with explore:
    left, right = st.columns([1, 3])

    continent = left.selectbox(
        "Continent",
        ["All"] + sorted(df["continent"].unique())
    )

    year = left.slider(
        "Year",
        first_year,
        latest_year,
        latest_year,
        step=5
    )

    filtered = df[df["year"] == year]

    if continent != "All":
        filtered = filtered[
            filtered["continent"] == continent
        ]

    place = "the world" if continent == "All" else continent

    avg_life = filtered["lifeExp"].mean()
    median_gdp = filtered["gdpPercap"].median()
    country_count = len(filtered)

    left.metric(
        "Countries",
        country_count
    )

    left.metric(
        "Avg life expectancy",
        f"{avg_life:.1f} yrs"
    )

    left.metric(
        "Median GDP per capita",
        f"${median_gdp:,.0f}"
    )

    right.markdown(
        f"In **{year}**, the **{country_count}** countries "
        f"in **{place}** had an average life expectancy "
        f"of **{avg_life:.1f} years** and a median GDP "
        f"per capita of **${median_gdp:,.0f}**."
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
        range_y=[25, 90],
        labels={
            "gdpPercap": "GDP per capita",
            "lifeExp": "Life expectancy (years)",
            "pop": "Population",
            "continent": "Continent"
        }
    )

    right.plotly_chart(fig, use_container_width=True)

    with st.expander("See the data behind this chart"):
        st.dataframe(filtered, hide_index=True)

        st.download_button(
            "Download as CSV",
            data=filtered.to_csv(index=False),
            file_name=f"gapminder_{continent}_{year}.csv",
            mime="text/csv"
        )
