import socket
import json
import ssl
from pathlib import Path
from users import init_users_file, register_user, authenticate_user
from data_encryption import encrypt_data, decrypt_data


HOST = "127.0.0.1"
PORT = 5000

base_dir = Path(__file__).resolve().parent
cert_path = base_dir / "cert.pem"
key_path = base_dir / "key.pem"


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

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

    # Force modern TLS
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.set_ciphers("ECDHE+AESGCM")
    context.load_cert_chain(certfile=str(cert_path), keyfile=str(key_path))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen(1)
        print("Secure server listening...")

        while True:
            conn, addr = sock.accept()
            print("Connected by", addr)

            with context.wrap_socket(conn, server_side=True) as secure_conn:
                while True:
                    data = secure_conn.recv(4096)
                    if not data:
                        break

                    response = handle_request(data.decode("utf-8"))
                    secure_conn.sendall(json.dumps(response).encode("utf-8"))

            print("Returned data for client ", addr)

if __name__ == "__main__":
    main()