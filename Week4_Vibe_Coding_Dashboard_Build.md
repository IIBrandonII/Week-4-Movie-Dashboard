# Homework: Driving "Vibe Coding" — Build the MovieLens Dashboard

> *"You have to be the driver. AI is sitting shotgun. They can give you directions, but you're ultimately the person behind the wheel."🫵*

---

## 1. Core Philosophy: The Engineer in the Driver's Seat 🚗

**Vibe coding is a tool, not an autopilot.** Using natural language prompts with models like Cursor, Claude, or ChatGPT lets you generate boilerplate and visual code quickly, but production-grade data science demands that **you** make the architectural and statistical choices.

AI does not understand your analytical intent, the nuances of the data, or the difference between a pretty chart and an accurate one. If you blindly accept whatever the AI suggests, the model is driving and you are just a passenger.

This week, you're getting an early, AI-scaffolded preview of dashboard building — before you've been formally taught the chart-craft and Streamlit mechanics behind it. That's intentional. You'll learn the "right" way to do this next week in the EDA + Dashboards lecture, and then you'll come back and judge your own work here against that standard. So build boldly, but **keep a record of how you got here** — you'll need it.

Your deliverable this week is a live, publicly accessible dashboard URL.

---

## 2. Dataset: MovieLens 🎥

You will use the GroupLens **MovieLens** dataset:
* `movie_ratings.csv` — contains `userId`, `movieId`, `rating`, `timestamp`, `title`, `year`, and pipe-separated `genres`).

---

## 3. Assignment Tasks 📑

### Task 1: The 4 Required Visualizations

Direct your AI assistant to answer each of these four questions with a chart. These are the same four questions you'll revisit by hand next week, so answer them as they're written — don't substitute your own.

**Question 1 — Genre Breakdown:** What's the distribution of genres among the movies that were rated? (Movies can have multiple genres — have the AI explain how it handled that before it counts anything.)

**Question 2 — Genre Satisfaction:** Which genres have the highest average rating? Which have the lowest?

**Question 3 — Ratings Over Time:** How has the mean rating changed across movie release years?

**Question 4 — Best Movies, With a Floor:** What are the top 5 best-rated movies, once you only count movies with at least 50 ratings? What changes if you raise that floor to 150?

> ⚠️ **A Note on "Ambiguity" by Design:**  
> If some of these questions feel slightly open to interpretation (e.g., how to compute a "mean rating," how to define a "floor," or it spawns up further questions like how to handle noisy outliers), **that is intentional.** Just look stuff up! Disambiguate the questions on your own. 

You choose — or let the AI choose and then judge — what chart type answers each question best. That's on purpose: you don't know chart-craft formally yet, so this is where you'll see the AI make a default choice, good or bad, and you'll be asked to evaluate it next week once you do know better.

#### Chart Toolkit — a reference while you prompt

You haven't been taught these formally yet, so lean on the AI to execute — but this table will help you recognize whether what it gives you actually fits the question:

| Chart type | Best for | Watch out for |
|---|---|---|
| **Bar chart** | Comparing counts or averages across categories | Ask for it sorted — don't accept default/alphabetical order |
| **Horizontal bar chart** | Same, but with long labels or many categories | Still needs sorting; watch for too many bars to read at a glance |
| **Pie chart** | Parts of a whole, only with a handful of categories | AI *loves* defaulting to pie charts for things like "genre breakdown" with 18 slices — notice if it does this |
| **Line / time series chart** | Trends over time | Notice if the AI confuses "year released" with "year rated" |
| **Scatter plot** | Relationship between two continuous variables | With thousands of points, ask for transparency/aggregation to avoid overplotting |
| **Heatmap** | Two categorical dimensions against a value | Needs a legend/color scale to be readable |

### Task 2: Deploy on Streamlit 🚀

### Deployment Prerequisite: Connect to GitHub First ⚠️

Streamlit Community Cloud builds directly from a public GitHub repository. It does not deploy local files from your computer. Follow these steps before deploying on Streamlit:

1. **Initialize & Commit Locally:**
   Initialize git in your project root, add your files like (`app.py`, `requirements.txt`, etc.), and make a commit.
2. **Push to a Remote GitHub Repository:**
   Create a new **Public** repository on GitHub, link it as your remote origin, and push your `main` branch.
   
Build and deploy your dashboard using **Streamlit**, on **Streamlit Community Cloud** (free hosting). No framework decision to make here — Streamlit is what the rest of the course uses, so that's the path.

Select your GitHub repository and `main` branch, point the main file path to `app.py`, and click **Deploy**.

### Task 3: Keep a Build Log (this is the part you'll thank yourself for later)

As you go, save 2–3 moments that capture your actual process — not a polished writeup, just the raw material:
* The prompt you gave
* What the AI produced on the first try
* What you changed and why (or didn't)

Paste these into a scratch doc, a comment in your code, wherever — just don't lose them. **You cannot accurately reconstruct a real prompt log from memory a week later**, and next week's report depends on having the real thing.

---

## 4. Required Dashboard Structure 🏛️

Your deployed web application must include:

1. **Interactive Controls:** At least 1–2 working input widgets (e.g., genre multi-select, threshold sliders, year/date ranges).
2. **Data Visualizations:** All 4 required charts from Task 1, answering the 4 questions above.

No embedded write-up or audit section needed in the app itself — that's next week's deliverable, and it lives in a notebook, not the dashboard.

---

## 5. Submission 🏁

* **Submission Format:** Submit the public link to your deployed app (e.g., `https://<your-username>.streamlit.app`). No code upload required for this week.
* **Pre-Flight Check:** Test your link in an **Incognito / Private window** before submitting to confirm it runs publicly without authentication errors or dependency crashes.
* **Don't lose your build log** — you might use it next week.