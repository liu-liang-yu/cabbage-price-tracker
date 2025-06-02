from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_NAME = 'cabbage.db'

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        with open('schema.sql', 'r') as f:
            conn.executescript(f.read())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_price():
    date = request.form['date']
    price = request.form['price']
    source = request.form['source']
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO cabbage_prices (date, price, source) VALUES (?, ?, ?)", (date, price, source))
        conn.commit()
    return redirect('/query')

@app.route('/query')
def query():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    query = "SELECT date, price, source FROM cabbage_prices"
    params = []
    if start_date and end_date:
        query += " WHERE date BETWEEN ? AND ?"
        params.extend([start_date, end_date])
    query += " ORDER BY date DESC"
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute(query, params)
        rows = cur.fetchall()
    return render_template('query.html', rows=rows)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
