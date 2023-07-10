import sqlite3
from sqlite3 import Cursor

conn = sqlite3.connect('data/test.db', check_same_thread=False)

def create_table():
    conn.execute(f"""CREATE TABLE IF NOT EXISTS tweet_cleaning (id INTEGER PRIMARY KEY AUTOINCREMENT, original_tweet char(1000), cleaned_new_tweet char(1000))""")
    conn.commit()

def insert_to_table(value_1, value_2, table_name):
    value_1 = value_1.encode('utf-8')
    value_2 = value_2.encode('utf-8')
    query = f"INSERT INTO tweet_cleaning (original_tweet, cleaned_new_tweet) VALUES (?, ?);"
    cursors = conn.execute(query, (value_1, value_2))
    conn.commit()

def read_table(target_index=None, target_keywords=None):
    if target_index == None and target_keywords is None:
        results = conn.execute(f'SELECT id, original_tweet, cleaned_new_tweet FROM tweet_cleaning;')
        results = [result for result in results]
        return results
    elif target_keywords is not None and target_index is None:
        results = conn.execute(f"SELECT id, original_tweet, cleaned_new_tweet FROM tweet_cleaning where original_tweet like '%{target_keywords}%';")
        results = [result for result in results]
        return results
    elif target_keywords is None and target_index is not None:
        results = conn.execute(f'SELECT id, original_tweet, cleaned_new_tweet FROM tweet_cleaning WHERE id = {target_index};')
        results = [result for result in results]
        return results[0]
