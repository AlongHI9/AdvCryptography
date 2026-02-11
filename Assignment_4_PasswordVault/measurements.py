import time
from users import authenticate_user
from data_encryption import encrypt_data, decrypt_data

def measure_auth_time(username, password):
    start = time.perf_counter()
    authenticate_user(username, password)
    end = time.perf_counter()
    return (end - start) * 1000  # Counting time in ms.

def generate_data(size_bytes):
    return b"A" * size_bytes # Creating some data of fixed size.

def measure_encrypt_time(username, password, data):
    start = time.perf_counter()
    encrypt_data(username, password, data)
    end = time.perf_counter()
    return (end - start) * 1000

def measure_decrypt_time(username, password):
    start = time.perf_counter()
    decrypt_data(username, password)
    end = time.perf_counter()
    return (end - start) * 1000