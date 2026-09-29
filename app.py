from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DATA_PATH = Path(__file__).parent / "data" / "movie_ratings.csv"
NO_GENRE_LABELS = {"(no genres listed)", "unknown", ""}


@st.cache_data
def load_ratings() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


def explode_genres(df: pd.DataFrame) -> pd.DataFrame:
    """One row per genre tag. Drop empty / unknown / (no genres listed)."""
    exploded = df.assign(genre=df["genres"].fillna("").str.split("|")).explode("genre")
    exploded["genre"] = exploded["genre"].str.strip()
    return exploded[~exploded["genre"].str.lower().isin(NO_GENRE_LABELS)].copy()


def unique_movie_genre_counts(ratings: pd.DataFrame) -> pd.DataFrame:
    """Count each unique movie once per listed genre.

    A movie tagged Action|Comedy adds 1 to Action and 1 to Comedy.
    Rows with no usable genre are dropped before counting.
    """
    movies = ratings.drop_duplicates(subset="movie_id")[["movie_id", "title", "genres"]]
    exploded = explode_genres(movies)
    return (
        exploded.groupby("genre", as_index=False)
        .agg(movie_count=("movie_id", "nunique"))
        .sort_values("movie_count", ascending=False)
    )


def genre_average_ratings(ratings: pd.DataFrame) -> pd.DataFrame:
    """Mean of every rating assigned to a genre (multi-label explode).

    A rating of an Action|Comedy movie is included in both genre averages.
    Sorted lowest average on the left to highest on the right.
    """
    exploded = explode_genres(ratings)
    return (
        exploded.groupby("genre", as_index=False)
        .agg(avg_rating=("rating", "mean"), n_ratings=("rating", "size"))
        .sort_values("avg_rating", ascending=True)
    )


def mean_rating_by_release_year(ratings: pd.DataFrame) -> pd.DataFrame:
    """Mean rating grouped by movie release year (`year`), not review time.

    Drops rows with a missing release year. Uses every rating of movies
    released in that year (same rating-level mean as Question 2).
    """
    yearly = ratings.dropna(subset=["year"]).copy()
    yearly["release_year"] = yearly["year"].astype(int)
    return (
        yearly.groupby("release_year", as_index=False)
        .agg(avg_rating=("rating", "mean"), n_ratings=("rating", "size"))
        .sort_values("release_year")
    )


RATING_FLOORS = (50, 150, 250)


def movie_rating_stats(ratings: pd.DataFrame) -> pd.DataFrame:
    """One row per movie: mean rating and how many ratings it received."""
    stats = ratings.groupby("movie_id", as_index=False).agg(
        title=("title", "first"),
        year=("year", "first"),
        avg_rating=("rating", "mean"),
        n_ratings=("rating", "size"),
    )
    stats["label"] = stats.apply(
        lambda row: (
            f"{row['title']} ({int(row['year'])})"
            if pd.notna(row["year"])
            else str(row["title"])
        ),
        axis=1,
    )
    return stats


def top_movies_at_floor(stats: pd.DataFrame, min_ratings: int, n: int = 5) -> pd.DataFrame:
    """Top n movies by mean rating among those with at least min_ratings ratings."""
    eligible = stats[stats["n_ratings"] >= min_ratings]
    return eligible.sort_values(
        ["avg_rating", "n_ratings"], ascending=[False, False]
    ).head(n)


st.set_page_config(page_title="MovieLens Dashboard", layout="wide")
st.title("MovieLens Dashboard")

ratings = load_ratings()
genre_counts = unique_movie_genre_counts(ratings)
genre_avgs = genre_average_ratings(ratings)
yearly_avgs = mean_rating_by_release_year(ratings)
movie_stats = movie_rating_stats(ratings)

st.header("Question 1: Genre breakdown")
st.markdown(
    """
    **How multiple genres are counted:** each unique movie is counted once
    for *every* genre listed on it. Pipe-separated tags such as
    `Action|Comedy` add 1 to Action and 1 to Comedy. Movies with no genre
    (`unknown` / empty / `(no genres listed)`) are excluded. Bar totals
    therefore sum to more than the number of unique movies.
    """
)

fig = px.bar(
    genre_counts,
    x="movie_count",
    y="genre",
    orientation="h",
    labels={"movie_count": "Unique movies", "genre": "Genre"},
    title="Unique rated movies per genre (multi-label counts)",
)
fig.update_layout(
    yaxis={"categoryorder": "array", "categoryarray": genre_counts["genre"].iloc[::-1]},
    margin=dict(l=10, r=10, t=50, b=10),
)
st.plotly_chart(fig, use_container_width=True)

n_unique = ratings["movie_id"].nunique()
n_counted = genre_counts["movie_count"].sum()
st.caption(
    f"{n_unique:,} unique rated movies. "
    f"Genre assignments after dropping missing genres: {n_counted:,}."
)

st.header("Question 2: Genre satisfaction")
st.markdown(
    """
    **How the average is computed:** every rating row is split across that
    movie’s genres (same multi-label rule as Question 1). A 4-star rating
    of an `Action|Comedy` film counts toward **both** Action and Comedy.
    Missing genres are dropped. The mean is the average of those rating
    values, so frequently rated movies influence a genre more than rarely
    rated ones.
    """
)

fig_avg = px.bar(
    genre_avgs,
    x="genre",
    y="avg_rating",
    labels={"avg_rating": "Average rating", "genre": "Genre"},
    title="Average rating by genre (lowest → highest)",
    hover_data={"n_ratings": True, "avg_rating": ":.3f"},
)
fig_avg.update_layout(
    xaxis={"categoryorder": "array", "categoryarray": genre_avgs["genre"].tolist()},
    yaxis={"range": [0, 5]},
    margin=dict(l=10, r=10, t=50, b=10),
)
st.plotly_chart(fig_avg, use_container_width=True)

lowest = genre_avgs.iloc[0]
highest = genre_avgs.iloc[-1]
st.caption(
    f"Lowest: {lowest['genre']} ({lowest['avg_rating']:.3f}). "
    f"Highest: {highest['genre']} ({highest['avg_rating']:.3f})."
)

st.header("Question 3: Ratings over time")
st.markdown(
    """
    **Release year, not review date:** the x-axis is the movie’s **release
    year** (`year` in the CSV), not `timestamp` / `rating_year` (when the
    user rated it). Each point is the mean of all ratings for movies
    released that year. Rows with a missing release year are dropped.
    """
)

fig_year = px.line(
    yearly_avgs,
    x="release_year",
    y="avg_rating",
    markers=True,
    labels={
        "release_year": "Movie release year",
        "avg_rating": "Average rating",
    },
    title="Mean rating by movie release year",
    hover_data={"n_ratings": True, "avg_rating": ":.3f"},
)
fig_year.update_layout(
    yaxis={"range": [0, 5]},
    margin=dict(l=10, r=10, t=50, b=10),
)
st.plotly_chart(fig_year, use_container_width=True)

n_missing_year = int(ratings["year"].isna().sum())
st.caption(
    f"Grouped by release year {int(yearly_avgs['release_year'].min())}–"
    f"{int(yearly_avgs['release_year'].max())}. "
    f"Dropped {n_missing_year:,} rating rows with no release year."
)

st.header("Question 4: Best movies, with a floor")
st.markdown(
    """
    **How the floor works:** a movie’s score is the mean of its ratings.
    It only enters the ranking if it has **at least** that many ratings,
    so one-off 5-star films cannot dominate. Rankings start at a floor of
    50, then 150, then 250 (step of 100). Ties break toward more ratings.
    """
)

for min_ratings in RATING_FLOORS:
    top5 = top_movies_at_floor(movie_stats, min_ratings)
    n_eligible = int((movie_stats["n_ratings"] >= min_ratings).sum())
    st.subheader(f"Top 5 with at least {min_ratings} ratings")
    if top5.empty:
        st.warning(f"No movies have {min_ratings}+ ratings.")
        continue
    fig_top = px.bar(
        top5,
        x="avg_rating",
        y="label",
        orientation="h",
        labels={"avg_rating": "Average rating", "label": "Movie"},
        title=f"Top 5 movies (≥ {min_ratings} ratings)",
        hover_data={"n_ratings": True, "avg_rating": ":.3f"},
    )
    fig_top.update_layout(
        yaxis={
            "categoryorder": "array",
            "categoryarray": top5["label"].iloc[::-1],
        },
        xaxis={
            "range": [3, 5],
            "dtick": 0.1,
            "tickformat": ".1f",
            "tick0": 3,
        },
        margin=dict(l=10, r=10, t=50, b=10),
    )
    st.plotly_chart(fig_top, use_container_width=True)
    st.caption(f"{n_eligible:,} movies meet the {min_ratings}+ rating floor.")
