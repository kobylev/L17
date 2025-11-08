"""
Analysis pipeline orchestration
Coordinates the full dimensionality reduction workflow
"""

import time
from sklearn.manifold import TSNE

from .data_loader import load_dataset
from .embeddings import texts_to_embeddings
from .pca import ManualPCA
from .analysis import analyze_pca_components
from .visualization import visualize_3d, plot_runtime_comparison, plot_category_histogram, plot_variance_pie_charts
from .reporting import print_runtime_comparison, print_analysis_discussion


def run_pca_analysis(embeddings, w2v_model, n_components=3):
    """
    Run manual PCA analysis on embeddings

    Args:
        embeddings: numpy array of shape (n_samples, n_features)
        w2v_model: trained Word2Vec model
        n_components: number of principal components (default: 3)

    Returns:
        tuple: (data_pca, runtime_pca, pca_model)
    """
    print(f"\n3. Applying Manual PCA...")
    start_time = time.time()

    pca = ManualPCA(n_components=n_components)
    data_pca = pca.fit_transform(embeddings)

    runtime = time.time() - start_time

    # Analyze PCA components
    analyze_pca_components(pca, w2v_model, top_n=10)

    return data_pca, runtime, pca


def run_tsne_analysis(embeddings, n_components=3, perplexity=30, n_iter=1000):
    """
    Run t-SNE analysis on embeddings

    Args:
        embeddings: numpy array of shape (n_samples, n_features)
        n_components: number of dimensions for output (default: 3)
        perplexity: t-SNE perplexity parameter (default: 30)
        n_iter: number of iterations (default: 1000)

    Returns:
        tuple: (data_tsne, runtime_tsne)
    """
    print(f"\n{'='*60}")
    print("t-SNE IMPLEMENTATION")
    print(f"{'='*60}")
    print(f"\nApplying t-SNE (n_components={n_components})...")

    start_time = time.time()

    tsne = TSNE(
        n_components=n_components,
        random_state=42,
        perplexity=perplexity,
        n_iter=n_iter,
        verbose=1
    )
    data_tsne = tsne.fit_transform(embeddings)

    runtime = time.time() - start_time

    print(f"  Transformed data shape: {data_tsne.shape}")

    return data_tsne, runtime


def run_full_pipeline():
    """
    Execute the complete dimensionality reduction pipeline

    Pipeline steps:
    1. Load text dataset with category labels
    2. Generate Word2Vec embeddings (300D)
    3. Apply manual PCA (reduce to 3D)
    4. Apply t-SNE (reduce to 3D)
    5. Compare runtime performance
    6. Generate visualizations with category coloring
    7. Print analysis and discussion

    Returns:
        dict: Results containing all data and metrics
    """
    # Step 1: Load dataset with labels
    texts, labels = load_dataset()

    # Step 2: Convert texts to embeddings
    print(f"\n2. Converting texts to embeddings...")
    embeddings, tokenized_texts, valid_indices, w2v_model = texts_to_embeddings(
        texts, vector_size=300
    )

    # Filter labels to match valid embeddings
    import numpy as np
    labels_array = np.array(labels)
    valid_labels = labels_array[valid_indices].tolist()

    # Step 3: Apply Manual PCA
    data_pca, runtime_pca, pca_model = run_pca_analysis(
        embeddings, w2v_model, n_components=3
    )

    # Step 4: Apply t-SNE
    data_tsne, runtime_tsne = run_tsne_analysis(
        embeddings, n_components=3, perplexity=30, n_iter=1000
    )

    # Step 5: Runtime comparison
    print_runtime_comparison(runtime_pca, runtime_tsne)

    # Create runtime comparison bar chart
    plot_runtime_comparison(runtime_pca, runtime_tsne)

    # Step 6: Visualization with category labels
    print(f"\n{'='*60}")
    print("VISUALIZATION")
    print(f"{'='*60}")

    # Get sample texts for annotation
    valid_texts = np.array(texts)[valid_indices].tolist()

    visualize_3d(data_pca, data_tsne, runtime_pca, runtime_tsne,
                labels=valid_labels, texts=valid_texts)

    # Create category distribution histogram
    plot_category_histogram(valid_labels)

    # Create variance pie charts for both methods
    plot_variance_pie_charts(pca_model, data_pca, data_tsne)

    # Step 7: Analysis and Discussion
    print_analysis_discussion()

    # Return results for further use if needed
    return {
        'texts': texts,
        'labels': labels,
        'valid_labels': valid_labels,
        'embeddings': embeddings,
        'pca_data': data_pca,
        'tsne_data': data_tsne,
        'runtime_pca': runtime_pca,
        'runtime_tsne': runtime_tsne,
        'pca_model': pca_model,
        'w2v_model': w2v_model
    }
