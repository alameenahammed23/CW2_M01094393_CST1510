import bcrypt
import sqlite3
import pandas as pd
from app_model.db import conn
from app_model.users import add_user, get_user
from hashing import hash_password, validate_password

# Function to register a new user
def register_user(conn):
    username = input("Enter username: ")
    password = input("Enter password: ")

   
    with open("DATA/user.txt", "a") as f:
        f.write(f"{username},{hash_password}\n")
    print("User registered successfully.")

# Function to login a user
def login_user(conn):
    name = input("Enter username: ")
    password = input("Enter password: ")


    
    
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

















