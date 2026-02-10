import csv
import bcrypt
import time
from pathlib import Path

base_directory = Path(__file__).resolve().parent
users_file = base_directory / "data" / "users.csv"
pw_list = base_directory / "pwlist.txt"

user_target = "luke"


def load_hash():
    with users_file.open(newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["username"] == user_target:
                return row["password_hash"].encode("utf-8")
    return None


def bruteforce():
    target_hash = load_hash()
    if not target_hash:
        print("User not found.")
        return

    attempts = 0
    start = time.perf_counter()

    with pw_list.open() as f:
        for password in f:
            password = password.strip()
            attempts += 1

            if bcrypt.checkpw(password.encode("utf-8"), target_hash):
                elapsed = time.perf_counter() - start
                print(f"Password found: {password}")
                print(f"Attempts: {attempts}")
                print(f"Time: {elapsed:.2f} seconds")
                print(f"Attempts/sec: {attempts / elapsed:.2f}")
                return

    print("Password not found in database.")


bruteforce()
