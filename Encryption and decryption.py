import random
import string

password = "Cristiano@1984"
print("Password: ",password)

def encryption(password):
    # hardcoded all user inputs
    Keyboard = "(l@p?si!3=g0Z5>2-TBUzx]7tGVHw8&.[4_n}F{O9^ENKhD6v:f$XdPeaAq1yYCmI,JojMk)*S%#u<bcRrLQ;W+"
    shift_key = len(password)

    # Shifting the whole keyboard
    shifted = Keyboard[shift_key:] + Keyboard[:shift_key]

    encrypted = []
    for char in password:
        index = Keyboard.find(char)
        encrypted.append(shifted[index])
    encrypted.append(str(password[0]))

    # Adding 4 random characters from keyboard to the encrypted password
    for i in range(4):
        Temp = random.randrange(1,86) # temporary holds a random number
        encrypted.append(str(Keyboard[Temp]))

    return "".join(encrypted)

encrypted_pw = encryption(password)
print("Encryption: ",encrypted_pw)


def decryption(encrypted_password):
    length = len(encrypted_password)
    Keyboard = "(l@p?si!3=g0Z5>2-TBUzx]7tGVHw8&.[4_n}F{O9^ENKhD6v:f$XdPeaAq1yYCmI,JojMk)*S%#u<bcRrLQ;W+"

    encrypted_text= encrypted_password[:-4] # Removal of unnessesary last 4 characters

    #Linear search function to find position
    def linear_search(char):
        find = str(char)
        for i in range(len(Keyboard)):
            if Keyboard[i] == find:
                position = i + 1
                break
        return position

    first_char = encrypted_text[- 1] # first character of the actual password
    FCA = linear_search(first_char)  # first character of the actual password
    FCE = linear_search(encrypted_text[0]) # position of first character of encrypted password

    shift_key = FCE - FCA # Difference gives the shift key (length of actual password)

    shifted = Keyboard[shift_key:] + Keyboard[:shift_key]

    decrypted = []

    for char in encrypted_text:
        index = shifted.find(char)
        decrypted.append(Keyboard[index])
    decrypted.pop() # remove the first character of the actual password

    return "".join(decrypted)

decrypted_text= decryption(encrypted_pw)
print("Decryption: ",decrypted_text)