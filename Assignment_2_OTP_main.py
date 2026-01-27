from pathlib import Path
from math import ceil
import cv2
import time
import hashlib

save_path = Path(__file__).parent / "screenshots"

def encrypt_otp(secret_text):
    hash_size = 32
    try: # Check if message is already in bytes (for binary) or if it isn't.
        encrypted_text = secret_text.encode() # Changes the text into bytes.
    except (UnicodeDecodeError, AttributeError):
        encrypted_text = secret_text

    picture_amount = ceil(len(encrypted_text) / hash_size) # The amount of pictures needed to take in order to have enough bytes for the key.
    print("Your message is " + str(len(encrypted_text)) + " bytes long. You will need " + str(picture_amount) + " pictures. Smile!")
    
    take_photo(save_path, picture_amount)

    encrypt_key = b"" # Keys we use to encrypt our text.
    for i in range(1, picture_amount + 1):
        filepath = save_path / f"webcam_{i:03d}.jpg"
        encrypt_key += hash_image(filepath)

    encrypted_text = bytes([p ^ k for p, k in zip(encrypted_text, encrypt_key)])
    return encrypted_text, encrypt_key # Returns both the OTP-encrypted text as well as the key.


def decrypt_otp(encrypted_text: str, encrypt_key):
    decrypted_text = bytes([p ^ k for p, k in zip(encrypted_text, encrypt_key)])
    try:
        secret_text = decrypted_text.decode()
    except (UnicodeDecodeError, AttributeError):
        secret_text = decrypted_text
    
    return secret_text
       

def take_photo(save_folder, screenshot_qty):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    time.sleep(2) # Allowing the camera to wake up properly.

    for i in range(screenshot_qty):
        time.sleep(2)

        for _ in range(10): # Flushing the camera in order to take photos of the current time, after 2 seconds have passed.
            cap.read()
            
        ret, frame = cap.read() # Here we actually take the shot we want to keep.
        
        if ret:
            filepath = save_folder / f"webcam_{i+1:03d}.jpg" 
            cv2.imwrite(str(filepath), frame)
            print(f"Saved photo {i+1}.")
    cap.release()
    return
    
    
def hash_image(filepath): # Hashing an image we take from 
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        while True:
            data = f.read(65536) # Reading at 64kb at a time to limit memory usage.
            if not data:
                break
            sha256.update(data)

        return sha256.digest()
    
    
def main():
    my_secret = "Robbery at twelve thirty tomorrow"
    secret_encrypted, secret_key = encrypt_otp(my_secret)
    secret_decrypted = decrypt_otp(secret_encrypted, secret_key)
    print()
    print("Your secret message was: " + str(my_secret))
    print("Shhhh, this is your secret key (in hex): " + str(secret_key.hex())) # Showcasing it in hex to make it more readable
    print("Your new encrypted phrase (in hex): " + str(secret_encrypted.hex())) 
    print("And decrypting the encrypted phrase gives us the message: " + str(secret_decrypted))

# Binary version
'''    
    binary_plaintext =  b'\xAF\x2C\x01\xFF' # 10101111 00101100 00000001 11111111
    secret_encrypted, secret_key = encrypt_otp(binary_plaintext)
    secret_decrypted = decrypt_otp(secret_encrypted, secret_key)
    print()
    print("Your secret message was: " + str(binary_plaintext))
    print("Shhhh, this is your secret key: " + str(secret_key)) # Showcasing it in hex to make it more readable
    print("Your new encrypted phrase: " + str(secret_encrypted)) 
    print("And decrypting the encrypted phrase gives us the message: " + str(secret_decrypted))
'''

if __name__ == "__main__":
    main()


