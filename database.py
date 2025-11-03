import json
import hashlib
import os

USERS_FILE = 'users.jsonl'

def create_user(username, password):
    """Creates a new user with a salted and hashed password."""
    salt = os.urandom(16)
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    user = {
        'username': username,
        'salt': salt.hex(),
        'password_hash': password_hash.hex()
    }
    with open(USERS_FILE, 'a') as f:
        f.write(json.dumps(user) + '\n')

def find_user_by_username(username):
    """Finds a user by username in the users.jsonl file."""
    try:
        with open(USERS_FILE, 'r') as f:
            for line in f:
                user = json.loads(line)
                if user.get('username') == username:
                    return user
    except FileNotFoundError:
        return None
    return None

def verify_password(user, password):
    """Verifies the password for a given user."""
    salt = bytes.fromhex(user['salt'])
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return password_hash == bytes.fromhex(user['password_hash'])