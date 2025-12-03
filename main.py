import bcrypt
import sqlite3
import pandas as pd
from app_model.db import conn
from app_model.users import add_user, get_user


# Function to hash a password
def hash_password(pwd):
    password_bytes = pwd.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

# Function to validate a password
def validate_password(pwd, hashed):
    password_bytes = pwd.encode('utf-8')
    hashed_bytes = hashed.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

# Function to register a new user
def register_user(conn):
    username = input("Enter username: ")
    password = input("Enter password: ")

    hashed_password = hash_password(password)
    add_user(conn, username, hashed_password)
    with open("DATA/user.txt", "a") as f:
        f.write(f"{username},{hashed_password}\n")
    print("User registered successfully.")

# Function to login a user
def login_user(conn):
    name = input("Enter username: ")
    password = input("Enter password: ")

    user_data = get_user(conn, name)  # fetch the user
    if user_data is None:
        print("User not found.")
        return False

    id, user_name, user_hash = user_data
    print(f"Welcome! {user_name}")

    if validate_password(password, user_hash):
        print("Login successful.")
        return True
    else:
        print("Invalid password.")
        return False
    
    
def menu():
    print("1. Register")
    print("2. Login")   
    print("3. Exit")


def main():
    while True:
        menu()
        choice = input("Enter choice: ")
        if choice == "1":
            register_user(conn)
        elif choice == "2":
            login_user(conn)
        elif choice == "3":
            print("Exiting...")
            break



if __name__ == "__main__":
    main()

















