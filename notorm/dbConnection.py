import sqlite3

DB_PATH='./database/db2.sqlite'

conn = sqlite3.connect(DB_PATH,
                       timeout=5.0,
                       detect_types=0,
                       isolation_level='DEFERRED',
                       check_same_thread=True,
                       factory=sqlite3.Connection,
                       cached_statements=128,
                       uri=False)

cursor = conn.cursor()