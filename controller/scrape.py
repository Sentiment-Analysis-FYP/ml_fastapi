import os

import tweepy
from dotenv import load_dotenv


async def run_scrape(data: dict):
    keywords = data['keywords']
    start_date = data['start_date']
    end_date = data['end_date']
    # print(keywords)
    scrape = await get_tweets(keywords, start_date, end_date)
    return scrape


def load_api_keys():
    load_dotenv()
    consumer_key = os.getenv('TWITTER_API_KEY')
    consumer_secret = os.getenv('TWITTER_API_SECRET')
    access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
    return consumer_key, consumer_secret, access_token, access_token_secret, bearer_token


async def get_tweets(keywords: list, start_date, end_date):
    consumer_key, consumer_secret, access_token, access_token_secret, bearer_token = load_api_keys()

    client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)

    result = []
    query = ' OR '.join(keywords)
    print(query)

    for tweet in tweepy.Paginator(client.search_recent_tweets, query=f"({query}) lang=en",
                                  user_fields=['username', 'name'], expansions=['author_id'],
                                  tweet_fields=['created_at', 'text'], max_results=10).flatten(limit=10):
        if not tweet.text.startswith("RT @"):
            result.append(tweet)

    return result
