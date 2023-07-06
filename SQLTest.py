import sqlite3
conn = sqlite3.connect('/Users/januardopanggabean/PycharmProjects/BinarGoldChallenge10Januardo/data_pokemon.db')

conn.execute("DROP TABLE IF EXISTS users")

conn.execute("""
CREATE TABLE users (username varchar(255), email varchar(255))
""")
print("Table has created successfully")


conn.execute("INSERT INTO users (username, email) VALUES ('Januardo', 'januardo@binar.com')")
conn.execute("INSERT INTO users (username, email) VALUES ('Dea', 'dea@binar.com')")
conn.commit()
print("Records has been updated")

print("list of users")
cursor = conn.execute("select * from users;")
for row in cursor:
    print(row)

