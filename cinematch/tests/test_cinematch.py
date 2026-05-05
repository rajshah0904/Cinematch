import pytest
import sys
import os

# add the parent directory so we can import movie and user
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from movie import Movie
from user import User


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
