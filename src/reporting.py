"""
Analysis reporting and discussion utilities
"""


def print_header():
    """Print analysis section header"""
    print(f"\n{'='*60}")
    print("ANALYSIS & DISCUSSION")
    print(f"{'='*60}")


def print_visual_separation_analysis():
    """Print analysis of visual separation and clustering patterns"""
    print("\nVISUAL SEPARATION & CLUSTERING:")
    print("-" * 60)
    print("PCA Results:")
    print("  • Linear dimensionality reduction preserving global structure")
    print("  • Data points spread across principal components")
    print("  • Variance captured by top 3 components shown above")
    print("  • May show gradual transitions rather than distinct clusters")

    print("\nt-SNE Results:")
    print("  • Non-linear dimensionality reduction preserving local structure")
    print("  • Better at revealing local neighborhoods and clusters")
    print("  • May show more distinct groupings of similar tweets")
    print("  • Sensitive to perplexity parameter (balance local/global)")


def print_pca_tsne_comparison():
    """Print comprehensive PCA vs t-SNE comparison"""
    print("\nPCA vs t-SNE COMPARISON:")
    print("-" * 60)
    print("PCA Advantages:")
    print("  + Deterministic (same result every run)")
    print("  + Fast computation - linear complexity")
    print("  + Interpretable components (linear combinations)")
    print("  + Good for preserving global structure")
    print("  + Can be inverted to reconstruct original space")
    print("  + Suitable for preprocessing before other algorithms")

    print("\nPCA Limitations:")
    print("  - Only captures linear relationships")
    print("  - May miss complex non-linear patterns")
    print("  - Assumes data variance = importance")
    print("  - Less effective for highly non-linear manifolds")

    print("\nt-SNE Advantages:")
    print("  + Captures non-linear relationships")
    print("  + Excellent for visualization and clustering")
    print("  + Preserves local neighborhood structure")
    print("  + Often reveals hidden patterns in high-dim data")

    print("\nt-SNE Limitations:")
    print("  - Computationally expensive (especially for large datasets)")
    print("  - Non-deterministic (different runs -> different results)")
    print("  - Sensitive to hyperparameters (perplexity, learning rate)")
    print("  - Doesn't preserve global structure well")
    print("  - Cannot be used to transform new data points")
    print("  - Distances between clusters may not be meaningful")


def print_recommendations():
    """Print recommendations for using PCA vs t-SNE on text data"""
    print("\nRECOMMENDATIONS FOR TEXT DATA:")
    print("-" * 60)
    print("• Use PCA when:")
    print("  - You need fast results for large datasets")
    print("  - Interpretability of components is important")
    print("  - Preprocessing for downstream ML tasks")
    print("  - You need deterministic reproducible results")

    print("\n• Use t-SNE when:")
    print("  - Visualization and exploration is the goal")
    print("  - Dataset is moderate size (<10,000 samples)")
    print("  - You want to discover hidden clusters")
    print("  - Non-linear patterns are expected")

    print("\n• Hybrid approach:")
    print("  - Apply PCA first to reduce to ~50 dimensions")
    print("  - Then apply t-SNE for final 2D/3D visualization")
    print("  - Combines speed of PCA with quality of t-SNE")


def print_footer():
    """Print analysis completion footer"""
    print(f"\n{'='*60}")
    print("ANALYSIS COMPLETE")
    print(f"{'='*60}\n")


def print_runtime_comparison(runtime_pca, runtime_tsne):
    """
    Print runtime comparison between PCA and t-SNE

    Args:
        runtime_pca: PCA execution time in seconds
        runtime_tsne: t-SNE execution time in seconds
    """
    print(f"\n{'='*60}")
    print("RUNTIME COMPARISON")
    print(f"{'='*60}")
    print(f"  Manual PCA Runtime:  {runtime_pca:.4f} seconds")
    print(f"  t-SNE Runtime:       {runtime_tsne:.4f} seconds")
    print(f"  Speedup (t-SNE/PCA): {runtime_tsne/runtime_pca:.2f}x")
    print(f"  PCA is {runtime_tsne/runtime_pca:.2f}x faster than t-SNE")


def print_analysis_discussion():
    """
    Print comprehensive analysis and discussion of results

    Includes:
    - Visual separation and clustering analysis
    - PCA vs t-SNE comparison
    - Recommendations for text data
    """
    print_header()
    print_visual_separation_analysis()
    print_pca_tsne_comparison()
    print_recommendations()
    print_footer()
