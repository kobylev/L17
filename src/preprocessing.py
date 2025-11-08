"""
Text preprocessing utilities for tweet data
"""

import re


def clean_text(text):
    """
    Clean and preprocess tweet text

    Args:
        text: Raw tweet text

    Returns:
        Cleaned text string
    """
    if not isinstance(text, str):
        return ""

    # Convert to lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)

    # Remove user mentions and hashtags
    text = re.sub(r'@\w+|#', '', text)

    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def tokenize_text(text):
    """
    Tokenize cleaned text into words

    Args:
        text: Cleaned text string

    Returns:
        List of word tokens
    """
    return text.split()
