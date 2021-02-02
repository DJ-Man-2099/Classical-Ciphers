from copy import deepcopy
from math import ceil
from os import path
from string import ascii_lowercase
import numpy as np
import gmpy2

# Individual part


def caesar(text, key, mode=True):
    """
    This Function implements the Caesar Cipher

    Tt takes the text(string) to be Ciphered, 
    and the key(integer) for ciphering, 

    and returns the ciphered text
    """
    shift = ord('a')
    try:
        if not (isinstance(key, str) and key.isdigit()):
            raise TypeError("Key is not an Integer")
        if not isinstance(text, str):
            raise TypeError("Text is not a String")
        key = int(key)
        text = list(text.lower())
        for index in range(len(text)):
            if not text[index].isalpha():
                continue
            alt = forward(text, key, shift, index) if mode else reverse(
                text, key, shift, index)
            text[index] = chr(alt)
        text = ''.join(text)
        return text
    except TypeError as e:
        print(e)


def forward(text, key, shift, index):
    alt = (((ord(text[index])-shift)+key) % 26)+shift
    return alt


def reverse(text, key, shift, index):
    alt = (((ord(text[index])-shift)-key) % 26)+shift
    return alt


def innerPlayFair(text, keyArray, mode):
    for index in range(len(text)//2):
        # find indices
        indices = getIndices(text, keyArray, index)
        # check corner case
        newIndices = getNewIndices(
            indices) if mode else getInvNewIndices(indices)
        # switch
        text[index*2] = keyArray[newIndices[0][0]][newIndices[0][1]]
        text[index*2+1] = keyArray[newIndices[1][0]][newIndices[1][1]]
    return text


def getNewIndices(indices):
    newIndices = list()
    if indices[0][0] == indices[1][0]:
        newIndices.append([indices[0][0], (indices[0][1]+1) % 5])
        newIndices.append([indices[1][0], (indices[1][1]+1) % 5])
    elif indices[0][1] == indices[1][1]:
        newIndices.append([(indices[0][0]+1) % 5, indices[0][1]])
        newIndices.append([(indices[1][0]+1) % 5, indices[1][1]])
    else:
        newIndices.append([indices[0][0], indices[1][1]])
        newIndices.append([indices[1][0], indices[0][1]])
    return newIndices


def getInvNewIndices(indices):
    newIndices = list()
    if indices[0][0] == indices[1][0]:
        newIndices.append([indices[0][0], (indices[0][1]-1) % 5])
        newIndices.append([indices[1][0], (indices[1][1]-1) % 5])
    elif indices[0][1] == indices[1][1]:
        newIndices.append([(indices[0][0]-1) % 5, indices[0][1]])
        newIndices.append([(indices[1][0]-1) % 5, indices[1][1]])
    else:
        newIndices.append([indices[0][0], indices[1][1]])
        newIndices.append([indices[1][0], indices[0][1]])
    return newIndices


def getIndices(text, keyArray, index):
    indices = list()
    # find first index
    for row in range(5):
        if text[index*2] == 'i' or text[index*2] == 'j':
            if keyArray[row].count('ij') != 0:
                indices.append([row, keyArray[row].index('ij')])
                break
        elif keyArray[row].count(text[index*2]) != 0:
            indices.append([row, keyArray[row].index(text[index*2])])
            break
    # find second index
    for row in range(5):
        if text[index*2+1] == 'i' or text[index*2+1] == 'j':
            if keyArray[row].count('ij') != 0:
                indices.append([row, keyArray[row].index('ij')])
                break
        elif keyArray[row].count(text[index*2+1]) != 0:
            indices.append([row, keyArray[row].index(text[index*2+1])])
            break
    return indices


def setText(text):
    temp = list(text.lower())
    i = 0
    length = len(temp)-1
    while i < length:
        if temp[i] == temp[i+1] and temp[i] != 'x':
            temp = temp[:i+1]+['x']+temp[i+1:]
        elif temp[i] == temp[i+1] and temp[i] == 'x':
            temp = temp[:i+1]+['q']+temp[i+1:]
        i += 1
        length = len(temp)-1
    if len(temp) % 2 != 0:
        temp.append('x')
    return temp


def setKey(key):
    keyArray = list()
    keyIndex = 0
    remain = deepcopy(ascii_lowercase)
    remainIndex = 0
    key = ''.join(dict.fromkeys(key))
    for letter in key:
        if letter == 'i':
            remain = remain.replace(letter, '')
            remain = remain.replace('j', '')
        elif letter == 'j':
            remain = remain.replace(letter, '')
            remain = remain.replace('i', '')
        else:
            remain = remain.replace(letter, '')
    for row in range(5):
        keyArray.append([])
        for column in range(5):
            if keyIndex < len(key):
                if key[keyIndex] == 'i':
                    keyArray[row].append(key[keyIndex]+'j')
                elif key[keyIndex] == 'j':
                    keyArray[row].append('i'+[keyIndex])
                else:
                    keyArray[row].append(key[keyIndex])
                keyIndex += 1
            else:
                if remain[remainIndex] == 'i':
                    keyArray[row].append(remain[remainIndex]+'j')
                    remain = remain.replace('j', '')
                elif remain[remainIndex] == 'j':
                    keyArray[row].append('i'+remain[remainIndex])
                    remain = remain.replace('i', '')
                else:
                    keyArray[row].append(remain[remainIndex])
                remainIndex += 1
    return keyArray


def playFair(text, key, mode=True):
    """
    This is the PlayFair Cipher

    It takes a pair of letters,
    and replaces them based on the key
    """

    # Set Key matrix
    keyArray = setKey(key)

    # Set Text before encrypting
    text = setText(text)

    # Encrypt Text
    text = innerPlayFair(text, keyArray, mode)
    return ''.join(text)


def Hill(text, key, mode=True):
    """
    This is the Hill Cipher

    It takes a String, and a key

    and returns the encrypted text
    """
    text = text.upper()
    text = list(text)
    key = np.matrix(key)
    if not mode:
        key = inverse(key)
    size = len(key)
    count = (size - (len(text) % size)) % size
    if len(text) % size != 0:
        for i in range(count):
            text.append('X')
    shift = ord('A')
    temp = list()
    for letter in text:
        temp.append(ord(letter)-shift)
    temp = np.array(temp)
    # print(size)
    plain = np.reshape(temp, (-1, size)).transpose()
    """ print(plain)
    print(key) """
    cipher = (np.dot(key, plain) % 26).transpose()
    cipher = list(np.array(np.reshape(cipher, -1))[0])
    # print(cipher)
    temp = list()
    for letter in cipher:
        temp.append(chr(letter+shift))
    text = ''.join(temp)
    # print(text)
    return text


def inverse(array):
    newArray = deepcopy(array)
    deter = np.rint(np.linalg.det(array)).astype(int)
    newArray = np.rint(np.linalg.inv(newArray)*deter).astype(int) % 26
    deter = int(str(gmpy2.rint(gmpy2.invert(gmpy2.mpz(deter % 26), 26)))[:-2])
    newArray = (newArray*deter) % 26
    return newArray


def Vigenere(text, key, mode, enc=True):
    """
    This is the Vigenere Cipher

    ...

    Attributes
    ----------
    for Auto Mode, set mode=true

    for repeated mode, set mode=false
    """
    textSize = len(text)
    keySize = len(key)
    trueKey = ''
    cipher = ''
    text = text.lower()
    key = key.lower()
    if mode:  # auto mode
        trueKey += key
        if enc:
            for letter in range(textSize):  # ciphering
                cipher += chr((ord(text[letter])-ord('a') +
                               (ord(trueKey[letter])-ord('a'))) % 26+ord('a'))
                trueKey += text[letter]
        else:
            for letter in range(textSize):  # deciphering
                cipher += chr((ord(text[letter])-ord('a') -
                               (ord(trueKey[letter])-ord('a'))) % 26+ord('a'))
                trueKey += cipher[-1]

    else:  # repeat mode
        trueKey += key*(ceil(textSize/keySize))
    # print(trueKey)
        if enc:
            for letter in range(textSize):  # ciphering
                cipher += chr((ord(text[letter])-ord('a') +
                               (ord(trueKey[letter])-ord('a'))) % 26+ord('a'))
        else:
            for letter in range(textSize):  # deciphering
                cipher += chr((ord(text[letter])-ord('a') -
                               (ord(trueKey[letter])-ord('a'))) % 26+ord('a'))

    return cipher


def Vernam(text, key, mode=True):
    """
    This is the Vernam Cipher

    ...

    Key can't be Shorter than the text
    """
    text = text.upper()
    key = key.upper()
    textSize = len(text)
    keySize = len(key)
    cipher = ''
    if keySize < textSize:
        raise ValueError("Key can't be Shorter than the text")
    if mode:
        for letter in range(textSize):  # ciphering
            cipher += chr((ord(text[letter])-ord('A') +
                           (ord(key[letter])-ord('A'))) % 26+ord('A'))
    else:
        for letter in range(textSize):  # deciphering
            cipher += chr((ord(text[letter])-ord('A') -
                           (ord(key[letter])-ord('A'))) % 26+ord('A'))

    return cipher


# Default part
def defaultCaesar():
    # try:
    abs_path = path.split(path.abspath(__file__))[0]
    file_path = path.join(abs_path, 'Input Files/Caesar/caesar_plain.txt')
    file = open(file_path, 'r')
    caesarPlain = file.readlines()
    file.close()
    for key in ['3', '6', '12']:
        file_path = path.join(
            abs_path, f'Input Files/Caesar/caesar_ciphered_{key}.txt')
        file = open(file_path, 'w')
        for text in caesarPlain:
            if text[len(text)-1:] == '\n':
                file.write(caesar(text=text[:len(text)-1], key=key)+'\n')
            else:
                file.write(caesar(text=text, key=key))
    print("Default Caesar Cipher Done")
    # except:
    #raise FileNotFoundError("Files Don't exist in the specified path")


def defaultPlayFair():
    abs_path = path.split(path.abspath(__file__))[0]
    file_path = path.join(abs_path, 'Input Files/PlayFair/playfair_plain.txt')
    file = open(file_path, 'r')
    playFairPlain = file.readlines()
    file.close()
    for key in ["rats", "archangel"]:
        file_path = path.join(
            abs_path, f'Input Files/PlayFair/playfair_ciphered_{key}.txt')
        file = open(file_path, 'w')
        for text in playFairPlain:
            if text[len(text)-1:] == '\n':
                file.write(playFair(text=text[:len(text)-1], key=key)+'\n')
            else:
                file.write(playFair(text=text, key=key))
    print("Default PlayFair Cipher Done")


def defaultHill():
    abs_path = path.split(path.abspath(__file__))[0]
    file_path = path.join(abs_path, 'Input Files/Hill/hill_plain_2x2.txt')
    file = open(file_path, 'r')
    playFairPlain = file.readlines()
    file.close()
    key = "5 17; 8 3"

    file_path = path.join(
        abs_path, f'Input Files/Hill/hill_ciphered_2x2.txt')
    file = open(file_path, 'w')
    for text in playFairPlain:
        temp = text[len(text)-1:]
        if text[len(text)-1:] == '\n':
            file.write(Hill(text=text[:len(text)-1], key=key)+'\n')
        else:
            file.write(Hill(text=text, key=key))

    file_path = path.join(abs_path, 'Input Files/Hill/hill_plain_3x3.txt')
    file = open(file_path, 'r')

    key = "2 4 12; 9 1 6; 7 5 3"

    file_path = path.join(
        abs_path, f'Input Files/Hill/hill_ciphered_3x3.txt')
    file = open(file_path, 'w')
    for text in playFairPlain:
        temp = text[len(text)-1:]
        if text[len(text)-1:] == '\n':
            file.write(Hill(text=text[:len(text)-1], key=key)+'\n')
        else:
            file.write(Hill(text=text, key=key))

    print("Default Hill Cipher Done")


def defaultVigenere():
    abs_path = path.split(path.abspath(__file__))[0]
    file_path = path.join(abs_path, 'Input Files/Vigenere/vigenere_plain.txt')
    file = open(file_path, 'r')
    VigenerePlain = file.readlines()
    file.close()

    key = "pie"
    file_path = path.join(
        abs_path, f'Input Files/Vigenere/vigenere_ciphered_{key}_Repeated.txt')
    file = open(file_path, 'w')
    for text in VigenerePlain:
        if text[len(text)-1:] == '\n':
            file.write(
                Vigenere(text=text[:len(text)-1], key=key, mode=False)+'\n')
        else:
            file.write(Vigenere(text=text, key=key, mode=False))

    key = "aether"
    file_path = path.join(
        abs_path, f'Input Files/Vigenere/vigenere_ciphered_{key}_Auto.txt')
    file = open(file_path, 'w')
    for text in VigenerePlain:
        if text[len(text)-1:] == '\n':
            file.write(
                Vigenere(text=text[:len(text)-1], key=key, mode=True)+'\n')
        else:
            file.write(Vigenere(text=text, key=key, mode=True))

    print("Default Vigenere Cipher Done")


def defaultVernam():
    abs_path = path.split(path.abspath(__file__))[0]
    file_path = path.join(abs_path, 'Input Files/Vernam/vernam_plain.txt')
    file = open(file_path, 'r')
    VernamPlain = file.readlines()
    file.close()

    key = "SPARTANS"
    file_path = path.join(
        abs_path, f'Input Files/Vernam/vernam_ciphered_{key}.txt')
    file = open(file_path, 'w')
    for text in VernamPlain:
        if text[len(text)-1:] == '\n':
            file.write(
                Vernam(text=text[:len(text)-1], key=key)+'\n')
        else:
            file.write(Vernam(text=text, key=key))

    print("Default Vernam Cipher Done")


""" defaultCaesar()
defaultPlayFair() 
defaultHill() 
defaultVigenere() 
defaultVernam() """


request = ''
print("Welcome to the Classical Ciphers Software:")
request = input("Please enter 's' to Start Ciphering  or 'e' to exit: ")
while request not in ['s', 'e']:
    print("invalid request, please try again")
    request = input("Please enter 's' to Start Ciphering  or 'e' to exit: ")
choice = ''
plain = ''
key = ''
mode = ''
secMode = ''
ciphers = {
    'c': caesar,
    'p': playFair,
    'h': Hill,
    'vi': Vigenere,
    've': Vernam
}
defaultCiphers = {
    'c': defaultCaesar,
    'p': defaultPlayFair,
    'h': defaultHill,
    'vi': defaultVigenere,
    've': defaultVernam
}
while request != 'e':
    print("Enter 'c' for Caeser, 'p' for PlayFair,")
    print("Enter 'h' for Hill, 'vi' for Vigenere, and 've' for Vernam")
    choice = input(
        "Choose a cipher method, or enter 'e' to return to main menu: ")
    if choice != 'e':
        if choice not in ['c', 'p', 'h', 'vi', 've']:
            while choice not in ['c', 'p', 'h', 'vi', 've', 'e']:
                print('invalid cipher method, please try again')
                print("Enter 'c' for Caeser, 'p' for PlayFair,")
                print("Enter 'h' for Hill, 'vi' for Vigenere, and 've' for Vernam")
                choice = input(
                    "Choose a cipher method, or enter 'e' to return to main menu: ")
            if choice == 'e':
                request = input(
                    "Please enter 's' to Start Ciphering  or 'e' to exit: ")
                if request == 's':
                    continue
                elif request == 'e':
                    break
                else:
                    while request not in ['s', 'e']:
                        print("invalid request, please try again")
                        request = input(
                            "Please enter 's' to Start Ciphering  or 'e' to exit: ")
                    if request == 's':
                        continue
                    elif request == 'e':
                        break

        mode = input(
            "Enter 'd' for default mode, 'i' to manually input text, or 'e' to return to main menu: ")
        if mode == 'd':
            try:
                defaultCiphers[choice]()
            except FileNotFoundError as e:
                print(
                    "Please ensure the files are in the pre-specified location \n(under Input Files)")
        elif mode == 'i':
            enc = input("Enter 'e' for encryption, 'd' for decryption: ")
            plain = input("Enter the Plain Text: ")
            if choice == 'h':
                key = input("Enter the key in matrix form (i.e: 3 5; 6 7): ")
            else:
                key = input("Enter the key: ")
            if choice == 'vi':
                secMode = input(
                    "Enter 'a' for auto mode, 'r' for repeated mode: ")
                print("The ciphered Text is: " +
                      ciphers[choice](plain, key, secMode == 'a', enc == 'e'))
            else:
                print("The ciphered Text is: " +
                      ciphers[choice](plain, key, enc == 'e'))
        elif mode != 'e':
            while mode != 'd' or mode != 'i' or mode != 'e':
                print('choice not understood, please try again')
                mode = input(
                    "Enter 'd' for default mode, 'i' to cipher input text, or 'e' to return to main menu: ")
                if mode == 'd':
                    try:
                        defaultCiphers[choice]()
                    except FileNotFoundError as e:
                        print(
                            "Please ensure the files are in the pre-specified location \n(under Input Files)")
                    finally:
                        break
                elif mode == 'i':
                    enc = input(
                        "Enter 'e' for encryption, 'd' for decryption: ")
                    plain = input("Enter the Plain Text: ")
                    if choice == 'h':
                        key = input(
                            "Enter the key in matrix form (i.e: 3 5; 6 7): ")
                    else:
                        key = input("Enter the key: ")
                    if choice == 'vi':
                        secMode = input(
                            "Enter 'a' for auto mode, 'r' for repeated mode: ")
                        print("The ciphered Text is: " +
                              ciphers[choice](plain, key, secMode == 'a', enc == 'e'))
                    else:
                        print("The ciphered Text is: " +
                              ciphers[choice](plain, key, enc == 'e'))
                    break
    request = input(
        "Please enter \"s\" to Start Ciphering  or \"e\" to exit: ")
    while request not in ['s', 'e']:
        print("invalid request, please try again")
        request = input(
            "Please enter 's' to Start Ciphering  or 'e' to exit: ")
    if request == 's':
        continue
    elif request == 'e':
        break
