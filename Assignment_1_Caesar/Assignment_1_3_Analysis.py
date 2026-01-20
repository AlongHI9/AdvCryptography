from pathlib import Path
import matplotlib.pyplot as plt
from Assignment_1_1_Caesar import caesar_encrypt, caesar_decrypt
from random import randrange

secret_text = "Welcome, to the world of Cryptography! This is a small body of text that we will be checking and comparing against the frequency analysis of something fun."

# Here we create dictionaries to populate the frequencies. en_freq = English frequency. book_freq = Book frequency. msg_freq = Message frequency.
en_freq = {"a":0, "b":0, "c":0, "d":0, "e":0, "f":0, "g":0, "h":0, "i":0, "j":0, "k":0, "l":0, "m":0, "n":0, "o":0, "p":0, "q":0, "r":0, "s":0, "t":0, "u":0, "v":0, "w":0, "x":0, "y":0, "z":0} 
book_freq = {"a":0, "b":0, "c":0, "d":0, "e":0, "f":0, "g":0, "h":0, "i":0, "j":0, "k":0, "l":0, "m":0, "n":0, "o":0, "p":0, "q":0, "r":0, "s":0, "t":0, "u":0, "v":0, "w":0, "x":0, "y":0, "z":0}
msg_freq = {"a":0, "b":0, "c":0, "d":0, "e":0, "f":0, "g":0, "h":0, "i":0, "j":0, "k":0, "l":0, "m":0, "n":0, "o":0, "p":0, "q":0, "r":0, "s":0, "t":0, "u":0, "v":0, "w":0, "x":0, "y":0, "z":0}

p = Path(__file__).with_name("THE_MONK.txt") # Using long text, unencrypted, to create our own frequency analysis of the English language.
with p.open('r', encoding='utf-8') as f:
    freq_data = f.read()

p = Path(__file__).with_name("THE_KING_IN_YELLOW.txt") # Grabbing different long text, which we will encrypt for analysis.
with p.open('r', encoding='utf-8') as f:
    book_encrypted = f.read()

secret_text = caesar_encrypt(secret_text, randrange(1,26)) # Shifting the letters by a random range for analysis purposes.
book_encrypted = caesar_encrypt(book_encrypted, randrange(1,26))

for i in freq_data: # Populating the en_freq with the frequency of letters of the English language.
    if i.isalpha():
        en_freq[i.lower()] = en_freq[i.lower()] + 1

for i in book_encrypted: # Populating the book_freq with the frequency of letters of the encrypted book.
    if i.isalpha():
        book_freq[i.lower()] = book_freq[i.lower()] + 1

for i in secret_text: # Populating the msg_freq with the frequency of letters of the encrypted text.                                                                     i
    if i.isalpha():
        msg_freq[i.lower()] = msg_freq[i.lower()] + 1

# Here we utilize matplotlib to showcase the frequency histograms of our texts.
key = list(en_freq.keys()) # Starting with the untouched long text.
value = list(en_freq.values())
plt.bar(key, value)
plt.title('Frequency of the most used letters in "The Monk".')
plt.show()

key = list(book_freq.keys()) # Here is the encrypted long text.
value = list(book_freq.values())
plt.bar(key, value)
plt.title('Frequency of the most used letters in "The King in Yellow" after encryption.')
plt.show()

key = list(msg_freq.keys()) # Here is the encrypted short text.
value = list(msg_freq.values())
plt.bar(key, value)
plt.title('Frequency of the most used letters in "The secret message" after encryption.')
plt.show()


encrypted_text = "Qyfwigy, ni nby qilfx iz Wlsjnialujbs! Nbcm cm u mguff vixs iz nyrn nbun qy qcff vy wbywecha uhx wigjulcha uauchmn nby zlykoyhws uhufsmcm iz migynbcha zoh."

decrypted_text = caesar_decrypt(encrypted_text, 20)
print(decrypted_text)