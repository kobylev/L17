"""
Manual PCA implementation from scratch
"""

import numpy as np


class ManualPCA:
    """
    Manual implementation of Principal Component Analysis

    Implements PCA without using sklearn.decomposition.PCA by:
    1. Mean centering the data
    2. Computing the covariance matrix
    3. Calculating eigenvalues and eigenvectors
    4. Selecting top n components
    5. Projecting data onto principal components
    """

    def __init__(self, n_components=3):
        """
        Initialize PCA

        Args:
            n_components: Number of principal components to keep (default: 3)
        """
        self.n_components = n_components
        self.components_ = None
        self.mean_ = None
        self.eigenvalues_ = None
        self.explained_variance_ratio_ = None

    def fit_transform(self, X):
        """
        Fit PCA and transform data

        Args:
            X: Input data matrix of shape (n_samples, n_features)

        Returns:
            Transformed data of shape (n_samples, n_components)

        Steps:
            1. Calculate mean-centered data matrix
            2. Compute covariance matrix
            3. Calculate eigenvalues and eigenvectors
            4. Select top n principal components
            5. Project data onto principal components
        """
        print(f"\n{'='*60}")
        print("MANUAL PCA IMPLEMENTATION")
        print(f"{'='*60}")

        # Step 1: Mean centering
        print("\nStep 1: Calculating mean-centered data matrix...")
        self.mean_ = np.mean(X, axis=0)
        X_centered = X - self.mean_
        print(f"  Original data shape: {X.shape}")
        print(f"  Mean vector shape: {self.mean_.shape}")

        # Step 2: Compute covariance matrix
        print("\nStep 2: Computing covariance matrix...")
        n_samples = X_centered.shape[0]
        cov_matrix = (1 / (n_samples - 1)) * np.dot(X_centered.T, X_centered)
        print(f"  Covariance matrix shape: {cov_matrix.shape}")

        # Step 3: Calculate eigenvalues and eigenvectors
        print("\nStep 3: Calculating eigenvalues and eigenvectors...")
        eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)

        # Sort eigenvalues and eigenvectors in descending order
        idx = eigenvalues.argsort()[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]

        self.eigenvalues_ = eigenvalues
        print(f"  Number of eigenvalues: {len(eigenvalues)}")
        print(f"  Top 5 eigenvalues: {eigenvalues[:5].real}")

        # Step 4: Select top n principal components
        print(f"\nStep 4: Selecting top {self.n_components} principal components...")
        self.components_ = eigenvectors[:, :self.n_components]
        print(f"  Components shape: {self.components_.shape}")

        # Calculate explained variance ratio
        total_variance = np.sum(eigenvalues.real)
        explained_variance = eigenvalues[:self.n_components].real
        self.explained_variance_ratio_ = explained_variance / total_variance
        print(f"\n  Explained variance ratio:")
        for i, ratio in enumerate(self.explained_variance_ratio_):
            print(f"    PC{i+1}: {ratio*100:.2f}%")
        print(f"    Total: {np.sum(self.explained_variance_ratio_)*100:.2f}%")

        # Step 5: Project data onto principal components
        print(f"\nStep 5: Projecting data to {self.n_components}D space...")
        X_pca = np.dot(X_centered, self.components_).real
        print(f"  Transformed data shape: {X_pca.shape}")

        return X_pca
