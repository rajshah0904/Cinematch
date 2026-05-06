import pandas as pd
import matplotlib.pyplot as plt
from cinematch.movie import Movie
from cinematch.user import User


class RecommendationSystem:
    """
    Main system for loading movies, managing users, and generating recommendations.

    This class uses composition — it contains Movie objects stored in self.movies
    and User objects stored in self.users. It does not inherit from any other class.
    """

    def __init__(self):
        """Set up empty dicts for movies and users, plus a placeholder for ratings data."""
        # movie_id -> Movie object
        self.movies = {}
        # user_id -> User object
        self.users = {}
        # filled in when load_ratings is called
        self.ratings_df = None

    def load_movies(self, filepath):
        """Load movies from a CSV and create a Movie object for each row."""
        try:
            df = pd.read_csv(filepath)
        except FileNotFoundError:
            raise FileNotFoundError(f"Movie file not found: {filepath}")

        # make sure the columns we need are present
        required_cols = ['movieId', 'title', 'genres']
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Missing required column in movies file: {col}")

        for _, row in df.iterrows():
            movie_id = int(row['movieId'])
            raw_title = str(row['title'])
            genres_str = str(row['genres'])

            # take just the first genre
            if genres_str == '(no genres listed)':
                genre = 'Unknown'
            else:
                genre = genres_str.split('|')[0]

            # pull the year out of titles like "Toy Story (1995)"
            year = 0
            clean_title = raw_title
            if '(' in raw_title and raw_title.strip().endswith(')'):
                try:
                    year_str = raw_title[raw_title.rfind('(') + 1:raw_title.rfind(')')]
                    year = int(year_str)
                    clean_title = raw_title[:raw_title.rfind('(')].strip()
                except ValueError:
                    # title has parentheses but no valid year inside
                    year = 0

            # MovieLens doesn't include directors, so use a placeholder
            director = "Unknown"

            movie = Movie(movie_id, clean_title, genre, year, director)
            self.movies[movie_id] = movie

    def load_ratings(self, filepath):
        """Load ratings from a CSV and attach each rating to the right Movie object."""
        try:
            self.ratings_df = pd.read_csv(filepath)
        except FileNotFoundError:
            raise FileNotFoundError(f"Ratings file not found: {filepath}")

        # check the columns we actually need are there
        required_cols = ['userId', 'movieId', 'rating']
        for col in required_cols:
            if col not in self.ratings_df.columns:
                raise ValueError(f"Missing required column in ratings file: {col}")

        # go row by row and add each rating to the matching movie
        for _, row in self.ratings_df.iterrows():
            movie_id = int(row['movieId'])
            rating = float(row['rating'])

            # skip ratings for movies we don't have loaded
            if movie_id not in self.movies:
                continue

            try:
                self.movies[movie_id].add_rating(rating)
            except ValueError:
                # skip ratings outside the 1.0–5.0 range (e.g. 0.5 in MovieLens)
                continue

    def add_user(self, user_id, name):
        """Create a User object and store it in self.users."""
        self.users[user_id] = User(user_id, name)

    def compute_genre_stats(self):
        """Return a dict mapping genre to its average rating across all movies in that genre."""
        # collect all per-movie averages grouped by genre
        genre_ratings = {}

        for movie in self.movies.values():
            # skip movies with no ratings
            if len(movie.ratings) == 0:
                continue

            if movie.genre not in genre_ratings:
                genre_ratings[movie.genre] = []

            genre_ratings[movie.genre].append(movie.average_rating())

        # average the collected ratings per genre
        genre_stats = {}
        for genre, ratings in genre_ratings.items():
            genre_stats[genre] = round(sum(ratings) / len(ratings), 2)

        return genre_stats

    def get_top_movies(self, n=10):
        """Return the top n Movie objects sorted by average rating, highest first."""
        # filter out movies with no ratings
        rated_movies = [m for m in self.movies.values() if len(m.ratings) > 0]

        # sort by rating descending
        sorted_movies = sorted(rated_movies, key=lambda m: m.average_rating(), reverse=True)

        return sorted_movies[:n]

    def recommend_for_user(self, user_id, n=5):
        """Return up to n recommended movies for the given user."""
        if user_id not in self.users:
            raise KeyError(f"User {user_id} not found")

        user = self.users[user_id]

        # skip movies the user already watched, and movies with no ratings
        candidates = [
            m for m in self.movies.values()
            if m.movie_id not in user.watch_history and len(m.ratings) > 0
        ]

        if user.preferred_genres:
            # put preferred-genre movies first, then everything else
            preferred = [m for m in candidates if m.genre in user.preferred_genres]
            others = [m for m in candidates if m.genre not in user.preferred_genres]

            # sort each group by rating, best first
            preferred = sorted(preferred, key=lambda m: m.average_rating(), reverse=True)
            others = sorted(others, key=lambda m: m.average_rating(), reverse=True)

            candidates = preferred + others
        else:
            # no preferences, just sort by rating
            candidates = sorted(candidates, key=lambda m: m.average_rating(), reverse=True)

        return candidates[:n]

    def similarity_score(self, movie_a, movie_b):
        """Return a similarity score between 0.0 and 1.0 comparing two movies."""
        # need ratings on both sides to do the comparison
        if len(movie_a.ratings) == 0 or len(movie_b.ratings) == 0:
            raise RuntimeError("Both movies need at least one rating to compare")

        score = 0.0

        # same genre gives half the score
        if movie_a.genre == movie_b.genre:
            score += 0.5

        # closer average ratings gives the other half
        avg_a = movie_a.average_rating()
        avg_b = movie_b.average_rating()
        rating_sim = 0.5 * (1 - abs(avg_a - avg_b) / 4.0)
        score += rating_sim

        return round(score, 4)

    def plot_genre_ratings(self):
        """Make a bar chart of average rating by genre, save it, and display it."""
        # build a small dataframe so we can use pandas groupby + mean
        rows = []
        for movie in self.movies.values():
            if len(movie.ratings) > 0:
                rows.append({'genre': movie.genre, 'avg_rating': movie.average_rating()})

        genre_df = pd.DataFrame(rows)

        # pandas groupby + mean to get one average per genre
        genre_means = genre_df.groupby('genre')['avg_rating'].mean().sort_values()

        genres = genre_means.index.tolist()
        avg_ratings = genre_means.values.tolist()

        plt.figure(figsize=(12, 6))
        plt.bar(genres, avg_ratings)
        plt.title("Average Rating by Genre")
        plt.xlabel("Genre")
        plt.ylabel("Average Rating")
        plt.ylim(0, 5)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig("genre_ratings.png")
        plt.show()

    def plot_rating_distribution(self):
        """Make a histogram of all ratings and save it."""
        plt.figure(figsize=(8, 5))
        plt.hist(self.ratings_df['rating'], bins=10)
        plt.title("Distribution of All Ratings")
        plt.xlabel("Rating")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.savefig("rating_distribution.png")
        plt.show()

    def __str__(self):
        """Return a summary showing how many movies and users are loaded."""
        return f"RecommendationSystem | Movies: {len(self.movies)} | Users: {len(self.users)}"

    def __len__(self):
        """Return the number of movies in the system."""
        return len(self.movies)
