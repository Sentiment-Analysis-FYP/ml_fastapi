# import nltk
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
#
# import gensim
#
# nltk.download('punkt')
# nltk.download('stopwords')
#
#
# def preprocess_text(text):
#     stop_words = set(stopwords.words('english'))
#     words = word_tokenize(text.lower())
#     words = [word for word in words if word.isalpha() and word not in stop_words]
#     return words
#
#
# def create_lda_model(corpus, num_topics):
#     dictionary = gensim.corpora.Dictionary(corpus)
#     bow_corpus = [dictionary.doc2bow(doc) for doc in corpus]
#     lda_model = gensim.models.LdaModel(bow_corpus, num_topics=num_topics, id2word=dictionary, passes=10)
#     return lda_model
