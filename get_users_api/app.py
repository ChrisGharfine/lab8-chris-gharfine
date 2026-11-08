import sqlite3
from flask import Flask, jsonify


def connect_to_db():
    return sqlite3.connect('database.db')


def get_user_names():
    conn = connect_to_db()
    try:
        rows = conn.execute('SELECT name FROM users').fetchall()
        return [row[0] for row in rows]
    except sqlite3.Error:
        return []
    finally:
        conn.close()


app = Flask(__name__)


@app.route('/api/get_users', methods=['GET'])
def api_get_users():
    return jsonify(get_user_names())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
