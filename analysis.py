"""
analysis.py
Basic analysis and plots for Google Play Store data.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def plot_rating_distribution(apps_df: pd.DataFrame, outpath: str):
    ensure_dir(outpath)
    plt.figure(figsize=(6, 4))
    sns.histplot(apps_df['Rating'].dropna(), bins=20, kde=True)
    plt.title("Distribution of App Ratings")
    plt.xlabel("Rating")
    plt.savefig(os.path.join(outpath, "rating_distribution.png"))
    plt.close()


def plot_apps_by_category(apps_df: pd.DataFrame, outpath: str, top_n: int = 10):
    ensure_dir(outpath)
    counts = apps_df['Category'].value_counts().head(top_n)
    plt.figure(figsize=(8, 5))
    sns.barplot(y=counts.index, x=counts.values)
    plt.title(f"Top {top_n} Categories by Number of Apps")
    plt.xlabel("Count")
    plt.savefig(os.path.join(outpath, "apps_by_category.png"))
    plt.close()


def plot_free_vs_paid(apps_df: pd.DataFrame, outpath: str):
    ensure_dir(outpath)
    plt.figure(figsize=(5, 4))
    sns.countplot(x='Type', data=apps_df)
    plt.title("Free vs Paid Apps")
    plt.savefig(os.path.join(outpath, "free_vs_paid.png"))
    plt.close()


def sentiment_distribution(reviews_df: pd.DataFrame, outpath: str):
    ensure_dir(outpath)
    plt.figure(figsize=(5, 4))
    sns.countplot(x='Sentiment', data=reviews_df)
    plt.title("Sentiment Distribution of Reviews")
    plt.savefig(os.path.join(outpath, "sentiment_distribution.png"))
    plt.close()


def export_summary(apps_df: pd.DataFrame, merged_df: pd.DataFrame, outdir: str):
    ensure_dir(outdir)
    # Top apps by installs
    apps_df[['App', 'Category', 'Installs', 'Rating']].sort_values(
        'Installs', ascending=False
    ).head(10).to_csv(os.path.join(outdir, "top_apps.csv"), index=False)

    # Category summary
    apps_df.groupby('Category').agg(
        app_count=('App', 'count'),
        avg_rating=('Rating', 'mean'),
        total_installs=('Installs', 'sum')
    ).sort_values('total_installs', ascending=False).to_csv(
        os.path.join(outdir, "category_summary.csv")
    )


def run_all(apps_df, reviews_df, merged_df, outputs_dir="outputs"):
    plots_dir = os.path.join(outputs_dir, "plots")
    reports_dir = os.path.join(outputs_dir, "reports")

    plot_rating_distribution(apps_df, plots_dir)
    plot_apps_by_category(apps_df, plots_dir)
    plot_free_vs_paid(apps_df, plots_dir)
    sentiment_distribution(reviews_df, plots_dir)
    export_summary(apps_df, merged_df, reports_dir)

    print("Analysis complete. Check the outputs folder.")
