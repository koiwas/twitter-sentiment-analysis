# [LEGACY] twitter-sentiment-analysis

***Note***: *This repository contains legacy code for fetching tweets and performing sentiment analysis on them.
Due to changes in Twitter's policies and APIs, the current implementation might not be functional.*

## Structure

- fetch_tweets.py - Script for fetching tweets based on a given keyword.
- sentiment_analysis.py - Script for performing sentiment analysis on tweets.
- requirements.txt - List of Python libraries required. Install them using pip install -r requirements.txt.
- .env - File to store environment variables. (Do not include the actual .env file in the repository for security reasons.)

## Prerequisites

- Python 3.7+
- Libraries: os, datetime, logging, pandas, dotenv, tweepy, requests, pytz
- Twitter API credentials (TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
- Google Cloud Natural Language API Key (for sentiment analysis)
- .env file with the necessary environment variables set.
