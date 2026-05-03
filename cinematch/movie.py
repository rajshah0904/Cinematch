class Movie:
    """Stores info about one movie and its ratings."""

    def __init__(self, movie_id, title, genre, year, director):
        """Create a movie record from identifiers and metadata.

        Stores movie_id, title, genre, year, and director as attributes.
        Ratings start empty; use add_rating to record scores in 1.0–5.0.
        """
        self.movie_id = movie_id
        self.title = title
        self.genre = genre
        self.year = year
        self.director = director
        # start with no ratings
        self.ratings = []

    def add_rating(self, rating):
        """Add a rating to this movie. Raises ValueError if not between 1.0 and 5.0."""
        # reject anything outside the valid range
        if rating < 1.0 or rating > 5.0:
            raise ValueError(f"Rating must be between 1.0 and 5.0, got {rating}")
        self.ratings.append(rating)

    def average_rating(self):
        """Return the mean of all ratings rounded to 2 decimal places."""
        # can't compute an average with nothing in the list
        if len(self.ratings) == 0:
            raise RuntimeError("No ratings yet")
        avg = sum(self.ratings) / len(self.ratings)
        return round(avg, 2)

    def __str__(self):
        """Return a readable one-line summary of the movie."""
        # show N/A when there are no ratings yet
        if len(self.ratings) == 0:
            rating_str = "N/A"
        else:
            rating_str = f"{self.average_rating():.2f}"
        # only show year if it was parsed successfully
        year_part = f" ({self.year})" if self.year > 0 else ""
        return f"{self.title}{year_part} | Genre: {self.genre} | Avg Rating: {rating_str}"

    def __len__(self):
        """Return how many ratings this movie has."""
        return len(self.ratings)

    def __eq__(self, other):
        """Two movies are equal if they share the same movie_id."""
        return self.movie_id == other.movie_id
