import sqlite3


connect = sqlite3.connect("database.db")
cursor = connect.cursor()

table = """
create table user(
      firstname varchar(100),
      familyname varchar(100),
      gender varchar(100),
      city varchar(100),
      country varchar(100),
      email varchar(100)
);
"""

cursor.execute(table)


rows = [
    ("Jack", "Reacher", "Male", "LA", "USA", "JackR@gmail.com"),
    ("Emily", "Blunt", "Female", "New York", "USA", "EmilyB@gmail.com"),
    ("Michael", "Smith", "Male", "Chicago", "USA", "MichaelS@gmail.com"),
    ("Sophia", "Johnson", "Female", "Houston", "USA", "SophiaJ@gmail.com"),
    ("James", "Brown", "Male", "Phoenix", "USA", "JamesB@gmail.com"),
    ("Olivia", "Williams", "Female", "Philadelphia", "USA", "OliviaW@gmail.com"),
    ("David", "Jones", "Male", "San Antonio", "USA", "DavidJ@gmail.com"),
    ("Isabella", "Miller", "Female", "San Diego", "USA", "IsabellaM@gmail.com"),
    ("John", "Davis", "Male", "Dallas", "USA", "JohnD@gmail.com"),
    ("Mia", "Garcia", "Female", "San Jose", "USA", "MiaG@gmail.com"),
    ("Ethan", "Martinez", "Male", "Austin", "USA", "EthanM@gmail.com")
]

cursor.executemany("INSERT INTO user VALUES (?, ?, ?, ?, ?, ?)", rows)


connect.commit()
connect.close()
