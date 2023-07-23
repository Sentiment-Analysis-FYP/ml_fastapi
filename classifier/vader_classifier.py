import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def run_vader(scrape_id):
    df = get_dataframe_from_scrape_id(scrape_id)
    sentiment_analyzer = SentimentIntensityAnalyzer()

    df['sentiment_neg'] = df['full_text'].apply(
        lambda txt: sentiment_analyzer.polarity_scores(str(txt))['neg'])

    df['sentiment_pos'] = df['full_text'].apply(
        lambda txt: sentiment_analyzer.polarity_scores(str(txt))['pos'])

    df['sentiment_compound'] = df['full_text'].apply(
        lambda txt: sentiment_analyzer.polarity_scores(str(txt))['compound'])

    return
