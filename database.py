import json

USERS_FILE = 'users.jsonl'

def create_user(user):
    """Appends a user to the users.jsonl file."""
    with open(USERS_FILE, 'a') as f:
        f.write(json.dumps(user) + '\n')

def find_user_by_username(username):
    """Finds a user by username in the users.jsonl file."""
    with open(USERS_FILE, 'r') as f:
        for line in f:
            user = json.loads(line)
            if user.get('username') == username:
                return user
    return None
