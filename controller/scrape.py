import os

from tweepy import API, OAuthHandler, Cursor
from dotenv import load_dotenv


async def run_scrape(scrape_id: str, data: dict):
    return


def load_api_keys():
    load_dotenv('../.env')
    consumer_key = os.getenv('CONSUMER_KEY')
    consumer_secret = os.getenv('CONSUMER_SECRET')
    access_token = os.getenv('ACCESS_TOKEN')
    access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
    return consumer_key, consumer_secret, access_token, access_token_secret


def get_tweets(keywords, start_date, end_date):
    consumer_key, consumer_secret, access_token, access_token_secret = load_api_keys()

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = API(auth, wait_on_rate_limit=True)

    try:
        # Format the query with multiple keywords joined by OR
        query = ' OR '.join(keywords)

        # Fetch tweets based on the query and date range
        tweets = Cursor(api.search_tweets, q=query, lang='en', tweet_mode='extended', since=start_date,
                        until=end_date).items()

        result = []
        for tweet in tweets:
            result.append(tweet.full_text)

        return result

    except Exception as e:
        print("Error occurred during the search:", e)
        return []
