import bcrypt

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
def register_user():
    username = input("Enter username: ")
    password = input("Enter password: ")
    hashed_password = hash_password(password)
    with open("user.txt", "a") as f:
        f.write(f"{username},{hashed_password}\n")
    print("user registered successfully.")

# Function to login a user
def login_user(username, password):
    with open("user.txt", "r") as f:
        lines= f.readlines()
        for line in lines :
            stored_username, stored_hashed = line.strip().split(",")
            if stored_username == username:
                if validate_password(password, stored_hashed):
                    print("Login successful.")
                    return
                else:
                    print("Invalid password.")
                    return
        print("Username not found.")
def menu():
    print("1. Register")
    print("2. Login")   
    print("3. Exit")


def main():
    while True:
        menu()
        choice = input("Enter choice: ")
        if choice == "1":
            register_user()
        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            login_user(username, password)
        elif choice == "3":
            print("Exiting...")
            break

if __name__ == "__main__":
    main()