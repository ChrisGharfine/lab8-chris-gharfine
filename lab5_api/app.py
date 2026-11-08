import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS


def connect_to_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def create_db_table():
    conn = connect_to_db()
    try:
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY NOT NULL,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            country TEXT NOT NULL
        )''')
        conn.commit()
    finally:
        conn.close()


def get_users():
    conn = connect_to_db()
    try:
        return [dict(row) for row in conn.execute('SELECT * FROM users')]
    except sqlite3.Error:
        return []
    finally:
        conn.close()


def get_user_by_id(user_id):
    conn = connect_to_db()
    try:
        row = conn.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()
        return dict(row) if row else {}
    except sqlite3.Error:
        return {}
    finally:
        conn.close()


def insert_user(user):
    conn = connect_to_db()
    try:
        cursor = conn.execute(
            'INSERT INTO users (name, email, phone, address, country) VALUES (?, ?, ?, ?, ?)',
            (user['name'], user['email'], user['phone'], user['address'], user['country'])
        )
        conn.commit()
        return get_user_by_id(cursor.lastrowid)
    except sqlite3.Error:
        conn.rollback()
        return {}
    finally:
        conn.close()


def update_user(user):
    conn = connect_to_db()
    try:
        conn.execute(
            'UPDATE users SET name = ?, email = ?, phone = ?, address = ?, country = ? WHERE user_id = ?',
            (user['name'], user['email'], user['phone'], user['address'], user['country'], user['user_id'])
        )
        conn.commit()
        return get_user_by_id(user['user_id'])
    except sqlite3.Error:
        conn.rollback()
        return {}
    finally:
        conn.close()


def delete_user(user_id):
    conn = connect_to_db()
    try:
        conn.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
        conn.commit()
        return {'status': 'User deleted successfully'}
    except sqlite3.Error:
        conn.rollback()
        return {'status': 'Cannot delete user'}
    finally:
        conn.close()


app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/api/users', methods=['GET'])
def api_get_users():
    return jsonify(get_users())


@app.route('/api/users/<user_id>', methods=['GET'])
def api_get_user(user_id):
    return jsonify(get_user_by_id(user_id))


@app.route('/api/users/add', methods=['POST'])
def api_add_user():
    return jsonify(insert_user(request.get_json()))


@app.route('/api/users/update', methods=['PUT'])
def api_update_user():
    return jsonify(update_user(request.get_json()))


@app.route('/api/users/delete/<user_id>', methods=['DELETE'])
def api_delete_user(user_id):
    return jsonify(delete_user(user_id))


if __name__ == '__main__':
    create_db_table()
    app.run(host='0.0.0.0', port=5000)
