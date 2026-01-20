#Author: Along A. Loftsson, aal9@hi.is

def caesar_encrypt(text, shift_num) -> str:
    '''
    A caesar encryption function. Takes a body of text, a shift key, and shifts the text to the right (up) according to the shift number. English Language only.
    
    :param text: Text that gets ciphered.
    :param shift_num: What the shift key should be.
    :return: Returns the text ciphered.
    :rtype: str
    '''

    encrypted_text = ""
    for i in text:
        unicode_letter = ord(i) # Convert letter to its unicode counterpart.
        if  65 <= unicode_letter <= 90: # Unicode range of uppercase english alphabet.
            overflow_limit = 90
        elif 97 <= unicode_letter <= 122: # Unicode range of lowercase english alphabet.
            overflow_limit = 122
        else:
            encrypted_text += i
            continue

        unicode_letter += (shift_num % 26) # In case the shift number excceeds the size of alphabet (25). 26 would go from A -> A.
        if unicode_letter > overflow_limit: # Check if letter overflows.
            unicode_letter -= 26
        
        encrypted_text += chr(unicode_letter) # Convert unicode back to letter and add it to the encrypted body of text.
            
    return encrypted_text


def caesar_decrypt(text, shift_num) -> str:
    '''
    Similar to caesar_encrypt, with checks happening at the opposite ends of the range and shifting happening left (down) instead of right.
    
    :param text: Text you want to be deciphered.
    :param shift_num: What the shift key should be.
    :return: Returns the text deciphered.
    :rtype: str
    '''

    decrypted_text = ""
    for i in text:
        unicode_letter = ord(i) # Convert letter to its unicode counterpart.
        if  65 <= unicode_letter <= 90: # Unicode range of uppercase english alphabet.
            underflow_limit = 65
        elif 97 <= unicode_letter <= 122: # Unicode range of lowercase english alphabet.
            underflow_limit = 97
        else:
            decrypted_text += i
            continue

        unicode_letter -= (shift_num % 26) # In case the shift number excceeds the size of alphabet (25). 26 would go from A -> A.
        if unicode_letter < underflow_limit: # Check if letter underflows.
            unicode_letter += 26
        
        decrypted_text += chr(unicode_letter) # Convert unicode back to letter and add it to the decrypted body of text.
            
    return decrypted_text

if __name__ == "__main__":
    my_text = "This is a small body of text that is a secret."
    my_shift_num = 39

    secret_word = caesar_encrypt(my_text, my_shift_num)
    print(secret_word)
    secret_word = caesar_decrypt(secret_word, my_shift_num)
    print(secret_word)