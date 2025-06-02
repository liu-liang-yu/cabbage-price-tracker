import sqlite3

def insert_price(date, price):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO prices (date, price) VALUES (?, ?)', (date, price))
    conn.commit()
    conn.close()

