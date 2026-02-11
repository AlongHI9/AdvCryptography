from users import init_users_file, register_user, authenticate_user
from data_encryption import encrypt_data, decrypt_data
from measurements import *


def measurement_tests():
    sizes = [
        1024,        # 1 KB
        10240,       # 10 KB
        102400,      # 100 KB
        1048576,    # 1 MB (1024 KB)
        10485760,   # 10 MB (10240 KB)
        104857600   # 100 MB (102400 KB)
    ]
    
    init_users_file() # Just in case this function is run first.

    print("Measuring the time authentication of 5 users in ms.")
    for i in range(5):
        print(f"Test {i+1}: {measure_auth_time("lucy", "goodman"):.3f} ms.") # Using user "lucy" with pw "goodman"
    print("Done.")

    print("Measuring the time encryption and decryption in ms of different sizes.")

    for size in sizes:
        data = generate_data(size)

        enc_time = measure_encrypt_time("lucy", "goodman", data)
        dec_time = measure_decrypt_time("lucy", "goodman")

        print(f"Size: {size // 1024} KB. Encryption: {enc_time:.3f} ms. Decryption: {dec_time:.3f} ms.")


def main():
    init_users_file()

    print("Welcome to the Secret Message Vault.")
    while True:
        print("\nPlease choose an option:")
        print("1. Register")
        print("2. Login")
        print("3. Quit")
        choice = input("> ")

        if choice == "1" or choice == "2":
            username = input("Username: ")
            password = input("Password: ")
            if choice == "1":
                if register_user(username, password):
                    print("User registered.")
                else:
                    print("User already exists.")

            elif choice == "2":
                if authenticate_user(username, password):
                    print("Login successful.")

                    print("1. Encrypt New Message")
                    print("2. Decrypt Previous Message")
                    action = input("> ")

                    if action == "1":
                        message = input("Message to store: ").encode("utf-8")
                        encrypt_data(username, password, message)
                        print("Data encrypted and stored.")
                    elif action == "2":
                        data = decrypt_data(username, password)
                        print("Decrypted data:", data.decode("utf-8"))
                else:
                    print("Login failed.")

        elif choice == "3":
            print("Thank you for using our service.")
            break

        else:
            print("That is not an option. Try again.")

if __name__ == "__main__":
    main()
    #measurement_tests()
