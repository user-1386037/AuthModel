import sys
import getpass
from database import create_user, find_user_by_username, verify_password

def main():
    if len(sys.argv) != 2:
        print("Usage: python app.py [create|login]")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'create':
        username = input("Enter username: ")
        password = getpass.getpass("Enter password: ")
        if find_user_by_username(username):
            print("User already exists.")
        else:
            create_user(username, password)
            print("User created successfully.")
    elif command == 'login':
        username = input("Enter username: ")
        password = getpass.getpass("Enter password: ")
        user = find_user_by_username(username)
        if user and verify_password(user, password):
            print("Login successful.")
        else:
            print("Invalid username or password.")
    else:
        print(f"Unknown command: {command}")
        print("Usage: python app.py [create|login]")
        sys.exit(1)

if __name__ == '__main__':
    main()