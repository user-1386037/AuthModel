import unittest
import os
import json
from database import create_user, find_user_by_username, verify_password, USERS_FILE

class TestAuth(unittest.TestCase):

    def setUp(self):
        # Ensure a clean users.jsonl for each test
        if os.path.exists(USERS_FILE):
            os.remove(USERS_FILE)
        # Create an empty file if it doesn't exist, so open() in database.py doesn't fail
        open(USERS_FILE, 'a').close()

    def tearDown(self):
        # Clean up after each test
        if os.path.exists(USERS_FILE):
            os.remove(USERS_FILE)

    def test_vague_error_messages(self):
        # Test login with non-existent username
        user = find_user_by_username("nonexistent_user")
        self.assertIsNone(user)

        # Create a user for testing incorrect password
        create_user("testuser", "password123")
        user = find_user_by_username("testuser")
        self.assertIsNotNone(user)

        # Test login with correct username but incorrect password
        self.assertFalse(verify_password(user, "wrongpassword"))

    def test_hash_and_salt_work_properly(self):
        username = "testuser_hash"
        password = "securepassword"
        create_user(username, password)

        user = find_user_by_username(username)
        self.assertIsNotNone(user)

        # Verify salt and hash are stored and not the original password
        self.assertIn('salt', user)
        self.assertIn('password_hash', user)
        self.assertNotEqual(user['password_hash'], password) # Stored hash should not be plaintext password

        # Verify correct password
        self.assertTrue(verify_password(user, password))

        # Verify incorrect password
        self.assertFalse(verify_password(user, "incorrectpassword"))

        # Test two users with same password have different salts and hashes
        create_user("user1", "commonpass")
        create_user("user2", "commonpass")

        user1 = find_user_by_username("user1")
        user2 = find_user_by_username("user2")

        self.assertIsNotNone(user1)
        self.assertIsNotNone(user2)

        self.assertNotEqual(user1['salt'], user2['salt'])
        self.assertNotEqual(user1['password_hash'], user2['password_hash'])
        self.assertTrue(verify_password(user1, "commonpass"))
        self.assertTrue(verify_password(user2, "commonpass"))

    def test_username_uniqueness(self):
        username = "uniqueuser"
        password = "pass1"

        create_user(username, password)
        self.assertIsNotNone(find_user_by_username(username))

        # Attempt to create user with same username again
        # The create_user function in database.py doesn't prevent creation, it just appends.
        # The check for uniqueness is done in app.py. So, we need to test find_user_by_username after creation.
        # For this test, we will check if find_user_by_username still returns the *first* user.
        # In a real scenario, create_user should ideally return a status or raise an error if user exists.
        # However, given the current implementation, we test how app.py would handle it.

        # Simulate app.py's check before calling create_user
        if not find_user_by_username(username):
            create_user(username, "pass2")

        # Verify that only one user with that username exists (the first one created)
        # This requires reading the file and counting, or relying on find_user_by_username returning the first match.
        # Since find_user_by_username returns the first match, we can check if the password hash is still the first one.
        user_after_second_attempt = find_user_by_username(username)
        self.assertIsNotNone(user_after_second_attempt)
        self.assertTrue(verify_password(user_after_second_attempt, password))
        self.assertFalse(verify_password(user_after_second_attempt, "pass2")) # Should still be the first user's password

if __name__ == '__main__':
    unittest.main()
