import string
import random
import time

def AutoGenerate():

    # Each set of characters in a charatacter type is assigned a variable

    upper = string.ascii_uppercase
    lower = string.ascii_lowercase
    digits = string.digits
    symbols = "!@#$%^&*()-_=+[]{};:,.<>?"

    character_type = [upper, lower, digits, symbols]

    # Creation of password with 4 characters in each character type
    password_chars = []

    for i in range(0, 4):
        for j in range(0, 4):
            password_chars.append(random.choice(character_type[i]))
            

    # Shuffle code for password_chars
    shuffled = []
    while len(password_chars) > 0:
        rand_index = random.randrange(0, len(password_chars))
        shuffled.append(password_chars[rand_index])
        password_chars.pop(rand_index)
    password_chars = shuffled

    # Combine the password characters to a string

    password = ""
    for i in range(0, len(password_chars)):
        password = password + password_chars[i]
    return password



def strength_checker():
    password = "u3zU{zk:r-SPN6C4xq#"
    print("Password: ",password)
    length = len(password)
    score = 0
    cU = 0
    cL = 0
    cD = 0
    cS = 0

    #Length score

    if length >= 12:
        score = score + 2
    elif 8 <= length < 12:
        score = score + 1
    else:
        score = score - 1

    #Character variation score
    upper = string.ascii_uppercase
    lower = string.ascii_lowercase
    digits = string.digits
    symbols = "!@#$%^&*()-_=+[]{};:,.<>?"

    # Uppercase check
    for i in range(length):
        for j in range(len(upper)):
            if password[i] == upper[j]:
                cU += 1

    # Lowercase check
    for i in range(length):
        for j in range(len(lower)):
            if password[i] == lower[j]:
                cL += 1

    # Digit check
    for i in range(length):
        for j in range(len(digits)):
            if password[i] == digits[j]:
                cD += 1

    # Symbol check
    for i in range(length):
        for j in range(len(symbols)):
            if password[i] == symbols[j]:
                cS += 1

    character = [cU, cL, cD, cS]

    for i in range(0, len(character)):
        current = character[i]
        if current == 0:
            score = score - 2
        elif current == 1:
            score = score + 2
        elif current > 1:
            score = score + 4
    print("Score:",score)
    # status
    if score >= 14:
            print("Strong")
    elif 9 < score <= 13:
            print("Medium strong")
    else:
            print("Weak")

strength_checker()