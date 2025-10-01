"""
run.py
Main script to run full pipeline:
  - loads the two CSVs
  - cleans them
  - aggregates/merges
  - runs EDA and saves outputs
Usage:
  python run.py --apps googleplaystore.csv --reviews googleplaystore_user_reviews.csv --out outputs
"""

import argparse
import os
from data_processing import full_pipeline
from analysis import run_all
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def main(apps_csv: str, reviews_csv: str, outdir: str):
    if not os.path.exists(apps_csv):
        raise FileNotFoundError(f"Apps CSV not found: {apps_csv}")
    if not os.path.exists(reviews_csv):
        raise FileNotFoundError(f"Reviews CSV not found: {reviews_csv}")

    os.makedirs(outdir, exist_ok=True)
    logging.info("Starting full pipeline...")
    apps_clean, reviews_clean, merged = full_pipeline(apps_csv, reviews_csv)
    logging.info(f"Cleaned apps: {apps_clean.shape}, cleaned reviews: {reviews_clean.shape}, merged: {merged.shape}")

    run_all(apps_clean, reviews_clean, merged, outputs_dir=outdir)
    logging.info("Pipeline finished. Outputs are in: %s", outdir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Google Play Store EDA pipeline")
    parser.add_argument("--apps", required=True, help="Path to googleplaystore.csv")
    parser.add_argument("--reviews", required=True, help="Path to googleplaystore_user_reviews.csv")
    parser.add_argument("--out", default="outputs", help="Output directory for plots / csvs")
    args = parser.parse_args()
    main(args.apps, args.reviews, args.out)
