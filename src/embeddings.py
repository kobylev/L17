"""
Word2Vec embedding generation for tweet data
"""

import numpy as np
from gensim.models import Word2Vec
from .preprocessing import clean_text, tokenize_text


def tweets_to_embeddings(tweets, vector_size=300):
    """
    Convert tweets to vector embeddings using Word2Vec

    Args:
        tweets: List of raw tweet strings
        vector_size: Dimensionality of word vectors (default: 300)

    Returns:
        tuple: (embeddings, tokenized_tweets, valid_indices, w2v_model)
            - embeddings: numpy array of shape (n_tweets, vector_size)
            - tokenized_tweets: list of tokenized tweets
            - valid_indices: indices of tweets with valid embeddings
            - w2v_model: trained Word2Vec model
    """
    print(f"\n{'='*60}")
    print("WORD2VEC EMBEDDING GENERATION")
    print(f"{'='*60}")

    # Preprocess tweets
    print("\nPreprocessing tweets...")
    cleaned_tweets = [clean_text(tweet) for tweet in tweets]
    tokenized_tweets = [tokenize_text(tweet) for tweet in cleaned_tweets]

    # Remove empty tweets
    tokenized_tweets = [tweet for tweet in tokenized_tweets if len(tweet) > 0]
    print(f"  Total tweets after cleaning: {len(tokenized_tweets)}")

    # Train Word2Vec model
    print(f"\nTraining Word2Vec model (vector_size={vector_size})...")
    w2v_model = Word2Vec(
        sentences=tokenized_tweets,
        vector_size=vector_size,
        window=5,
        min_count=2,
        workers=4,
        epochs=10
    )
    print(f"  Vocabulary size: {len(w2v_model.wv)}")

    # Convert tweets to document vectors (average of word vectors)
    print("\nConverting tweets to document vectors...")
    tweet_vectors = []
    valid_indices = []

    for idx, tweet in enumerate(tokenized_tweets):
        word_vectors = []
        for word in tweet:
            if word in w2v_model.wv:
                word_vectors.append(w2v_model.wv[word])

        if len(word_vectors) > 0:
            # Average pooling of word vectors
            tweet_vector = np.mean(word_vectors, axis=0)
            tweet_vectors.append(tweet_vector)
            valid_indices.append(idx)

    embeddings = np.array(tweet_vectors)
    print(f"  Final embeddings shape: {embeddings.shape}")

    return embeddings, tokenized_tweets, valid_indices, w2v_model
