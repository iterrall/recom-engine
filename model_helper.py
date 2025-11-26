import pickle
from implicit_markov_chain import ImplicitMarkovChain

def save_model(model, filename):
    """Save the trained model"""
    with open(filename, 'wb') as f:
        pickle.dump({
            'transition_matrix': model.transition_matrix,
            'movie_ids': model.movie_ids,
            'movie_to_idx': model.movie_to_idx,
            'alpha': model.alpha
        }, f)
    print(f"Model saved to {filename}")

def load_model(filename):
    """Load a trained model"""
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    
    model = ImplicitMarkovChain(alpha=data['alpha'])
    model.transition_matrix = data['transition_matrix']
    model.movie_ids = data['movie_ids']
    model.movie_to_idx = data['movie_to_idx']
    model.idx_to_movie = {idx: movie for movie, idx in model.movie_to_idx.items()}
    
    print(f"Model loaded from {filename}")
    return model