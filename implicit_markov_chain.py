import numpy as np
from tqdm import tqdm

class ImplicitMarkovChain:
    def __init__(self, alpha=2.0):
        self.alpha = alpha
        self.transition_matrix = None
        self.movie_info = None
        
    def build_transition_matrix_efficient(self, ratings_df, sample_fraction=0.1):
        """Memory-efficient implementation using sampling"""
        
        # Sample users to reduce memory (optional)
        if sample_fraction < 1.0:
            unique_users = ratings_df['userId'].unique()
            sampled_users = np.random.choice(
                unique_users, 
                size=int(len(unique_users) * sample_fraction), 
                replace=False
            )
            ratings_df = ratings_df[ratings_df['userId'].isin(sampled_users)]
            print(f"Sampled {len(sampled_users)} users")
        
        # Add confidence column
        ratings_df = ratings_df.copy()
        ratings_df['confidence'] = 1 + self.alpha * ratings_df['rating']
        
        # Group by user and process each user's ratings
        user_groups = ratings_df.groupby('userId')
        movie_pairs = {}
        
        # print("Processing user ratings...")
        # print(f"User Groups: {len(user_groups)}")
        # count = 1
        for user_id, user_ratings in tqdm(user_groups):
            if len(user_ratings) < 2:
                continue
                
            movies = user_ratings['movieId'].values
            confidences = user_ratings['confidence'].values
            
            # For each pair of movies rated by this user
            # print(f"debug: {count}/{len(user_groups)}")
            # count += 1
            for i in range(len(movies)):
                for j in range(len(movies)):
                    if i != j:
                        pair = (movies[i], movies[j])
                        strength = min(confidences[i], confidences[j])
                        
                        if pair in movie_pairs:
                            movie_pairs[pair] += strength
                        else:
                            movie_pairs[pair] = strength
        
        # Convert to transition matrix
        all_movies = ratings_df['movieId'].unique()
        movie_to_idx = {movie: idx for idx, movie in enumerate(all_movies)}
        n_movies = len(all_movies)
        
        transition_strength = np.zeros((n_movies, n_movies))
        
        for (from_movie, to_movie), strength in movie_pairs.items():
            if from_movie in movie_to_idx and to_movie in movie_to_idx:
                i = movie_to_idx[from_movie]
                j = movie_to_idx[to_movie]
                transition_strength[i, j] = strength
        
        # Normalize to probabilities
        row_sums = transition_strength.sum(axis=1)
        row_sums[row_sums == 0] = 1
        transition_matrix = transition_strength / row_sums[:, np.newaxis]
        
        self.transition_matrix = transition_matrix
        self.movie_ids = all_movies
        self.movie_to_idx = movie_to_idx
        self.idx_to_movie = {idx: movie for movie, idx in movie_to_idx.items()}
        
        return self
    
    def recommend(self, movie_id, top_n=10):
        """Get recommendations for a given movie"""
        if movie_id not in self.movie_to_idx:
            return []
        
        movie_idx = self.movie_to_idx[movie_id]
        probabilities = self.transition_matrix[movie_idx]
        
        # Get top N recommendations
        top_indices = np.argsort(probabilities)[::-1][:top_n+1]  # +1 to account for self
        
        recommendations = []
        for idx in top_indices:
            rec_movie_id = self.idx_to_movie[idx]
            if rec_movie_id != movie_id and probabilities[idx] > 0:
                recommendations.append((rec_movie_id, probabilities[idx]))
            if len(recommendations) >= top_n:
                break
        
        return recommendations