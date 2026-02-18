import os
from pathlib import Path
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


vault_dir = Path(__file__).resolve().parent / "data" / "vault"
salt_size = 16

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32, 
        salt=salt,
        iterations=600000, # Minimum iteration recommended for SHA256. https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
        backend=default_backend()
    )
    return kdf.derive(password.encode("utf-8"))


def encrypt_data(username, password, plaintext: bytes):
    os.makedirs(vault_dir, exist_ok=True)

    salt = os.urandom(salt_size)
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)

    ciphertext = aesgcm.encrypt(nonce, plaintext, None)

    filepath = os.path.join(vault_dir, f"{username}.enc")
    with open(filepath, "wb") as f:
        f.write(salt + nonce + ciphertext)


def decrypt_data(username, password) -> bytes:
    filepath = os.path.join(vault_dir, f"{username}.enc")
    with open(filepath, "rb") as f:
        data = f.read()

    salt = data[:salt_size]
    nonce = data[salt_size:salt_size + 12]
    ciphertext = data[salt_size + 12:]

    key = derive_key(password, salt)
    aesgcm = AESGCM(key)

    return aesgcm.decrypt(nonce, ciphertext, None)
