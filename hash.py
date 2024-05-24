import argon2
import os

def hash_password_with_salt_and_pepper(password):
    # Generate a random salt (will be set in a configuration file)
    salt = os.urandom(16)

    # Defining the secret pepper (will be in a configuration file)
    pepper = b'my_secret_pepper'

    # Combine the password and pepper
    password_with_pepper = pepper + password.encode('utf-8')

    # Hash the password with salt and pepper using Argon2id
    ph = argon2.PasswordHasher(time_cost=2, memory_cost=102400, parallelism=8)
    hash = ph.hash(password_with_pepper, salt)

    return hash, salt

# Example usage:
password = "example_password"
hashed_password, salt = hash_password_with_salt_and_pepper(password)
print("Hashed password:", hashed_password)
print("Salt:", salt.hex())
