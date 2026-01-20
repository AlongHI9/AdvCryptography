from random import randrange
from Assignment_1_1_Caesar import caesar_encrypt

def et_tu_Brute_force(text):
    for x in range(26):
        decrypted_text = ""
        for i in text:
            unicode_letter = ord(i) # Convert letter to its unicode counterpart.
            if  65 <= unicode_letter <= 90: # Unicode range of uppercase english alphabet.
                overflow_limit = 90
            elif 97 <= unicode_letter <= 122: # Unicode range of lowercase english alphabet.
                overflow_limit = 122
            else:
                decrypted_text += i
                continue

            unicode_letter += x # In case the shift number excceeds the size of alphabet (25). 26 would go from A -> A.
            if unicode_letter > overflow_limit: # Check if letter overflows.
                unicode_letter -= 26
            
            decrypted_text += chr(unicode_letter) # Convert unicode back to letter and add it to the encrypted body of text.
        
        print("LS " + str(x) + ", RS " + str(25-x) + ": " + decrypted_text)
                

secret_text = "Welcome, to the world of Cryptography!"
encrypted_text = caesar_encrypt(secret_text, randrange(1,26))
et_tu_Brute_force(encrypted_text)