import os

import tweepy
from tweepy import API, OAuthHandler, Cursor
from dotenv import load_dotenv


async def run_scrape(data: dict):
    keywords, start_date, end_date = data
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


async def get_tweets(keywords, start_date, end_date):
    consumer_key, consumer_secret, access_token, access_token_secret, bearer_token = load_api_keys()

    # auth = OAuthHandler(consumer_key, consumer_secret)
    # auth.set_access_token(access_token, access_token_secret)
    # api = API(auth, wait_on_rate_limit=True)
    # client = tweepy.Client(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token,
    #                        access_token_secret=access_token_secret)
    client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)

    result = []
    query = ' OR '.join(keywords)
    #
    # try:
    #     # Format the query with multiple keywords joined by OR
    #
    #     # Fetch tweets based on the query and date range
    #     # tweets = Cursor(api.search_tweets, q=query, lang='en', tweet_mode='extended').items()
    #     tweets = client.search_recent_tweets(query=query, max_results=10)
    #     for tweet in tweets:
    #         result.append(tweet.full_text)
    #
    #     print(len(result))
    #
    # except Exception as e:
    #     print("Error occurred during the search:", e)
    #     return []

    # tweets = client.search_recent_tweets(query=query, max_results=100)

    for tweet in tweepy.Paginator(client.search_recent_tweets, query=f"{query} -filter:retweets lang:en",
                                  user_fields=['username', 'name'],
                                  tweet_fields=['created_at', 'text'], max_results=10).flatten(limit=10):
        result.append(tweet)

    # for tweet in tweets.data:
    #     result.append(tweet)
    #     print(tweet.text.encode("utf-8"))

    return result
