from classifier.custom_classifier import run_custom, classify_emotions
from classifier.textblob_classifier import run_textblob
from classifier.utils import save_csv
from classifier.vader_classifier import run_vader
import pandas as pd


def run_classifiers(scrape_id):
    """Run vader, textblob and custom classifiers sequentially"""
    run_vader(scrape_id)
    run_textblob(scrape_id)
    # run_emotion(scrape_id)
    run_custom(scrape_id)

    return


def run_emotion(scrape_id):
    file_path = f"text_data/complete/{scrape_id}.csv"
    df = pd.read_csv(file_path)

    # emo
    if 'emotion_label' not in df:
        df = classify_emotions(df)

    print('finished emotion')
    save_csv(df, f"text_data/emotion/{scrape_id}.csv")

    print(f"emotion for {scrape_id} complete")

    return df
