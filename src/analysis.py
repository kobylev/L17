"""
PCA component analysis and interpretation utilities
"""

import numpy as np


def analyze_pca_components(pca, w2v_model, top_n=10):
    """
    Analyze which embedding dimensions contribute most to each PC

    Note: With Word2Vec, we can't directly map to words, but we can show
    which dimensions are most important

    Args:
        pca: Fitted ManualPCA object
        w2v_model: Trained Word2Vec model
        top_n: Number of top contributing dimensions to show (default: 10)
    """
    print(f"\n{'='*60}")
    print("PCA COMPONENT INTERPRETATION")
    print(f"{'='*60}")

    print("\nIMPORTANT: PCA components are mathematical abstractions")
    print("They are linear combinations of all 300 Word2Vec dimensions.")
    print("We cannot directly map them to specific words or topics.\n")

    for i in range(pca.n_components):
        component = pca.components_[:, i]

        # Get top contributing dimensions (by absolute weight)
        abs_weights = np.abs(component)
        top_indices = np.argsort(abs_weights)[-top_n:][::-1]

        print(f"PC{i+1} - Top {top_n} Contributing Embedding Dimensions:")
        print(f"  (These are Word2Vec dimensions, not individual words)")
        print(f"  Dimension | Weight      | Interpretation")
        print(f"  " + "-" * 50)

        for rank, dim_idx in enumerate(top_indices, 1):
            weight = component[dim_idx]
            influence = 'High' if abs(weight) > 0.1 else 'Moderate'
            print(f"  Dim {dim_idx:3d}   | {weight:+.6f} | {influence} influence")

        print(f"\n  Statistical Summary:")
        print(f"    - Max absolute weight: {np.max(abs_weights):.6f}")
        print(f"    - Mean absolute weight: {np.mean(abs_weights):.6f}")
        print(f"    - Std of weights: {np.std(component):.6f}")
        print()

    print("=" * 60)
    print("SEMANTIC INTERPRETATION NOTES:")
    print("=" * 60)
    print("Since components are combinations of 300 dimensions:")
    print("  - PC1: Likely captures the dominant semantic axis")
    print("         (e.g., sentiment, formality, or topic breadth)")
    print("  - PC2: Secondary orthogonal variation")
    print("         (e.g., information vs opinion, or sub-topics)")
    print("  - PC3: Tertiary variation, increasingly abstract")
    print("\nTo find semantic meaning, you would need to:")
    print("  1. Examine texts with extreme PC values (high/low)")
    print("  2. Look for patterns in their content")
    print("  3. Label the axis based on observed differences")
    print()
