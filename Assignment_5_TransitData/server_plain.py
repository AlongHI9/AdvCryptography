import socket
import json
from users import init_users_file, register_user, authenticate_user
from data_encryption import encrypt_data, decrypt_data

HOST = "127.0.0.1"
PORT = 5000

def handle_request(data):
    request = json.loads(data)

    action = request.get("action")
    username = request.get("username")
    password = request.get("password")

    if action == "register":
        if register_user(username, password):
            return {"status": "success"}
        return {"status": "fail"}

    elif action == "login":
        if authenticate_user(username, password):
            return {"status": "success"}
        return {"status": "fail"}

    elif action == "encrypt":
        plaintext = request.get("message").encode("utf-8")
        encrypt_data(username, password, plaintext)
        return {"status": "stored"}

    elif action == "decrypt":
        data = decrypt_data(username, password)
        return {"status": "success", "data": data.decode("utf-8")}

    return {"status": "invalid"}

def main():
    init_users_file()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        print("Server listening...")

        while True:
            conn, addr = s.accept()
            print("Request sent by client ", addr)

            with conn:
                while True:
                    data = conn.recv(4096)
                    if not data:
                        break

                    response = handle_request(data.decode("utf-8"))
                    conn.sendall(json.dumps(response).encode("utf-8"))

            print("Returned data for client ", addr)

if __name__ == "__main__":
    main()