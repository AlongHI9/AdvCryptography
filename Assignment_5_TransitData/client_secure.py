import socket
import json
import ssl
from pathlib import Path
import time

HOST = "127.0.0.1"
PORT = 5000

base_dir = Path(__file__).resolve().parent
cert_path = base_dir / "cert.pem"
key_path = base_dir / "key.pem"


def send_request(request):
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations(cafile=str(cert_path))
    context.check_hostname = False
    context.verify_mode = ssl.CERT_REQUIRED

    with socket.create_connection((HOST, PORT)) as sock:
        with context.wrap_socket(sock, server_hostname=HOST) as ssock:
            ssock.sendall(json.dumps(request).encode("utf-8"))
            response = ssock.recv(4096)
            return json.loads(response.decode("utf-8"))


# The functions below are used to measure the performance between the plain and secure methods.
''' 
def send_request(request):
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations(cafile=str(cert_path))
    context.check_hostname = False
    context.verify_mode = ssl.CERT_REQUIRED

    start = time.perf_counter()

    with socket.create_connection((HOST, PORT)) as sock:
        with context.wrap_socket(sock, server_hostname=HOST) as ssock:
            ssock.sendall(json.dumps(request).encode("utf-8"))
            response = ssock.recv(4096)

    end = time.perf_counter()

    return json.loads(response.decode("utf-8")), (end - start)

def performance_test(request, iterations=20):
    times = []

    for _ in range(iterations):
        _, duration = send_request(request)
        times.append(duration)

    avg = sum(times) / len(times)
    print(f"Average over {iterations} runs: {avg * 1000:.3f} ms")

def test():
    username = input("Username: ")
    password = input("Password: ")

    print("Running LOGIN performance test (TLS)...")

    login_request = {
        "action": "login",
        "username": username,
        "password": password
    }

    performance_test(login_request)

    print("\nRunning ENCRYPT performance test (TLS)...")

    encrypt_request = {
        "action": "encrypt",
        "username": username,
        "password": password,
        "message": "performance_test_message"
    }

    performance_test(encrypt_request)
'''

def main():
    print("1. Register")
    print("2. Login")
    choice = input("> ")

    username = input("Username: ")
    password = input("Password: ")

    if choice == "1":
        response = send_request({
            "action": "register",
            "username": username,
            "password": password
        })
        print(response)

    elif choice == "2":
        response = send_request({
            "action": "login",
            "username": username,
            "password": password
        })

        if response["status"] == "success":
            print("Login successful")

            print("1. Encrypt")
            print("2. Decrypt")
            action = input("> ")

            if action == "1":
                message = input("Message: ")
                response = send_request({
                    "action": "encrypt",
                    "username": username,
                    "password": password,
                    "message": message
                })
                print(response)

            elif action == "2":
                response = send_request({
                    "action": "decrypt",
                    "username": username,
                    "password": password
                })
                print("Decrypted:", response.get("data"))

        else:
            print("Login failed")

if __name__ == "__main__":
# Comment main out and uncomment test when you want to do performance testing.
    main()
    #test() 