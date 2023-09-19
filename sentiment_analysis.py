import os
from datetime import datetime
import logging
import requests
import pandas as pd
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

def main():
    url, df = load_gcp_config_and_data()
    update_dataframe_with_sentiment(df, url)
    save_to_csv(df)

def load_gcp_config_and_data():
    # Load environment variables
    load_dotenv()

    # Fetch GCP API key and CSV path from environment variables
    key = os.getenv("GCP_API_KEY")
    csv_path = os.getenv("CSV_PATH")

    # Validate environment variable values
    if not key or not csv_path:
        logging.error("Required environment variables for GCP are not set properly.")
        raise ValueError("load missing.")

    # Create API URL
    url = f'https://language.googleapis.com/v1beta2/documents:analyzeSentiment?key={key}'

    # Load data from the specified CSV path
    df = pd.read_csv(csv_path, index_col=None, header=0)

    return url, df

def sentiment_analyse(text, url):
    header = {'Content-Type' : 'application/json'}
    body = {
        "document":{
            "type":"PLAIN_TEXT",
            "language":"JA",
            "content":text
        }
    }

    try:
        # Request sentiment analysis
        response = requests.post(url, headers=header, json=body).json()
        score = response.get("documentSentiment", {}).get("score")
        magnitude = response.get("documentSentiment", {}).get("magnitude")

        # Validate response values
        if score is None or magnitude is None:
            logging.error(f"Unexpected API response: {response}")
            return None, None

        return score, magnitude

    except requests.RequestException as e:
        logging.error(f"Error occurred while fetching sentiment analysis: {e}")
        return None, None


def update_dataframe_with_sentiment(df, url):
    score_list = []
    magnitude_list = []

    for tweet in df['tweet_text']:
        score, magnitude = sentiment_analyse(tweet, url)
        score_list.append(score)
        magnitude_list.append(magnitude)

    df['score'] = score_list
    df['magnitude'] = magnitude_list

def save_to_csv(df):
    # Generate file name
    now = datetime.now()
    file_name = 'tweet_sentiment_{}.csv'.format(now.strftime('%Y_%m_%d_%H_%M_%S'))

    # Save to a CSV file
    df.to_csv(file_name, encoding='utf-8-sig', index=False)

    logging.info(f'Data saved to {file_name}')

if __name__ == '__main__':
    main()
