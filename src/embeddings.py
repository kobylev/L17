"""
Word2Vec embedding generation for text data
"""

import numpy as np
from gensim.models import Word2Vec
from .preprocessing import clean_text, tokenize_text


def texts_to_embeddings(texts, vector_size=300):
    """
    Convert texts to vector embeddings using Word2Vec

    Args:
        texts: List of raw text strings
        vector_size: Dimensionality of word vectors (default: 300)

    Returns:
        tuple: (embeddings, tokenized_texts, valid_indices, w2v_model)
            - embeddings: numpy array of shape (n_texts, vector_size)
            - tokenized_texts: list of tokenized texts
            - valid_indices: indices of texts with valid embeddings
            - w2v_model: trained Word2Vec model
    """
    print(f"\n{'='*60}")
    print("WORD2VEC EMBEDDING GENERATION")
    print(f"{'='*60}")

    # Preprocess texts
    print("\nPreprocessing texts...")
    cleaned_texts = [clean_text(text) for text in texts]
    tokenized_texts = [tokenize_text(text) for text in cleaned_texts]

    # Remove empty texts
    tokenized_texts = [text for text in tokenized_texts if len(text) > 0]
    print(f"  Total texts after cleaning: {len(tokenized_texts)}")

    # Train Word2Vec model
    print(f"\nTraining Word2Vec model (vector_size={vector_size})...")
    w2v_model = Word2Vec(
        sentences=tokenized_texts,
        vector_size=vector_size,
        window=5,
        min_count=2,
        workers=4,
        epochs=10
    )
    print(f"  Vocabulary size: {len(w2v_model.wv)}")

    # Convert texts to document vectors (average of word vectors)
    print("\nConverting texts to document vectors...")
    text_vectors = []
    valid_indices = []

    for idx, text in enumerate(tokenized_texts):
        word_vectors = []
        for word in text:
            if word in w2v_model.wv:
                word_vectors.append(w2v_model.wv[word])

        if len(word_vectors) > 0:
            # Average pooling of word vectors
            text_vector = np.mean(word_vectors, axis=0)
            text_vectors.append(text_vector)
            valid_indices.append(idx)

    embeddings = np.array(text_vectors)
    print(f"  Final embeddings shape: {embeddings.shape}")

    return embeddings, tokenized_texts, valid_indices, w2v_model
