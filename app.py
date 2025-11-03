import getpass
from database import create_user, find_user_by_username, verify_password

def create_user_flow():
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    if find_user_by_username(username):
        print("User already exists.")
    else:
        create_user(username, password)
        print("User created successfully.")

def login_flow():
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    user = find_user_by_username(username)
    if user and verify_password(user, password):
        print("Login successful.")
    else:
        print("Invalid username or password.")

def main():
    while True:
        print("\nChoose an option:")
        print("1. Login")
        print("2. Create user")
        print("q. Quit")
        choice = input("Enter your choice: ")

        if choice == '1':
            login_flow()
        elif choice == '2':
            create_user_flow()
        elif choice.lower() == 'q':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
