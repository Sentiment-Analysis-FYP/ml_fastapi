import os

import tweepy
import csv
from dotenv import load_dotenv

MAX_RESULTS = 10
FLATTEN_LIMIT = 2


async def run_scrape(data: dict, scrape_id):
    username = data['username']
    keywords = data['keywords']
    start_date = data['start_date']
    end_date = data['end_date']
    # print(keywords)
    scrape = await get_tweets(scrape_id, username, keywords, start_date, end_date)
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


async def get_tweets(scrape_id: str, username: str, keywords: list, start_date, end_date):
    """2-step function to get tweets based on provided username, and then based on the other parameters"""

    result = []
    query = ' OR '.join(keywords)
    print(query)

    csv_file = open(f"text_data/incomplete/{scrape_id}.csv", 'w')
    csv_writer = csv.writer(csv_file)

    paginator = tweepy.Paginator(client.search_recent_tweets,
                                 query=f"({query}) lang=en",
                                 user_fields=['username', 'name'],
                                 expansions='author_id',
                                 tweet_fields=['id', 'author_id', 'created_at', 'text'],
                                 max_results=MAX_RESULTS,
                                 limit=FLATTEN_LIMIT)

    for response in paginator:
        # print(f"{response.data}".encode('utf-8'))
        users = response.includes.get('users')
        # print(len(users))
        # print(f"{users}".encode('utf-8'))
    # for tweet in tweepy.Paginator(client.search_recent_tweets,
    #                                  query=f"({query}) lang=en",
    #                                  user_fields=['username', 'name'],
    #                                  expansions=['author_id'],
    #                                  tweet_fields=['id', 'author_id', 'created_at', 'text'],
    #                                  max_results=MAX_RESULTS) \
    #            .flatten(limit=FLATTEN_LIMIT):
    #        # if not tweet.text.startswith("RT @"):
    #        result.append(tweet)
    #        csv_writer.writerow([tweet.id, tweet.created_at, tweet.text.encode('utf-8'), tweet.user.screen_name])

    if not username:
        return result

    # username provided
    user_id = await get_user_id(username)
    # for tweet in tweepy.Paginator(client.get_users_tweets, id=user_id, max_results=MAX_RESULTS) \
    #         .flatten(limit=FLATTEN_LIMIT):
    #     result.append(tweet)

    username_paginator = tweepy.Paginator(client.get_users_tweets, id=user_id, max_results=MAX_RESULTS)

    for response in username_paginator:
        tweets = response.data
        users = response.includes['users']
        users = {user["id"]: user for user in users}
        # print(f"{users}".encode('utf-8'))

        for tweet in tweets:
            author = users[tweet.author_id]
            print(f"The tweet {tweet.id} was written by {author.username}.")
            csv_writer.writerow([tweet.id, tweet.created_at, tweet.text.encode('utf-8'), author.username])

    return result
