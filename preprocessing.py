

def preprocess_data(ratings, min_ratings_per_user=5, min_ratings_per_movie=50):
    """Preprocess the ratings data"""
    print("Original ratings shape:", ratings.shape)
    
    # Filter out users with too few ratings
    user_rating_counts = ratings['userId'].value_counts()
    active_users = user_rating_counts[user_rating_counts >= min_ratings_per_user].index
    ratings = ratings[ratings['userId'].isin(active_users)]
    print(f"After filtering inactive users: {ratings.shape}")
    
    # Filter out movies with too few ratings
    movie_rating_counts = ratings['movieId'].value_counts()
    popular_movies = movie_rating_counts[movie_rating_counts >= min_ratings_per_movie].index
    ratings = ratings[ratings['movieId'].isin(popular_movies)]
    print(f"After filtering unpopular movies: {ratings.shape}")
    
    # Create mappings for userId and movieId
    user_ids = ratings['userId'].unique()
    movie_ids = ratings['movieId'].unique()
    
    user_to_idx = {user_id: idx for idx, user_id in enumerate(user_ids)}
    movie_to_idx = {movie_id: idx for idx, movie_id in enumerate(movie_ids)}
    idx_to_movie = {idx: movie_id for movie_id, idx in movie_to_idx.items()}
    
    return ratings, user_to_idx, movie_to_idx, idx_to_movie