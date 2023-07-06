pip install pandas
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
################################################################
# join dengan spasi menjadi 1 string besar
all_tweet = " ".join(tweetcheck_df['Tweet'].astype(str))

words = all_tweet.split()

word_counts = pd.Series(words).value_counts()

df_word_counts = pd.DataFrame({'Words': word_counts.index,'Counts': word_counts.values} )

print(word_counts)
# df_word_counts.to_csv('/Users/januardopanggabean/Python DB Latihan/BinarGoldChallengeBatch10/hitungkatachallenge.csv', index=False)

# dictionary of alayword
alay_dict = dict(zip(kamusalay_df['alayraw'], kamusalay_df['alayfixed']))

#define replace alay word function
def replace_alay(tweet):
    words = tweet.split()
    revised_alay = [alay_dict.get(word, word)for word in words]
    revised_tweet = " ".join(revised_alay)
    return revised_tweet

tweetcheck_df['Tweet Revisi Alay'] = tweetcheck_df['Tweet'].apply(replace_alay)

tweetcheck_df.to_csv('/Users/januardopanggabean/Python DB Latihan/BinarGoldChallengeBatch10/TweetGakAlay.csv', index=False)

print(alay_dict)

###################################################################
#penetapan pattern dulu
#user_pattern = r'\bUSER\b'

# fungsi khusus
#def replace_user(match):
 #   return "ALDI TAHER GALLAGHER"
# Cleansing kosakata 'USER' dari tweet
#tweetcheck_df['Tweet'] = tweetcheck_df['Tweet'].apply(lambda nouser:re.sub(user_pattern,replace_user, nouser, flags=re.IGNORECASE))

# tweetcheck_df.to_csv('/Users/januardopanggabean/Python DB Latihan/BinarGoldChallengeBatch10/sulapaldi.csv', index=False)

#test_df = pd.DataFrame({"Entries" : ["nomor saya 0212345467",
                                    # "ini telp saya 0219876576",
                                    # "hubungi di 0216789765"
                                    # ]})

#telp_pattern = r'(\d{3})(\d+)'

#test_df["NomorBaru"] = test_df["Entries"].apply(lambda nobaru: re.sub(telp_pattern,r'\1+\2', nobaru,))

#print(test_df)