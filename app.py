from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database import create_user, find_user_by_username

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    if find_user_by_username(username):
        return jsonify({'message': 'User already exists'}), 400

    hashed_password = generate_password_hash(password)
    create_user({'username': username, 'password': hashed_password})

    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    user = find_user_by_username(username)

    if not user or not check_password_hash(user.get('password'), password):
        return jsonify({'message': 'Invalid username or password'}), 401

    return jsonify({'message': 'Login successful'})

if __name__ == '__main__':
    app.run(debug=True)
