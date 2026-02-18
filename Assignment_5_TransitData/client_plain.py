import socket
import json
import time

HOST = "127.0.0.1"
PORT = 5000


def send_request(request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(json.dumps(request).encode("utf-8"))
        response = s.recv(4096)
        return json.loads(response.decode("utf-8"))


# The functions below are used to measure the performance between the plain and secure methods.
'''
def send_request(request):
    start = time.perf_counter()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(json.dumps(request).encode("utf-8"))
        response = s.recv(4096)

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

    print("Running LOGIN performance test (Plain TCP)...")

    login_request = {
        "action": "login",
        "username": username,
        "password": password
    }

    performance_test(login_request)

    print("\nRunning ENCRYPT performance test (Plain TCP)...")

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