from pathlib import Path
import csv
import os
import bcrypt

users_file = Path(__file__).resolve().parent / "data" / "users.csv"

def init_users_file():
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(users_file):
        with open(users_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["username", "password_hash"])

def register_user(username, password):
    with open(users_file, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["username"] == username:
                return False

    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    with open(users_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([username, password_hash])

    return True

def authenticate_user(username, password):
    with open(users_file, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["username"] == username:
                return bcrypt.checkpw(password.encode("utf-8"), row["password_hash"].encode("utf-8"))
    return False
