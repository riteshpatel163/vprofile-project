from flask import Flask, jsonify, request, render_template
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

import os

# MySQL connection
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', 'password'),
        database='demo_db'
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return jsonify(users)

@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, email) VALUES (%s, %s)', 
                   (data['name'], data['email']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'User added successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)