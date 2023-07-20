import tweepy


async def run_scrape(scrape_id: str, data: dict):
    return


def get_tweets(keywords, start_date, end_date):
    consumer_key = 'YOUR_CONSUMER_KEY'
    consumer_secret = 'YOUR_CONSUMER_SECRET'
    access_token = 'YOUR_ACCESS_TOKEN'
    access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True)

    try:
        # Format the query with multiple keywords joined by OR
        query = ' OR '.join(keywords)

        # Fetch tweets based on the query and date range
        tweets = tweepy.Cursor(api.search, q=query, lang='en', tweet_mode='extended', since=start_date,
                               until=end_date).items()

        result = []
        for tweet in tweets:
            result.append(tweet._json)

        return result

    except tweepy.TweepError as e:
        print("Error occurred during the search:", e)
        return []
