"""Pytest tests for CineMatch core logic (ratings, users, recommendations)."""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from cinematch.movie import Movie
from cinematch.user import User
from cinematch.recommendation_system import RecommendationSystem


def test_movie_average_rating():
    """Average of 3.0, 4.0, 5.0 should come out to 4.0."""
    movie = Movie(1, "Test Movie", "Action", 2020, "Director")
    movie.add_rating(3.0)
    movie.add_rating(4.0)
    movie.add_rating(5.0)
    assert movie.average_rating() == 4.0


def test_movie_no_ratings_raises():
    """Calling average_rating on a movie with no ratings should raise RuntimeError."""
    movie = Movie(2, "Empty Movie", "Drama", 2019, "Director")
    with pytest.raises(RuntimeError):
        movie.average_rating()


def test_invalid_rating_raises():
    """Ratings outside the 1.0 to 5.0 range should raise ValueError."""
    movie = Movie(3, "Rating Test", "Comedy", 2021, "Director")
    with pytest.raises(ValueError):
        movie.add_rating(6.0)
    with pytest.raises(ValueError):
        movie.add_rating(0.5)


def test_movie_len():
    """len(movie) should equal the number of ratings that were added."""
    movie = Movie(4, "Length Test", "Horror", 2018, "Director")
    movie.add_rating(3.0)
    movie.add_rating(4.5)
    movie.add_rating(2.0)
    assert len(movie) == 3


def test_movie_eq():
    """Two movies with the same movie_id should be considered equal."""
    movie_a = Movie(5, "First Title", "Action", 2015, "Director A")
    movie_b = Movie(5, "Different Title", "Drama", 2020, "Director B")
    assert movie_a == movie_b


def test_user_watch_history():
    """Adding the same movie_id twice should only store it once."""
    user = User(1, "Alice")
    user.add_to_history(1)
    user.add_to_history(1)
    assert len(user.watch_history) == 1


def test_recommend_for_user_unknown_user_raises_keyerror():
    """recommend_for_user should raise KeyError when the user_id is not registered."""
    system = RecommendationSystem()
    with pytest.raises(KeyError, match="User 404 not found"):
        system.recommend_for_user(404)


def test_get_top_movies_orders_by_average_rating_descending():
    """get_top_movies should return the highest-rated movies first (among rated movies)."""
    system = RecommendationSystem()
    low = Movie(1, "Low", "Action", 2020, "X")
    low.add_rating(2.0)
    high = Movie(2, "High", "Drama", 2020, "Y")
    high.add_rating(5.0)
    mid = Movie(3, "Mid", "Comedy", 2020, "Z")
    mid.add_rating(4.0)
    system.movies = {1: low, 2: high, 3: mid}
    top = system.get_top_movies(n=2)
    assert [m.movie_id for m in top] == [2, 3]