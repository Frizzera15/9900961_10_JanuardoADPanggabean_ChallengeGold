import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import regex as re

# Filepath Shortcut
abusive_df = pd.read_csv('/Users/januardopanggabean/Python DB Latihan/BinarGoldChallengeBatch10/abusive.csv')
kamusalay_df = pd.read_csv('/Users/januardopanggabean/Python DB Latihan/BinarGoldChallengeBatch10/new_kamusalay.csv', encoding='latin=1')
data_df = pd.read_csv('/Users/januardopanggabean/Python DB Latihan/BinarGoldChallengeBatch10/data.csv', encoding='latin=1')

# Add new columns karena original df kamusalay tidak ada column header
kamusalay_df.columns = ['alayraw', 'alayfixed']

# Membuat DataFrame baru untuk menghindari perubahan data original
tweetcheck_df = pd.DataFrame(data_df['Tweet'])
# Prepare wordlists untuk bahan komparasi atas tiap entris dalam dataframe terhadap seluruh kata dalam 1 set list
abusewordlists = abusive_df['ABUSIVE'].to_list()
alayrawlists = kamusalay_df['alayraw'].to_list()
alaymodlists = kamusalay_df['alayfixed'].to_list()

# Cleansing kosakata 'USER' dari tweet
tweetcheck_df['Tweet'] = tweetcheck.df['Tweet'].apply(lambda nouser:re.sub(r'\bUSER\b', '', nouser, flags=re.IGNORECASE))


# Ini membuat column baru dengan fungsi tersendiri tanpa fungsi append
tweetcheck_df['contains_hatespeech'] = tweetcheck_df['Tweet'].apply(lambda Tweet: any(word in Tweet for word in abusewordlists))
tweetcheck_df['contains_alaywords'] = tweetcheck_df['Tweet'].apply(lambda Tweet: any(word in Tweet for word in alayrawlists))

# Hitung penggunaan kata abusive
abusive_counts = []

for abuseword in abusive_df['ABUSIVE']:
    countabuse = sum(1 for tweet in data_df['Tweet'] if abuseword in tweet)
    abusive_counts.append(countabuse)

abusive_df['Word_Count'] = abusive_counts

# abusive_df.to_csv('/Users/januardopanggabean/Python DB Latihan/BinarGoldChallengeBatch10/newabusestat.csv', index=False)

# Hitung penggunaan kata alay
alay_counts = []

for alayword in kamusalay_df['alayraw']:
    countalay = sum(1 for tweet in data_df['Tweet'] if alayword in tweet)
    alay_counts.append(countalay)

kamusalay_df['Word_Counts'] = alay_counts

# kamusalay_df.to_csv('/Users/januardopanggabean/Python DB Latihan/BinarGoldChallengeBatch10/alaytest.csv', index=False)


print(tweetcheck_df )