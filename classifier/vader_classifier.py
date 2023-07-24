import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from classifier.utils import get_dataframe_from_scrape_id, save_csv


def run_vader(scrape_id):
    df = get_dataframe_from_scrape_id(scrape_id)
    sentiment_analyzer = SentimentIntensityAnalyzer()

    df['v_sentiment_neg'] = df['text'].apply(
        lambda txt: sentiment_analyzer.polarity_scores(str(txt))['neg'])

    df['v_sentiment_pos'] = df['text'].apply(
        lambda txt: sentiment_analyzer.polarity_scores(str(txt))['pos'])

    df['v_sentiment_polarity'] = df['text'].apply(
        lambda txt: sentiment_analyzer.polarity_scores(str(txt))['compound'])

    save_csv(df, f"text_data/incomplete/{scrape_id}.csv")

    print("vader complete")

    return
