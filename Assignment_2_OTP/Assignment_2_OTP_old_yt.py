from pathlib import Path
from math import ceil
import subprocess
import hashlib
"""
THIS IS NOT THE MAIN PROGRAM! Please check Assignment_2_OTP_main.py
Note: This was the first implementation I did using live animal sanctuary feeds as an entropy source.
For this assignment, I swapped to the webcam solution considering the fact that the entropy source is technically
not coming from me, and is reliant on another party's youtube source (not to mention it being public, so it's not secure either).
"""

save_path = Path(__file__).parent / "screenshots"
youtube_url = "https://www.youtube.com/watch?v=yv5BH8zU9B0" # Change later?

def screenshot_footage(save_folder, stream_link, screenshot_qty):
    cmd = (
        f'yt-dlp -o - "{stream_link}" | '
        f'ffmpeg -i pipe:0 -vf fps=0.5 -frames:v {screenshot_qty} '
        f'"{save_folder / "frame_%03d.jpg"}"'
    )

    # ffmpeg will throw an error here because the yt-dlp is still streaming which leads to a broken pipe, which I'm not sure how to fix :(.
    # Code will still continue despite it.
    subprocess.run(cmd, shell=True, check=True)
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
    
def encrypt_otp(secret_text: str):
    hash_size = 32
    encrypted_text = secret_text.encode() # Changes the text into bytes.
    print(len(encrypted_text))

    picture_amount = ceil(len(encrypted_text) / hash_size) # The amount of pictures needed to take in order to have enough bytes for the key.
    screenshot_footage(save_path, youtube_url, picture_amount)

    encrypt_key = b"" # Keys we use to encrypt our text.
    for i in range(1, picture_amount + 1):
        filepath = save_path / f"frame_{i:03d}.jpg"
        encrypt_key += hash_image(filepath)
    
    encrypted_text = bytes([p ^ k for p, k in zip(encrypted_text, encrypt_key)])
    return encrypted_text, encrypt_key # Returns both the OTP-encrypted text as well as the key.

def decrypt_otp(encrypted_text: str, encrypt_key):
    decrypted_text = bytes([p ^ k for p, k in zip(encrypted_text, encrypt_key)])
    secret_text = decrypted_text.decode()
    return secret_text   
       
    

def main():
    my_secret = "Robbery at twelve thirty tomorrow"
    secret_encrypted, secret_key = encrypt_otp(my_secret)
    secret_decrypted = decrypt_otp(secret_encrypted, secret_key)
    print("Your secret message: " + my_secret)
    print("Shhhh, this is your secret key (in hex): " + str(secret_key.hex())) # Showcasing it in hex to make it more readable
    print("Your new encrypted phrase (in hex): " + str(secret_encrypted.hex())) 
    print("And your secret message was: " + str(secret_decrypted))

main()
#test_images = screenshot_footage(save_path, youtube_url, 3)


