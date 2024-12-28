import sqlite3
import json

conn = sqlite3.connect("community_issues.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()


for table in tables:
    print(table[0])

conn.close()