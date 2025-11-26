from apl import register_user, login_user

# Display menu
def menu():
    print("1. Register")
    print("2. Login")   
    print("3. Exit")

# Main function
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

