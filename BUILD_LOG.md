# Week 4 Vibe Coding — Build Log

Scratch notes for next week's review. Not a polished write-up.

---

## Question 1 — Genre breakdown

**Prompt given (paraphrased / actual):**
> Make a chart of the distribution of genres among movies that were rated from `movie_ratings.csv`. Plenty of movies have multiple genres. Explain how the chart handles multiple genres *before* counting. Return a bar chart sorted by count. Count the movie once for each of its genres.

**Clarifications before coding:**
- Count **unique movies**, then add 1 to each of that movie’s genres.
- Discard movies/tokens with no genre listed.
- Put the app in `Week-04-Vibe-Coding-101/app.py`.
- CSV lives in `data/movie_ratings.csv`.

**What the AI produced on the first try:**
- Streamlit app with a horizontal bar chart (Plotly), sorted by unique-movie count.
- Split `genres` on `|`, explode, drop `unknown` / empty / `(no genres listed)`.
- On-page explanation of the multi-label counting rule.
- `requirements.txt`: streamlit, pandas, plotly.
- This build log.

**What we changed and why:**
- (none yet — first working Q1)

**Method locked in:**
- Unit: unique `movie_id`.
- Multi-genre: one count per listed genre.
- Missing genre: discarded (`unknown` in this MovieLens file is 2 movies).

---

## Question 2 — Genre satisfaction

**Prompt given:**
> Using `movie_ratings.csv`, make a bar chart of which genres have the highest average rating, from lowest on the left to highest on the right. Put this chart underneath the previous one.

**What the AI produced on the first try:**
- Second Plotly bar chart in `app.py` under Q1.
- Same `|` explode + drop missing genres.
- Average = mean of **all rating rows** per genre (not unique-movie means). A multi-genre rating counts in every listed genre.
- Vertical bars sorted ascending (lowest left, highest right). Y-axis 0–5.

**What we changed and why:**
- (none yet — first working Q2)

**Method chosen (not confirmed by user):**
- Rating-level mean, so popular films weigh more. Alternative not used: average each movie first, then average those movie means per genre.

---

## Question 3 — Ratings over time

**Prompt given:**
> Show how the mean rating has changed across movie release years using a line chart. Match the year of the movie with when it was released, not when a review was placed. Place this chart directly under the previous one.

**What the AI produced on the first try:**
- Plotly line chart under Q2.
- X-axis = `year` (release), **not** `rating_year` / `timestamp`.
- Mean of all ratings for movies released that year; missing `year` dropped.
- Markers on the line; y-axis 0–5; hover shows rating count.

**What we changed and why:**
- (none yet — first working Q3)

---

## Question 4 — Best movies, with a floor

**Prompt given:**
> Show the top 5 best-rated movies using a bar chart. Show with at least 50 ratings, then make different bar charts increasing the required minimum by 100 each time until a minimum of 250 ratings.

**What the AI produced on the first try:**
- Three horizontal bar charts under Q3: floors **50, 150, 250**.
- Rank by mean rating; eligible only if `n_ratings >= floor`.
- Tie-break: more ratings first.
- Labels include title and release year.

**What we changed and why:**
- Q4 x-axis zoomed to **3.0–5.0** with **0.1** ticks (3.0, 3.1, … 5.0) so the 4-star+ bars are readable. First version used 0–5 with no decimal ticks.
