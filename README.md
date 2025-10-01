# Google-playstore-apps
📊 Google Play Store Apps Analysis

This project analyzes Google Play Store applications using two datasets:
googleplaystore.csv → app metadata (category, installs, rating, size, price, etc.)
googleplaystore_user_reviews.csv → user reviews + sentiment scores
The project is built in Python and produces data insights, plots, and CSV reports.

📁 Project Structure
google-play-analysis/
│── data_processing.py   # Load + clean data
│── analysis.py          # Exploratory analysis & plots
│── run.py               # Main script (pipeline)
│── requirements.txt     # Dependencies
│── googleplaystore.csv  # Dataset 1
│── googleplaystore_user_reviews.csv  # Dataset 2
│── outputs/             # Generated plots & reports
│   ├── plots/
│   └── reports/

▶️ Usage
Run the pipeline with:
python run.py --apps googleplaystore.csv --reviews googleplaystore_user_reviews.csv --out outputs

📊 Features

Data Cleaning
Fix invalid ratings
Convert installs, reviews, price, size into numeric values
Drop duplicates & handle missing values
Exploratory Data Analysis
App rating distribution
Top categories by number of apps
Free vs Paid breakdown
Sentiment distribution of reviews

Outputs

PNG plots (outputs/plots/)
CSV summary reports (outputs/reports/)
