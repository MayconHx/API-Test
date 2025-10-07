from flask import Flask, jsonify, request
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

@app.route('/')
def home():
    return jsonify({"message": "Se viu e pq rodou"})


@app.route('/users', methods=['GET'])
def get_users():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name TEXT NOT NULL)")
        cur.execute("SELECT id, name FROM users")
        rows = cur.fetchall()
        cur.close()
        conn.close()

        users = [{"id": r[0], "name": r[1]} for r in rows]
        return jsonify(users)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    name = data.get("name")

    if not name:
        return jsonify({"error": "'name' é obrigatório"}), 400

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name TEXT NOT NULL)")
        cur.execute("INSERT INTO users (name) VALUES (%s) RETURNING id;", (name,))
        user_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"id": user_id, "name": name}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
