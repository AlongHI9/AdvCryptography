from Assignment_2_OTP_main import hash_image
from pathlib import Path
import secrets
from collections import Counter
import math
import matplotlib.pyplot as plt

save_path = Path(__file__).parent / "screenshots"

def shannon_entropy(data: bytes):
    counts = Counter(data) # Occurance of each byte.
    total = len(data) # Total number of bytes.
    return -sum((c / total) * math.log2(c / total) for c in counts.values()) # The sum over all unique bytes: p(x) * log2(p(x)).

def encrypt_many(): # Used to hash the mass webcam data that was taken beforehand.
    encrypt_key = b"" # Keys we use to encrypt our text.
    for i in range(1, 50 + 1):
        filepath = save_path / f"webcamData_{i:03d}.jpg"
        encrypt_key += hash_image(filepath)

    return encrypt_key # Returns the key.


webcam_keys = encrypt_many()
os_keys = secrets.token_bytes(len(webcam_keys)) # Generates random bytes with the same length as the webcam key bytes.

entropy_webcam = shannon_entropy(webcam_keys)
entropy_os = shannon_entropy(os_keys)

print(f"The webcam key entropy is: {entropy_webcam:.3f} bits/byte")
print(f"The OS key entropy is: {entropy_os:.3f} bits/byte")



webcam_keys_int = list(webcam_keys) # For matplotlib
os_keys_int = list(os_keys)

# Here we utilize matplotlib to showcase the byte distribution.
plt.figure(figsize=(12, 6))
bins = range(256)
plt.hist(webcam_keys_int, bins=bins, label="Webcam Keys", color='blue')
plt.hist(os_keys_int, bins=bins, label="OS Keys", color='orange')
plt.xlabel("Bytes 0-255")
plt.ylabel("Normalized Frequency")
plt.title("Comparison of Byte Distributio")
plt.legend()
plt.show()


