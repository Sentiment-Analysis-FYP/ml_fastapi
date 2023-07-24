from classifier.utils import load_model, get_dataframe_from_scrape_id, save_csv


def run_custom(scrape_id):
    """Logistic Regression model with 83% accuracy"""
    lr_model = load_model()
    df = get_dataframe_from_scrape_id(scrape_id)
    df['lr_sentiment'] = lr_model.predict(df['text'])

    complete_path = f"text_data/complete/{scrape_id}.csv"
    save_csv(df, complete_path)
