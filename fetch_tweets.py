import os
from datetime import datetime
import logging
from pytz import timezone
import pandas as pd
from dotenv import load_dotenv
import tweepy

logging.basicConfig(level=logging.INFO)

def main():
    keyword = 'hogehoge'
    api = init_twitter_api()
    tw_data = fetch_tweets(api, keyword, max_results=100)
    save_to_csv(tw_data)

def init_twitter_api():
    # Load environment variables
    load_dotenv()

    # Fetch Twitter API credentials from environment variables
    API_KEY = os.getenv("TWITTER_API_KEY")
    API_SECRET = os.getenv("TWITTER_API_SECRET")
    ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

    # Validate API credentials
    if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET]):
        logging.error("Environment variables for Twitter API are not set properly.")
        raise ValueError("API credentials missing.")

    # Set up authentication for Twitter API
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit = True)

    return api

def fetch_tweets(api, keyword, max_results):
    try:
        tw_data = []
        # Search for tweets using the given keyword
        tweets = tweepy.Cursor(api.search_tweets, q=keyword, lang='ja', tweet_mode="extended").items(max_results)
        created_at = datetime.now(timezone('UTC'))
        for tweet in tweets:
            # Extract data from each tweet
            row = [
                tweet.id, tweet.created_at, tweet.full_text,
                tweet.favorite_count, tweet.retweet_count, tweet.user.screen_name,
                tweet.user.name, tweet.user.friends_count, tweet.user.followers_count,
                tweet.user.created_at, created_at
            ]
            tw_data.append(row)
    except tweepy.TweepError as e:
        # Handle possible TweepError
        logging.error(f"Error occurred while fetching tweets: {e}")

    return tw_data

def save_to_csv(data):
    # Define column names for the CSV
    LABELS = [
        'tweet_id', 'tweet_time', 'tweet_text', 'favorite_cnt',
        'retweet_cnt', 'user_id', 'account_name', 'follow',
        'follower', 'account_start', 'created_at'
    ]

    # Generate file name
    now = datetime.now()
    file_name = 'tweet_data_{}.csv'.format(now.strftime('%Y_%m_%d_%H_%M_%S'))

    # Convert data to a DataFrame and save to a CSV file
    df = pd.DataFrame(data, columns=LABELS)
    df.to_csv(file_name, encoding='utf-8-sig', index=False)

    logging.info(f'Data saved to {file_name}')

if __name__ == '__main__':
    main()
