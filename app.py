from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
from database import create_user, find_user_by_username, verify_password

app = Flask(__name__)
app.secret_key = os.urandom(24)

# HTML serving routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/profile')
def profile_page():
    if 'username' in session:
        return render_template('profile.html')
    return redirect(url_for('login_page'))

# API routes
@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    if find_user_by_username(username):
        return jsonify({'message': 'User already exists'}), 400

    create_user(username, password)
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    user = find_user_by_username(username)

    if user and verify_password(user, password):
        session['username'] = username
        return jsonify({'message': 'Login successful'})
    
    return jsonify({'message': 'Invalid username or password'}), 401

@app.route('/api/logout')
def api_logout():
    session.pop('username', None)
    return jsonify({'message': 'Logout successful'})

@app.route('/api/profile')
def api_profile():
    if 'username' in session:
        return jsonify({'username': session['username']})
    return jsonify({'message': 'Unauthorized'}), 401

if __name__ == '__main__':
    app.run(debug=True)