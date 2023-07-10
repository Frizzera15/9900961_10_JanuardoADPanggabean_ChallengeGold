import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('all')

#Pembersihan Stopwords untuk mendapat kata yang lebih bersih
def remove_stopwords(text):
    nltk.download('all')
    stop_words = set(stopwords.words('indonesian'))
    indowords = word_tokenize(text, languange='indonesian')
    meaningful_word = [word for word in indowords if word.lower() not in stop_words]
    cleanedtext = " ".join(meaningful_word)

    return cleanedtext