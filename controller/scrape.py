import os

import tweepy
from dotenv import load_dotenv

MAX_RESULTS = 100
FLATTEN_LIMIT = 300


async def run_scrape(data: dict):
    username = data['username']
    keywords = data['keywords']
    start_date = data['start_date']
    end_date = data['end_date']
    # print(keywords)
    scrape = await get_tweets(username, keywords, start_date, end_date)
    return scrape


def load_api_keys():
    load_dotenv()
    consumer_key = os.getenv('TWITTER_API_KEY')
    consumer_secret = os.getenv('TWITTER_API_SECRET')
    access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
    return consumer_key, consumer_secret, access_token, access_token_secret, bearer_token


def get_tweepy_client():
    consumer_key, consumer_secret, access_token, access_token_secret, bearer_token = load_api_keys()

    return tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)


client = get_tweepy_client()


async def get_user_id(screen_name: str):
    print("The screen name is: " + screen_name)
    user = client.get_user(username=screen_name)
    # print(user)
    return user.data.id


async def get_tweets(username: str, keywords: list, start_date, end_date):
    """2-step function to get tweets based on provided username, and then based on the other parameters"""

    result = []
    query = ' OR '.join(keywords)
    print(query)

    for tweet in tweepy.Paginator(client.search_recent_tweets, query=f"({query}) lang=en",
                                  user_fields=['username', 'name'], expansions=['author_id'],
                                  tweet_fields=['created_at', 'text'], max_results=MAX_RESULTS) \
            .flatten(limit=FLATTEN_LIMIT):
        # if not tweet.text.startswith("RT @"):
        result.append(tweet)

    if not username:
        return result

    # username provided
    user_id = await get_user_id(username)
    for tweet in tweepy.Paginator(client.get_users_tweets, id=user_id, max_results=MAX_RESULTS) \
            .flatten(limit=FLATTEN_LIMIT):
        result.append(tweet)

    return result
