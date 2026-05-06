import random
import math

def get_all_genres(movies_dict):
    """Return a set of every unique genre found across all movies."""
    genres = set()
    for movie in movies_dict.values():
        genres.add(movie.genre)
    return genres


def generate_movie_report(movies_list):
    """Build and return a list of dicts summarizing each movie in the list."""
    # try to get the average rating, fall back to N/A if there are no ratings
    def safe_avg(movie):
        """Return average rating or the string 'N/A' if the movie has no ratings."""
        try:
            return movie.average_rating()
        except RuntimeError:
            return "N/A"

    report = [
        {
            'title': movie.title,
            'genre': movie.genre,
            'year': movie.year,
            'avg_rating': safe_avg(movie)
        }
        for movie in movies_list
    ]
    return report


def random_movie_suggestion(movies_dict):
    """Return one random movie that has at least one rating."""
    # filter down to movies that have been rated
    rated = list(filter(lambda m: len(m.ratings) > 0, movies_dict.values()))

    if len(rated) == 0:
        raise RuntimeError("No movies have ratings yet")

    return random.choice(rated)


def genre_filter_generator(movies_dict, genre):
    """Yield Movie objects one at a time that match the given genre."""
    for movie in movies_dict.values():
        if movie.genre == genre:
            yield movie


def calculate_popularity_scores(movies_dict):
    """Return a list of (title, score) tuples sorted by popularity, highest first."""
    # only score movies that have been rated
    rated_movies = list(filter(lambda m: len(m.ratings) > 0, movies_dict.values()))

    # score = avg_rating * number_of_ratings / 10, capped at 5.0
    def compute_score(movie):
        """Return (movie title, popularity score capped at 5.0)."""
        raw_score = movie.average_rating() * len(movie.ratings) / 10.0
        return (movie.title, min(raw_score, 5.0))

    scores = list(map(compute_score, rated_movies))

    # sort by score descending
    scores.sort(key=lambda t: t[1], reverse=True)

    return scores


if __name__ == "__main__":
    print("utils.py loaded directly")
