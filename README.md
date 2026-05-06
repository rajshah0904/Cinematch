# CineMatch: Movie Recommendation and Rating Analysis System

## Team Members
- Raj Shah | rshah10@stevens.edu | 20028030
- Jalen Thompson | jthomps8@stevens.edu | 20014187

## Project Description
**Problem.** Movie catalogs are huge and ratings are noisy, so browsing manually does not reliably surface titles a user might like.

**Approach.** CineMatch loads MovieLens CSVs into `Movie`, `User`, and `RecommendationSystem` objects; it ranks candidates using averages and genre preferences and visualizes distributions with pandas and matplotlib.

## Dependencies
- Python 3.12+ (course requirement: 3.12, 3.13, or 3.14)
- Third-party packages and minimum versions are listed in `requirements.txt` (pandas, matplotlib, ipykernel for the notebook, pytest for tests).

## File and Module Structure

- `cinematch/movie.py` — Defines the `Movie` class. Each movie stores its id, title, genre, year, director, and a list of ratings. Includes `add_rating`, `average_rating`, `__str__`, `__len__`, and `__eq__`.
- `cinematch/user.py` — Defines the `User` class. Each user has a watch history and preferred genres. Includes `add_to_history`, `set_preferred_genres`, and `get_genre_profile`.
- `cinematch/recommendation_system.py` — Defines the `RecommendationSystem` class, which composes `Movie` and `User` objects. Handles CSV loading, genre stats, top movie ranking, user recommendations, similarity scoring, and both matplotlib charts.
- `cinematch/utils.py` — Five standalone utility functions: `get_all_genres`, `generate_movie_report`, `random_movie_suggestion`, `genre_filter_generator` (a generator), and `calculate_popularity_scores`. Uses `map`, `filter`, `lambda`, `random`, and `yield`.
- `tests/test_cinematch.py` — Pytests for movie ratings/helpers, duplicate watch-history behavior, recommendation error handling, and top-movie ordering (prepends repo root on `sys.path` so imports resolve).
- `main.ipynb` — Jupyter notebook that runs the full system end-to-end: loads data, adds users, shows stats and charts, demonstrates recommendations and utility functions, and shows set operations on genre data.
- `requirements.txt` — Pinned minimum versions for pandas, matplotlib, ipykernel, and pytest.
- `data/movies.csv` — MovieLens movies file with movieId, title, and pipe-separated genres.
- `data/ratings.csv` — MovieLens ratings file with userId, movieId, rating, and timestamp.

## Data Source
Movie and rating data comes from the MovieLens Small Dataset provided by GroupLens Research at the University of Minnesota. It contains approximately 9,000 movies and 100,000 ratings from 600 users. The dataset is publicly available at https://grouplens.org/datasets/movielens/latest/ and is free for non-commercial use.

## How to Run

Run everything from the project root (the folder containing `cinematch/`, `data/`, and `main.ipynb`). Optional: `python3 -m venv .venv` then `source .venv/bin/activate` (macOS/Linux) before installing.

1. Install dependencies from `requirements.txt`:
   ```
   pip install -r requirements.txt
   ```

2. Make sure the data files are in the `data/` folder (they should already be there after cloning):
   ```
   data/movies.csv
   data/ratings.csv
   ```

3. Open and run the notebook:
   ```
   jupyter notebook main.ipynb
   ```
   Run cells from top to bottom in order. Note: loading ratings takes a moment since it processes ~100,000 rows.

4. To run the tests:
   ```
   python -m pytest tests/test_cinematch.py -v
   ```

## Main Contributions
- Raj Shah: `recommendation_system.py`, `movie.py`, `main.ipynb`, `test_cinematch.py`, data pipeline setup, README
- Jalen Thompson: `user.py`, `utils.py`, `test_cinematch.py`, `main.ipynb`, `recommendation_system.py`
