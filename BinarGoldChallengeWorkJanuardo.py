import pandas as pd
import regex as re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as mpl
import seaborn as sns

# Membuat filepath shortcut untuk 'Gold CHallenge Assets'
abusive_df = pd.read_csv('/Users/januardopanggabean/PycharmProjects/BinarGoldChallenge10Januardo/data/abusive.csv')
kamusalay_df = pd.read_csv('/Users/januardopanggabean/PycharmProjects/BinarGoldChallenge10Januardo/data/new_kamusalay.csv', encoding='latin=1')
goldchallenge_df = pd.read_csv('/Users/januardopanggabean/PycharmProjects/BinarGoldChallenge10Januardo/data/data.csv', encoding='latin=1')

# Menyiapkan kamus alay sebagai dictionary
kamusalay_df.columns = ['alayraw', 'alayfixed']
alay_dict = dict(zip(kamusalay_df['alayraw'], kamusalay_df['alayfixed']))
alayraw_list = kamusalay_df['alayraw'].to_list()
alayfixed_list = kamusalay_df['alayfixed'].to_list()

# review dataframe utama
#goldchallenge_df.info()

# Merubah entry Tweets dalam dataframe ke dalam list untuk manipulasi lebih lanjut
tweet_list = goldchallenge_df['Tweet'].tolist()

# Mengubah entry Tweets dalam dataframe dengan manipulasi pemisahan menjadi koleksi besar kosakata
all_tweet_words = " ".join(goldchallenge_df['Tweet'].astype(str))
tweet_words = all_tweet_words.split()



#### DATA CLEANSING AND REFORMATTING

# Melakukan koversi typeformat Tweets ke lowercase
# Perlu diingat bahwa list tidak bisa langsung diproses sehingga harus ditarik satu persatu melalui tweet in tweet_list
def lower_process(text):
    return text.lower()

# Sensor alamat email yang tercantum dalam Tweet di Dataframe
def censor_emails(text):
    return re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', 'EMAIL OMITTED', text)

# Eliminasi tanda baca
def punctuation_erase(text):
    return re.sub(r'[^\w\s]','',text)

# Sensor nomor telepon
def phone_censor(text):
    text = text.replace(" 62", " 0")
    text = re.sub(r"\b\d{4}\s?\d{4}\s?\d{4}\b", "PHONE OMITTED", text)
    return text

# Omit USER dari Tweets
def omit_user(text):
    return text.replace("user","")

# Strip blank spaces dari Tweet
def tweet_strip(text):
    return text.strip()



#### Menyatukan seluruh fungsi untuk 1 eksekusi yang lebih lengkap
def processing_text(text):
    text = lower_process(text)
    text = censor_emails(text)
    text = punctuation_erase(text)
    text = phone_censor(text)
    text = omit_user(text)
    text = tweet_strip(text)
    return text

#for idx, tweet in enumerate(tweet_list):
   # cleaned_tweet = processing_text(tweet)
   # print(cleaned_tweet)

   # if idx == 50:
    #    break

tweetcheck_df = pd.DataFrame(goldchallenge_df['Tweet'])
tweetcheck_df['Cleaned_Tweet_Text'] = tweetcheck_df['Tweet'].apply(lambda x:processing_text(x))

# tweetcheck_df.to_csv('/Users/januardopanggabean/Python DB Latihan/BinarGoldChallengeBatch10/goldv1.csv')

# assign column header dikarenakan abusive dataframe belum punya header
abusive_df.columns = ['abusive_words']

# Buat set kata abusive dari dataframe. Penggunaan set menghasilkan kosakata unique yang berguna dalam proses sweeping nanti
abusive_wordset = set(abusive_df['abusive_words'])
alay_wordset = set(kamusalay_df['alayraw'])


def processing_word(input_text):
    phase_one_text = []  # set up hasil proses fase 1 (Abusive Cleanse)
    phase_two_text = []  # set up hasil proses fase 2 (Alay Cleanse)
    text = input_text.split(" ")  # split input_text menjadi list of words
    for word in text:  # untuk setiap word in 'text'
        if word in abusive_wordset:  # check word di dalam list_of_abusive_words
            phase_one_text.append("ABUSEWORDDETECTED")
        else:
            phase_one_text.append(word)  # jika tidak ada, masukkan ke dalam list new_text

    for word in phase_one_text:
        if word in alay_dict:
            alayword = alay_dict[word]
            phase_two_text.append(alayword)
        else:
            phase_two_text.append(word)

    text = " ".join(phase_two_text)
    return text

#tweetcheck_df['Cleaned_Tweet_Whole'] = tweetcheck_df['Cleaned_Tweet_Text'].apply(lambda x:processing_word(x))
print(tweetcheck_df)

#tweetcheck_df.to_csv('/Users/januardopanggabean/PycharmProjects/BinarGoldChallenge10Januardo/data/tweetcheckmk2.csv', index=False)






