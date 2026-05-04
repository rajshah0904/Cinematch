class User:
    """Represents a user with a watch history and genre preferences."""

    def __init__(self, user_id, name):
        """Set up the user with their id, name, and empty history and preferences."""
        self.user_id = user_id
        self.name = name
        # list of movie_ids the user has watched
        self.watch_history = []
        # genres the user prefers
        self.preferred_genres = []

    def add_to_history(self, movie_id):
        """Add a movie_id to watch history only if it isn't already there."""
        # don't add duplicates
        if movie_id not in self.watch_history:
            self.watch_history.append(movie_id)

    def set_preferred_genres(self, genres):
        """Replace the preferred genres list with the given one."""
        self.preferred_genres = genres

    def get_genre_profile(self, movie_lookup):
        """Return a dict mapping each preferred genre to how many watched movies belong to it."""
        # start every preferred genre at 0
        genre_counts = {genre: 0 for genre in self.preferred_genres}

        # go through the watch history and count genre matches
        for movie_id in self.watch_history:
            if movie_id in movie_lookup:
                movie = movie_lookup[movie_id]
                if movie.genre in genre_counts:
                    genre_counts[movie.genre] += 1

        return genre_counts

    def __str__(self):
        """Return a short readable summary of this user."""
        num_watched = len(self.watch_history)
        genres_str = ", ".join(self.preferred_genres) if self.preferred_genres else "None"
        return f"User {self.user_id} ({self.name}) | Watched: {num_watched} movies | Preferred: {genres_str}"
