import codecs
import re
import string

from nltk import RegexpTokenizer, PorterStemmer, WordNetLemmatizer
from numpy import clip
from transformers import pipeline

from classifier.utils import load_model, get_dataframe_from_scrape_id, save_csv, load_vectorizer, add_to_compilation

lr_model = load_model()
vectorizer = load_vectorizer()


def run_custom(scrape_id):
    """Logistic Regression model with 83% accuracy"""
    df = get_dataframe_from_scrape_id(scrape_id)

    if df.empty:
        print('empty dataframe, exiting classifier')
        return

    # data cleaning to match expected
    df_predict = df.copy(deep=True)
    df_predict = clean_data(df_predict)

    # df['lr_sentiment'] = lr_model.predict(df_predict)
    lr_sentiment = lr_model.predict(df_predict)
    # print(f"lr sentiment len {len(lr_sentiment)}, df items {df.count()}")
    # print(lr_sentiment, df)

    df['lr_sentiment'] = lr_sentiment
    # print(df_predict.columns)
    # df['emotion_label'] = df_predict['emotion_label']
    # df['emotion_score'] = df_predict['emotion_score']
    if 'emotion_label' not in df:
        df = classify_emotions(df)
    print(df.columns)

    df = calculate_score(df)

    # df['topic'] = df['text'].apply(lambda x:)
    df['text'] = df['text'].apply(
        lambda x: codecs.escape_decode(bytes(x[2:-1], "utf-8"))[0].decode("utf-8"))

    complete_path = f"text_data/complete/{scrape_id}.csv"
    save_csv(df, complete_path)
    add_to_compilation(df)

    print("custom complete")

    return


def calculate_score(dataset):
    # dataset['score'] = dataset['v_sentiment_polarity'] + dataset['t_sentiment_polarity']
    # # Clip the values to the range of -1 to 1
    # dataset['score'] = dataset['score'].clip(lower=-1, upper=1)
    dataset['score'] = clip(dataset['v_sentiment_polarity'] + dataset['t_sentiment_polarity'], -1, 1)

    return dataset


stopwordlist = ['a', 'about', 'above', 'after', 'again', 'ain', 'all', 'am', 'an',
                'and', 'any', 'are', 'as', 'at', 'be', 'because', 'been', 'before',
                'being', 'below', 'between', 'both', 'by', 'can', 'd', 'did', 'do',
                'does', 'doing', 'down', 'during', 'each', 'few', 'for', 'from',
                'further', 'had', 'has', 'have', 'having', 'he', 'her', 'here',
                'hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 'if', 'in',
                'into', 'is', 'it', 'its', 'itself', 'just', 'll', 'm', 'ma',
                'me', 'more', 'most', 'my', 'myself', 'now', 'o', 'of', 'on', 'once',
                'only', 'or', 'other', 'our', 'ours', 'ourselves', 'out', 'own', 're', 's', 'same', 'she', "shes",
                'should', "shouldve", 'so', 'some', 'such',
                't', 'than', 'that', "thatll", 'the', 'their', 'theirs', 'them',
                'themselves', 'then', 'there', 'these', 'they', 'this', 'those',
                'through', 'to', 'too', 'under', 'until', 'up', 've', 'very', 'was',
                'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom',
                'why', 'will', 'with', 'won', 'y', 'you', "youd", "youll", "youre",
                "youve", 'your', 'yours', 'yourself', 'yourselves']
STOPWORDS = set(stopwordlist)


def cleaning_stopwords(text):
    return " ".join([word for word in str(text).split() if word not in STOPWORDS])


english_punctuations = string.punctuation
punctuations_list = english_punctuations


def cleaning_punctuations(text):
    translator = str.maketrans('', '', punctuations_list)
    return text.translate(translator)


def cleaning_repeating_char(text):
    return re.sub(r'(.)1+', r'1', text)


def clean_repeating_words(text):
    # Use regular expression to find consecutive duplicate words
    pattern = r'\b(\w+)( \1\b)+'
    # Use re.sub to replace duplicate words with a single occurrence
    cleaned_text = re.sub(pattern, r'\1', text)
    return cleaned_text


def cleaning_URLs(data):
    return re.sub('((www.[^s]+)|(https?://[^s]+))', ' ', data)


def cleaning_numbers(data):
    return re.sub('[0-9]+', '', data)


tokenizer = RegexpTokenizer(r'\w+')

st = PorterStemmer()


def stemming_on_text(data):
    text = [st.stem(word) for word in data]
    return data


lm = WordNetLemmatizer()


def lemmatizer_on_text(data):
    text = [lm.lemmatize(word) for word in data]
    return data


def remove_usernames(text):
    # Use regular expression to find and remove usernames
    pattern = r'@\w+'
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text


def clean_data(dataset):
    dataset['text'] = dataset['text'].apply(lambda text: cleaning_stopwords(text))
    # dataset['text'].head()

    dataset['text'] = dataset['text'].apply(lambda x: cleaning_punctuations(x))

    dataset['text'] = dataset['text'].apply(lambda x: cleaning_repeating_char(x))

    dataset['text'] = dataset['text'].apply(lambda x: cleaning_URLs(x))

    dataset['text'] = dataset['text'].apply(lambda x: cleaning_numbers(x[1:]))

    # dataset = classify_emotions(dataset)
    # print(dataset.tail())

    dataset['text'] = dataset['text'].apply(tokenizer.tokenize)

    dataset['text'] = dataset['text'].apply(lambda x: stemming_on_text(x))

    dataset['text'] = dataset['text'].apply(lambda x: lemmatizer_on_text(x))

    # join the arrays into strings
    dataset['text'] = dataset['text'].apply(lambda x: ' '.join(x))

    dataset = vectorizer.transform(dataset['text'])

    return dataset


model = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")


def classify_emotions(dataset):
    print('classifying emotions')
    # df = dataset.copy(deep=True)
    # df['text'] = df['text'].apply(tokenizer.tokenize)
    all_texts = dataset['text'].apply(lambda x:
                                      cleaning_numbers(
                                          cleaning_URLs(
                                              cleaning_punctuations(
                                                  cleaning_stopwords(
                                                      clean_repeating_words(
                                                          remove_usernames(x))))))).tolist()
    # print(all_texts)
    print('list')
    all_emotions = model(all_texts)
    print('after run emo model')
    print(all_emotions)
    dataset['emotion_score'] = [d['score'] for d in all_emotions]
    dataset['emotion_label'] = [d['label'] for d in all_emotions]
    # print(dataset.columns)
    return dataset

# def get_emotion_info(text_item):
#     """second emo classifier, takes long"""
#     emotion = LeXmo.LeXmo(text_item)
#     print(emotion)
#     emotion.pop('text', None)
#     return emotion
