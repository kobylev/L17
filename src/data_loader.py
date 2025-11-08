"""
Dataset loading utilities for text analysis
"""

import pandas as pd
import os


def categorize_text(text):
    """
    Categorize text based on keyword presence

    Args:
        text: Input text string

    Returns:
        str: Category label
    """
    text_lower = text.lower()

    # Define topic categories based on common themes in alt.atheism
    if any(word in text_lower for word in ['bible', 'scripture', 'gospel', 'testament', 'biblical']):
        return 'Bible Discussion'
    elif any(word in text_lower for word in ['religion', 'church', 'faith', 'belief', 'god', 'christian', 'islam', 'muslim']):
        return 'Religion & Faith'
    elif any(word in text_lower for word in ['atheist', 'atheism', 'secular', 'humanist', 'freethinker', 'rationalist']):
        return 'Atheism & Humanism'
    elif any(word in text_lower for word in ['moral', 'ethics', 'ethical', 'morality', 'philosophy']):
        return 'Ethics & Philosophy'
    elif any(word in text_lower for word in ['science', 'evolution', 'evidence', 'research', 'study']):
        return 'Science & Evidence'
    elif any(word in text_lower for word in ['political', 'government', 'state', 'law', 'rights', 'separation']):
        return 'Politics & Society'
    else:
        return 'General Discussion'


def load_dataset():
    """
    Load text dataset from alt.atheism.txt or fallback options

    Attempts to load from:
    1. data/alt.atheism.txt (primary text file)
    2. CSV files (COVID-19 tweets)
    3. Demo data (fallback)

    Returns:
        tuple: (texts, labels) - List of text strings and their category labels
    """
    print(f"\n{'='*60}")
    print("TEXT DIMENSIONALITY REDUCTION ANALYSIS")
    print(f"{'='*60}")

    print("\n1. Loading dataset...")

    # Try loading alt.atheism.txt first
    atheism_file = 'data/alt.atheism.txt'
    if os.path.exists(atheism_file):
        print(f"   Found: {atheism_file}")
        try:
            with open(atheism_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            # Filter out empty lines and very short lines
            texts = [line.strip() for line in lines if len(line.strip()) > 20]

            print(f"   Total lines: {len(lines)}")
            print(f"   Valid text lines: {len(texts)}")

            # Sample for faster processing
            import random
            random.seed(42)
            n_samples = min(5000, len(texts))
            sampled_texts = random.sample(texts, n_samples)

            # Categorize each text
            labels = [categorize_text(text) for text in sampled_texts]

            # Count categories
            from collections import Counter
            label_counts = Counter(labels)

            print(f"   Sampled {n_samples} text lines for analysis")
            print(f"   Dataset: alt.atheism newsgroup posts")
            print(f"\n   Topic Distribution:")
            for category, count in sorted(label_counts.items(), key=lambda x: x[1], reverse=True):
                print(f"     - {category}: {count} ({100*count/n_samples:.1f}%)")

            return sampled_texts, labels

        except Exception as e:
            print(f"   Error loading {atheism_file}: {e}")
            print("   Trying CSV fallback...")

    # Fallback to CSV files
    try:
        print("   Looking for CSV files...")
        possible_files = [
            'coronavirus_tweets.csv',
            'covid19_tweets.csv',
            'tweets.csv',
            'Corona_NLP_train.csv',
            'Corona_NLP_test.csv'
        ]

        df = None
        for filename in possible_files:
            try:
                df = pd.read_csv(filename, encoding='utf-8')
                print(f"   Loaded: {filename}")
                break
            except FileNotFoundError:
                continue
            except UnicodeDecodeError:
                try:
                    df = pd.read_csv(filename, encoding='latin-1')
                    print(f"   Loaded: {filename} (latin-1 encoding)")
                    break
                except:
                    continue

        if df is None:
            raise FileNotFoundError("No dataset files found")

        print(f"   Dataset shape: {df.shape}")
        print(f"   Columns: {list(df.columns)}")

        # Find text column
        text_columns = ['text', 'OriginalTweet', 'tweet', 'Tweet', 'full_text']
        text_col = None
        for col in text_columns:
            if col in df.columns:
                text_col = col
                break

        if text_col is None:
            print(f"\n   Available columns: {list(df.columns)}")
            raise ValueError("Could not find text column")

        print(f"   Using text column: '{text_col}'")

        # Sample tweets for faster processing
        n_samples = min(5000, len(df))
        sampled_df = df.sample(n=n_samples, random_state=42)
        tweets = sampled_df[text_col].values

        # Categorize each text
        labels = [categorize_text(str(text)) for text in tweets]

        print(f"   Sampled {n_samples} texts for analysis")

        return tweets, labels

    except Exception as e:
        print(f"\n   WARNING: Could not load any dataset files!")
        print(f"   Error: {e}")
        print("   Using demo data for demonstration...")
        return _get_demo_data()


def _get_demo_data():
    """
    Generate demo dataset for testing when real data is unavailable

    Returns:
        tuple: (texts, labels) - List of sample texts and their category labels
    """
    tweets = [
        "COVID-19 cases are rising in many countries",
        "Get vaccinated to protect yourself and others",
        "Wearing masks helps prevent coronavirus spread",
        "Social distancing is important during pandemic",
        "Healthcare workers are heroes fighting COVID",
    ] * 200  # Replicate for demonstration

    labels = [categorize_text(text) for text in tweets]

    return tweets, labels
