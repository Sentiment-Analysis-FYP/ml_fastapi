import re
import string

from nltk import RegexpTokenizer, PorterStemmer, WordNetLemmatizer

from classifier.utils import load_model, get_dataframe_from_scrape_id, save_csv, load_vectorizer


def run_custom(scrape_id):
    """Logistic Regression model with 83% accuracy"""
    lr_model = load_model()
    df = get_dataframe_from_scrape_id(scrape_id)

    # data cleaning to match expected
    df_clean = df.copy(deep=True)
    df_clean = clean_data(df_clean)

    # df['lr_sentiment'] = lr_model.predict(df['text'])

    complete_path = f"text_data/complete/{scrape_id}.csv"
    save_csv(df, complete_path)

    print("custom complete")

    return


def clean_data(dataset):
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

    dataset['text'] = dataset['text'].apply(lambda text: cleaning_stopwords(text))
    # dataset['text'].head()

    english_punctuations = string.punctuation
    punctuations_list = english_punctuations

    def cleaning_punctuations(text):
        translator = str.maketrans('', '', punctuations_list)
        return text.translate(translator)

    dataset['text'] = dataset['text'].apply(lambda x: cleaning_punctuations(x))

    def cleaning_repeating_char(text):
        return re.sub(r'(.)1+', r'1', text)

    dataset['text'] = dataset['text'].apply(lambda x: cleaning_repeating_char(x))

    def cleaning_URLs(data):
        return re.sub('((www.[^s]+)|(https?://[^s]+))', ' ', data)

    dataset['text'] = dataset['text'].apply(lambda x: cleaning_URLs(x))

    def cleaning_numbers(data):
        return re.sub('[0-9]+', '', data)

    dataset['text'] = dataset['text'].apply(lambda x: cleaning_numbers(x))

    tokenizer = RegexpTokenizer(r'\w+')
    dataset['text'] = dataset['text'].apply(tokenizer.tokenize)

    st = PorterStemmer()

    def stemming_on_text(data):
        text = [st.stem(word) for word in data]
        return data

    dataset['text'] = dataset['text'].apply(lambda x: stemming_on_text(x))

    lm = WordNetLemmatizer()

    def lemmatizer_on_text(data):
        text = [lm.lemmatize(word) for word in data]
        return data

    dataset['text'] = dataset['text'].apply(lambda x: lemmatizer_on_text(x))

    vectorizer = load_vectorizer()

    dataset = vectorizer.transform(dataset)

    return dataset
