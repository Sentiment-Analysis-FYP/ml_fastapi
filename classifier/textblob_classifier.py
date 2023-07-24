from classifier.utils import get_dataframe_from_scrape_id, save_csv
from textblob import TextBlob


def run_textblob(scrape_id):
    df = get_dataframe_from_scrape_id(scrape_id)

    df['t_sentiment_polarity'] = df['text'].apply(
        lambda t: TextBlob(t).sentiment.polarity)

    df['t_sentiment_subjectivity'] = df['text'].apply(
        lambda t: TextBlob(t).sentiment.subjectivity)

    save_csv(df, f"text_data/incomplete/{scrape_id}.csv")

    return
