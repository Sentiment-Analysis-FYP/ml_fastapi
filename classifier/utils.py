import os
import sys

import pandas as pd
from joblib import load


def load_model():
    model = load('classifier/logisticregression.joblib')
    return model


def load_vectorizer():
    vectorizer = load('classifier/vectorizer.pkl')
    return vectorizer


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


def add_to_compilation(dataframe):
    """Add a newly analyzed scrape to the compilation csv"""
    file_path = f"text_data/compilation/compilation.csv"

    if not os.path.isfile(file_path):
        dataframe.to_csv(file_path, index=False, encoding='utf-8')
    else:  # else it exists so append without writing the header
        dataframe.to_csv(file_path, mode='a', header=False, index=False, encoding='utf-8')
    # dataframe.to_csv(file_path, mode='a', header=False)

    return


def get_compilation():
    """Get the compilation csv (for sending)"""
    file_path = f"text_data/compilation/compilation.csv"

    return
