import pandas as pd
import regex as re
import matplotlib.pyplot as mpl
import seaborn as sns

# Membuat filepath shortcut untuk 'Gold CHallenge Assets'
abusive_df = pd.read_csv('/Users/januardopanggabean/Python DB Latihan/BinarGoldChallengeBatch10/abusive.csv')
kamusalay_df = pd.read_csv('/Users/januardopanggabean/Python DB Latihan/BinarGoldChallengeBatch10/new_kamusalay.csv', encoding='latin=1')
goldchallenge_df = pd.read_csv('/Users/januardopanggabean/Python DB Latihan/BinarGoldChallengeBatch10/data.csv', encoding='latin=1')

# Menyiapkan kamus alay sebagai dictionary
kamusalay_df.columns = ['alayraw', 'alayfixed']
alay_dict = dict(zip(kamusalay_df['alayraw'], kamusalay_df['alayfixed']))
alayraw_list = kamusalay_df['alayraw'].to_list()
alayfixed_list = kamusalay_df['alayfixed'].to_list()
# print(alay_dict)

#menghilangkan duplikat terlebih dahulu
#goldchallenge_df = goldchallenge_df.drop_duplicates()

# review dataframe utama
goldchallenge_df.info()

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
def tweet_process(text):
    text = lower_process(text)
    text = censor_emails(text)
    text = punctuation_erase(text)
    text = phone_censor(text)
    text = omit_user(text)
    text = tweet_strip(text)
    return text

for idx, tweet in enumerate(tweet_list):
    cleaned_tweet = tweet_process(tweet)
    print(cleaned_tweet)

    if idx == 50:
        break

tweetcheck_df = pd.DataFrame(goldchallenge_df['Tweet'])
tweetcheck_df['Cleaned_Tweet'] = tweetcheck_df['Tweet'].apply(lambda x:tweet_process(x))

# tweetcheck_df.to_csv('/Users/januardopanggabean/Python DB Latihan/BinarGoldChallengeBatch10/goldv1.csv')

# assign column header dikarenakan abusive dataframe belum punya header
abusive_df.columns = ['abusive_words']

# Buat set kata abusive dari dataframe. Penggunaan set menghasilkan kosakata unique yang berguna dalam proses sweeping nanti
abusive_wordset = set(abusive_df['abusive_words'])
alay_wordset = set(kamusalay_df['alayraw'])

from tqdm import tqdm
# Fungsi deteksi kosakata di dataframe lain (Boolean)
#def dfwordset_check(text, words):
#    for word in words:
#        if re.search(r'\b' + re.escape(word) + r'\b', text, flags=re.IGNORECASE):
#            return True
#    return False
def dfwordset_check(text, words):
    compiled_patterns = [re.compile(r'\b' + re.escape(word) + r'\b', flags=re.IGNORECASE) for word in words]
    return any(pattern.search(text) for pattern in compiled_patterns)

tweetcheck_df['Abusive_Words_Present'] = tweetcheck_df['Cleaned_Tweet'].apply(lambda x: dfwordset_check(x, abusive_wordset))
#tweetcheck_df['Alay_Words_Present'] = tweetcheck_df['Tweet'].apply(lambda x: dfwordset_check(x, alay_wordset))

print(tweetcheck_df[['Cleaned_Tweet','Abusive_Words_Present']])







