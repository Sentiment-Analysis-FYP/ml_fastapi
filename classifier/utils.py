import pandas as pd
from joblib import load

from classifier.custom_classifier import run_custom
from classifier.textblob_classifier import run_textblob
from classifier.vader_classifier import run_vader


def load_model():
    model = load('logisticregression.joblib')
    return model


def remove_user_handles(txt):
    return ' '.join(word for word in txt.split(' ') if not word.startswith('@'))


def format_output(output_dict):
    polarity = "neutral"

    if output_dict['compound'] >= 0.05:
        polarity = "positive"

    elif output_dict['compound'] <= -0.05:
        polarity = "negative"

    return polarity


def save_as_json(dataframe, new_file_name):
    out = dataframe.to_json(orient='records', force_ascii=False)[1:-1]
    out = '[' + out + ']'

    with open(new_file_name + '.json', 'w', encoding='utf-8') as f:
        f.write(out)
    # dataframe.to_json(new_file_name + '.json', orient='records', lines=True)
    return


def save_csv(dataframe, file_name):
    dataframe.to_csv(file_name, encoding='utf-8', index=False)
    return


def get_dataframe_from_scrape_id(scrape_id):
    file_path = f"text_data/incomplete/{scrape_id}.csv"
    df = pd.read_csv(file_path)

    # cleaning dataframe
    df['text'] = df['text'].apply(lambda t: remove_user_handles(t))
    df['created_at'] = pd.to_datetime(df['created_at']).apply(lambda d: d.date())

    return df


def run_classifiers(scrape_id):
    """Run vader, textblob and custom classifiers sequentially"""
    run_vader(scrape_id)
    run_textblob(scrape_id)
    run_custom(scrape_id)

    return
