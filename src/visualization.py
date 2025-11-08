"""
Visualization functions for PCA and t-SNE results
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def visualize_3d(data_pca, data_tsne, runtime_pca, runtime_tsne, labels=None, texts=None, output_dir='outputs'):
    """
    Create 3D visualization plots for PCA and t-SNE with category coloring

    Args:
        data_pca: PCA-transformed data (n_samples, 3)
        data_tsne: t-SNE-transformed data (n_samples, 3)
        runtime_pca: PCA execution time in seconds
        runtime_tsne: t-SNE execution time in seconds
        labels: Category labels for each sample (optional)
        texts: Original text samples for annotation (optional)
        output_dir: Directory to save visualization (default: 'outputs')
    """
    fig = plt.figure(figsize=(18, 8))

    # Define color mapping for categories
    if labels is not None:
        unique_labels = sorted(set(labels))
        color_map = plt.cm.get_cmap('tab10', len(unique_labels))
        label_to_color = {label: i for i, label in enumerate(unique_labels)}
        colors = [label_to_color[label] for label in labels]

        print(f"\n   Color mapping for {len(unique_labels)} categories:")
        for i, label in enumerate(unique_labels):
            print(f"     {i+1}. {label}")
    else:
        colors = range(len(data_pca))
        unique_labels = None

    # PCA plot
    ax1 = fig.add_subplot(121, projection='3d')
    scatter1 = ax1.scatter(
        data_pca[:, 0],
        data_pca[:, 1],
        data_pca[:, 2],
        c=colors,
        cmap='tab10' if labels is not None else 'viridis',
        alpha=0.7,
        s=30,
        edgecolors='black',
        linewidths=0.5
    )
    ax1.set_xlabel('PC1 (First Principal Component)', fontsize=10)
    ax1.set_ylabel('PC2 (Second Principal Component)', fontsize=10)
    ax1.set_zlabel('PC3 (Third Principal Component)', fontsize=10)
    ax1.set_title(f'Manual PCA (3D)\nEach point = one text | Runtime: {runtime_pca:.4f}s',
                  fontsize=11, fontweight='bold')

    if labels is None:
        plt.colorbar(scatter1, ax=ax1, label='Sample Index', pad=0.1, shrink=0.6)

    # Add text annotation
    ax1.text2D(0.05, 0.95, 'Linear projection:\nPreserves global structure',
               transform=ax1.transAxes, fontsize=9,
               verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))

    # t-SNE plot
    ax2 = fig.add_subplot(122, projection='3d')
    scatter2 = ax2.scatter(
        data_tsne[:, 0],
        data_tsne[:, 1],
        data_tsne[:, 2],
        c=colors,
        cmap='tab10' if labels is not None else 'plasma',
        alpha=0.7,
        s=30,
        edgecolors='black',
        linewidths=0.5
    )
    ax2.set_xlabel('t-SNE Dimension 1', fontsize=10)
    ax2.set_ylabel('t-SNE Dimension 2', fontsize=10)
    ax2.set_zlabel('t-SNE Dimension 3', fontsize=10)
    ax2.set_title(f't-SNE (3D)\nEach point = one text | Runtime: {runtime_tsne:.4f}s',
                  fontsize=11, fontweight='bold')

    if labels is None:
        plt.colorbar(scatter2, ax=ax2, label='Sample Index', pad=0.1, shrink=0.6)

    # Add text annotation
    ax2.text2D(0.05, 0.95, 'Non-linear projection:\nPreserves local neighborhoods',
               transform=ax2.transAxes, fontsize=9,
               verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))

    # Add shared legend for categories
    if labels is not None:
        # Create legend handles
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor=color_map(label_to_color[label]),
                                edgecolor='black', label=label)
                          for label in unique_labels]

        # Add legend below both plots
        fig.legend(handles=legend_elements, loc='lower center', ncol=min(4, len(unique_labels)),
                  fontsize=9, title='Topic Categories', title_fontsize=10,
                  bbox_to_anchor=(0.5, -0.05), frameon=True, fancybox=True, shadow=True)

        # Optionally annotate a few sample points (not too many to avoid clutter)
        if texts is not None and len(texts) > 0:
            print(f"\n   Sample annotations from different categories:")
            # Select one representative from each category for annotation
            annotated_samples = {}
            for i, (label, text) in enumerate(zip(labels, texts)):
                if label not in annotated_samples and len(text) > 30:
                    # Take the first good example from each category
                    annotated_samples[label] = (i, text[:60] + '...' if len(text) > 60 else text)
                if len(annotated_samples) >= min(3, len(unique_labels)):  # Limit to 3 annotations
                    break

            for label, (idx, sample_text) in annotated_samples.items():
                print(f"     [{label}]: {sample_text}")

    plt.tight_layout()
    filepath = f'{output_dir}/text_pca_tsne_comparison.png'
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"\nVisualization saved as '{filepath}'")
    plt.close()


def plot_runtime_comparison(runtime_pca, runtime_tsne, output_dir='outputs'):
    """
    Create runtime comparison bar chart

    Args:
        runtime_pca: PCA execution time in seconds
        runtime_tsne: t-SNE execution time in seconds
        output_dir: Directory to save chart (default: 'outputs')
    """
    print("\nCreating runtime comparison chart...")
    fig_runtime = plt.figure(figsize=(10, 6))
    methods = ['Manual PCA', 't-SNE']
    runtimes = [runtime_pca, runtime_tsne]
    colors = ['#2ecc71', '#e74c3c']

    bars = plt.bar(methods, runtimes, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)

    # Add value labels on bars
    for i, (bar, runtime) in enumerate(zip(bars, runtimes)):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{runtime:.4f}s',
                ha='center', va='bottom', fontsize=12, fontweight='bold')

    plt.ylabel('Runtime (seconds)', fontsize=12, fontweight='bold')
    plt.title('Runtime Comparison: PCA vs t-SNE\n(Lower is Better)', fontsize=14, fontweight='bold')
    plt.grid(axis='y', alpha=0.3, linestyle='--')

    # Add speedup annotation
    speedup = runtime_tsne / runtime_pca
    plt.text(0.5, max(runtimes) * 0.9,
            f'PCA is {speedup:.1f}x FASTER',
            ha='center', fontsize=13, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7))

    plt.tight_layout()
    filepath = f'{output_dir}/runtime_comparison.png'
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"Runtime comparison chart saved as '{filepath}'")
    plt.close()


def plot_category_histogram(labels, output_dir='outputs'):
    """
    Create histogram showing the distribution of samples across categories

    Args:
        labels: List of category labels for each sample
        output_dir: Directory to save histogram (default: 'outputs')
    """
    from collections import Counter

    print("\nCreating category distribution histogram...")

    # Count occurrences of each category
    label_counts = Counter(labels)

    # Sort by count (descending)
    sorted_categories = sorted(label_counts.items(), key=lambda x: x[1], reverse=True)
    categories = [cat for cat, _ in sorted_categories]
    counts = [count for _, count in sorted_categories]

    # Create figure
    fig, ax = plt.subplots(figsize=(12, 7))

    # Define colors - use a colormap
    colors = plt.cm.tab10(np.linspace(0, 1, len(categories)))

    # Create bars
    bars = ax.bar(range(len(categories)), counts, color=colors, alpha=0.8,
                  edgecolor='black', linewidth=1.5)

    # Add value labels on bars
    for i, (bar, count) in enumerate(zip(bars, counts)):
        height = bar.get_height()
        percentage = (count / sum(counts)) * 100
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{count}\n({percentage:.1f}%)',
                ha='center', va='bottom', fontsize=10, fontweight='bold')

    # Customize plot
    ax.set_xlabel('Category', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Samples', fontsize=12, fontweight='bold')
    ax.set_title(f'Distribution of Samples Across Categories\nTotal Samples: {sum(counts)}',
                fontsize=14, fontweight='bold')
    ax.set_xticks(range(len(categories)))
    ax.set_xticklabels(categories, rotation=45, ha='right', fontsize=10)
    ax.grid(axis='y', alpha=0.3, linestyle='--')

    # Add summary statistics
    summary_text = f'Categories: {len(categories)}\nAvg per category: {sum(counts)/len(categories):.1f}'
    ax.text(0.98, 0.97, summary_text,
            transform=ax.transAxes, fontsize=10,
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))

    plt.tight_layout()
    filepath = f'{output_dir}/category_histogram.png'
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"Category histogram saved as '{filepath}'")

    # Print detailed statistics
    print(f"\n   Category Distribution Statistics:")
    print(f"   {'='*50}")
    for category, count in sorted_categories:
        percentage = (count / sum(counts)) * 100
        bar_visual = '#' * int(percentage / 2)  # Visual bar
        print(f"   {category:<25} {count:>5} ({percentage:>5.1f}%) {bar_visual}")
    print(f"   {'='*50}")
    print(f"   {'Total':<25} {sum(counts):>5} (100.0%)")

    plt.close()


def plot_variance_pie_charts(pca_model, data_pca, data_tsne, output_dir='outputs'):
    """
    Create separate pie charts showing explained variance for PCA and t-SNE methods

    Args:
        pca_model: Fitted PCA model with explained_variance_ratio_
        data_pca: PCA-transformed data for calculating component variances
        data_tsne: t-SNE-transformed data for calculating dimension variances
        output_dir: Directory to save visualization (default: 'outputs')
    """
    print("\nCreating variance explanation pie charts...")

    pca_variance_ratios = pca_model.explained_variance_ratio_

    # ===== PCA Pie Chart (Separate Plot) =====
    fig1, ax1 = plt.subplots(figsize=(10, 8))

    pca_labels = [
        f'PC1: {pca_variance_ratios[0]*100:.2f}%',
        f'PC2: {pca_variance_ratios[1]*100:.2f}%',
        f'PC3: {pca_variance_ratios[2]*100:.2f}%',
        f'Lost: {(1 - pca_variance_ratios.sum())*100:.2f}%'
    ]

    pca_sizes = [
        pca_variance_ratios[0],
        pca_variance_ratios[1],
        pca_variance_ratios[2],
        1 - pca_variance_ratios.sum()
    ]

    pca_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#D3D3D3']
    pca_explode = (0.05, 0.05, 0.05, 0)  # Explode the first 3 slices

    wedges1, texts1, autotexts1 = ax1.pie(
        pca_sizes,
        labels=pca_labels,
        colors=pca_colors,
        autopct='%1.2f%%',
        startangle=90,
        explode=pca_explode,
        textprops={'fontsize': 12, 'fontweight': 'bold'}
    )

    ax1.set_title(
        f'PCA Explained Variance from Original 300D Data\nTotal Preserved: {pca_variance_ratios.sum()*100:.2f}%',
        fontsize=14,
        fontweight='bold',
        pad=20
    )

    # Add explanation text
    explanation = (
        'This chart shows how much of the original 300-dimensional\n'
        'variance is captured by each of the 3 principal components.\n'
        f'Only {(1-pca_variance_ratios.sum())*100:.2f}% of information is lost in the reduction.'
    )
    ax1.text(0.5, -0.15, explanation, transform=ax1.transAxes,
             ha='center', fontsize=10, style='italic',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    filepath1 = f'{output_dir}/pca_variance_pie.png'
    plt.savefig(filepath1, dpi=300, bbox_inches='tight')
    print(f"PCA variance pie chart saved as '{filepath1}'")
    plt.close()

    # ===== t-SNE Pie Chart (Separate Plot) =====
    fig2, ax2 = plt.subplots(figsize=(10, 8))

    # For t-SNE, calculate variance in each output dimension
    tsne_var = np.var(data_tsne, axis=0)
    tsne_var_ratio = tsne_var / tsne_var.sum()

    tsne_labels = [
        f'Dimension 1: {tsne_var_ratio[0]*100:.2f}%',
        f'Dimension 2: {tsne_var_ratio[1]*100:.2f}%',
        f'Dimension 3: {tsne_var_ratio[2]*100:.2f}%'
    ]

    tsne_sizes = tsne_var_ratio
    tsne_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    tsne_explode = (0.05, 0.05, 0.05)

    wedges2, texts2, autotexts2 = ax2.pie(
        tsne_sizes,
        labels=tsne_labels,
        colors=tsne_colors,
        autopct='%1.2f%%',
        startangle=90,
        explode=tsne_explode,
        textprops={'fontsize': 12, 'fontweight': 'bold'}
    )

    ax2.set_title(
        't-SNE Variance Distribution in 3D Output Space\n(Relative Distribution Only)',
        fontsize=14,
        fontweight='bold',
        pad=20
    )

    # Add explanation text
    explanation = (
        'This chart shows the relative variance distribution across\n'
        't-SNE\'s 3 output dimensions. These percentages DO NOT represent\n'
        'preserved variance from the original 300D space.\n'
        't-SNE optimizes for local structure, not variance preservation.'
    )
    ax2.text(0.5, -0.15, explanation, transform=ax2.transAxes,
             ha='center', fontsize=10, style='italic',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))

    plt.tight_layout()
    filepath2 = f'{output_dir}/tsne_variance_pie.png'
    plt.savefig(filepath2, dpi=300, bbox_inches='tight')
    print(f"t-SNE variance pie chart saved as '{filepath2}'")
    plt.close()

    # Print detailed statistics
    print(f"\n   PCA Variance Explanation:")
    print(f"   {'='*50}")
    print(f"   PC1: {pca_variance_ratios[0]*100:>6.2f}% of original variance")
    print(f"   PC2: {pca_variance_ratios[1]*100:>6.2f}% of original variance")
    print(f"   PC3: {pca_variance_ratios[2]*100:>6.2f}% of original variance")
    print(f"   {'='*50}")
    print(f"   Total captured: {pca_variance_ratios.sum()*100:>6.2f}%")
    print(f"   Total lost:     {(1-pca_variance_ratios.sum())*100:>6.2f}%")

    print(f"\n   t-SNE Relative Dimension Distribution:")
    print(f"   {'='*50}")
    print(f"   Dimension 1: {tsne_var_ratio[0]*100:>6.2f}% (relative)")
    print(f"   Dimension 2: {tsne_var_ratio[1]*100:>6.2f}% (relative)")
    print(f"   Dimension 3: {tsne_var_ratio[2]*100:>6.2f}% (relative)")
    print(f"   {'='*50}")
    print(f"   Note: t-SNE doesn't preserve variance - values show")
    print(f"         how spread varies across the 3 output dimensions")
