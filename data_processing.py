"""
data_processing.py
Simplified functions to load, clean and merge Google Play Store datasets.
"""

import pandas as pd
import numpy as np


def load_data(apps_path: str, reviews_path: str):
    apps = pd.read_csv(apps_path)
    reviews = pd.read_csv(reviews_path)
    return apps, reviews


def clean_apps(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Drop duplicates
    df.drop_duplicates(inplace=True)

    # Fix Rating column (remove invalid values > 5)
    df.loc[df['Rating'] > 5, 'Rating'] = np.nan

    # ---- FIX FOR INSTALLS COLUMN ----
    # Remove '+' and ',' then force numeric (bad values -> NaN)
    df['Installs'] = (
        df['Installs']
        .astype(str)
        .str.replace('+', '', regex=False)
        .str.replace(',', '', regex=False)
    )
    df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce')

    # Clean Price (remove $ and convert to float)
    df['Price'] = df['Price'].astype(str).str.replace('$', '', regex=False)
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce').fillna(0.0)

    # Convert Reviews to int
    df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce').fillna(0).astype(int)

    # Convert Size column to numeric MB
    def size_to_mb(x):
        if "M" in str(x):
            return float(str(x).replace("M", ""))
        elif "k" in str(x):
            return float(str(x).replace("k", "")) / 1024
        else:
            return np.nan

    df['Size_MB'] = df['Size'].apply(size_to_mb)

    return df


def clean_reviews(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # Drop rows with no sentiment
    df = df.dropna(subset=['Sentiment'])
    return df


def merge_data(apps: pd.DataFrame, reviews: pd.DataFrame) -> pd.DataFrame:
    # Aggregate review sentiment per app
    review_summary = reviews.groupby('App').agg({
        'Sentiment_Polarity': 'mean',
        'Sentiment_Subjectivity': 'mean',
        'Sentiment': lambda x: x.value_counts().idxmax() if not x.empty else None
    }).reset_index()

    # Merge with apps data
    merged = pd.merge(apps, review_summary, on='App', how='left')
    return merged


def full_pipeline(apps_path: str, reviews_path: str):
    apps, reviews = load_data(apps_path, reviews_path)
    apps_clean = clean_apps(apps)
    reviews_clean = clean_reviews(reviews)
    merged = merge_data(apps_clean, reviews_clean)
    return apps_clean, reviews_clean, merged


if __name__ == "__main__":
    # Example usage
    a, r, m = full_pipeline("googleplaystore.csv", "googleplaystore_user_reviews.csv")
    print("Apps:", a.shape, "Reviews:", r.shape, "Merged:", m.shape)
