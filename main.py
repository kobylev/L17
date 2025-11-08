"""
COVID-19 Tweets Dimensionality Reduction Analysis
Main entry point

This script executes the complete analysis pipeline:
1. Dataset loading and preprocessing
2. Word2Vec embedding generation (300D)
3. Manual PCA implementation (reduce to 3D)
4. t-SNE comparison (reduce to 3D)
5. Runtime benchmarking
6. Visualization generation
7. Analysis and discussion

Usage:
    python main.py
"""

import warnings
from src.pipeline import run_full_pipeline

warnings.filterwarnings('ignore')


def main():
    """
    Main entry point - executes the full analysis pipeline
    """
    run_full_pipeline()


if __name__ == "__main__":
    main()
