import argon2
import os
from dotenv import load_dotenv

load_dotenv()

def hash_password_with_salt_and_pepper(password):
    # Generate a random salt
    salt = os.urandom(16)

    # Loading the secret pepper and encoding it to bytes
    pepper = os.getenv('PEPPER').encode('utf-8')

    # Combine the password and pepper
    password_with_pepper = pepper + password.encode('utf-8')

    # Hash the password with salt and pepper using Argon2id
    ph = argon2.PasswordHasher()
    hash = ph.hash(password_with_pepper, salt=salt)

    return hash, salt

# Example usage:
password = "example_password"
hashed_password, salt = hash_password_with_salt_and_pepper(password)
print("Hashed password:", hashed_password)
print("Salt:", salt.hex())
