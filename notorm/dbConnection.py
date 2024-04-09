import sqlite3
import os

DB_PATH=os.environ['DB_PATH'] #'./database/db2.sqlite'

print(DB_PATH)
conn = sqlite3.connect(DB_PATH,
                       timeout=5.0,
                       detect_types=0,
                       isolation_level='DEFERRED',
                       check_same_thread=True,
                       factory=sqlite3.Connection,
                       cached_statements=128,
                       uri=False)

cursor = conn.cursor()