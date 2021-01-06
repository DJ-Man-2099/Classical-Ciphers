from copy import deepcopy
from os import path
from string import ascii_lowercase
import numpy as np

def caesar(text, key):
    """
    This Function implements the Caesar Cipher

    Tt takes the text(string) to be Ciphered, 
    and the key(integer) for ciphering, 

    and returns the ciphered text
    """
    shift = ord('a')
    try:
        if not isinstance(key, int):
            raise TypeError("Key is not an Integer")
        if not isinstance(text, str):
            raise TypeError("Text is not a String")
        text = list(text.lower())
        for index in range(len(text)):
            if not text[index].isalpha():
                continue
            alt = (((ord(text[index])-shift)+key) % 26)+shift
            text[index] = chr(alt)
        text = ''.join(text)
        return text
    except TypeError as e:
        print(e)

def innerPlayFair(text, keyArray):
    for index in range(len(text)//2):
        # find indices
        indices = getIndices(text, keyArray, index)
        # check corner case
        newIndices = getNewIndices(indices)
        # switch
        text[index*2]=keyArray[newIndices[0][0]][newIndices[0][1]]
        text[index*2+1]=keyArray[newIndices[1][0]][newIndices[1][1]]
    return text

def getNewIndices(indices):
    newIndices = list()
    if indices[0][0]==indices[1][0]:
        newIndices.append([indices[0][0],(indices[0][1]+1)%5])
        newIndices.append([indices[1][0],(indices[1][1]+1)%5])
    elif indices[0][1]==indices[1][1]:
        newIndices.append([(indices[0][0]+1)%5,indices[0][1]])
        newIndices.append([(indices[1][0]+1)%5,indices[1][1]])
    else:
        newIndices.append([indices[0][0],indices[1][1]])
        newIndices.append([indices[1][0],indices[0][1]])
    return newIndices

def getIndices(text, keyArray, index):
    indices = list()
    # find first index
    for row in range(5):
        if text[index*2]=='i'or text[index*2]=='j':
            if keyArray[row].count('ij')!=0:
                indices.append([row,keyArray[row].index('ij')])
                break
        elif keyArray[row].count(text[index*2])!=0:
            indices.append([row,keyArray[row].index(text[index*2])])
            break
    # find second index
    for row in range(5):
        if text[index*2+1]=='i'or text[index*2+1]=='j':
            if keyArray[row].count('ij')!=0:
                indices.append([row,keyArray[row].index('ij')])
                break
        elif keyArray[row].count(text[index*2+1])!=0:
            indices.append([row,keyArray[row].index(text[index*2+1])])
            break
    return indices

def setText(text):
    temp = list(text)
    i = 0
    length = len(temp)-1
    while i < length:
        if temp[i]==temp[i+1] and temp[i]!='x':
            temp = temp[:i+1]+['x']+temp[i+1:]
        elif temp[i]==temp[i+1] and temp[i]=='x':
            temp = temp[:i+1]+['q']+temp[i+1:]
        i += 1
        length = len(temp)-1
    if len(temp)%2 !=0:
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

def playFair(text, key):
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
    text = innerPlayFair(text, keyArray)
    return ''.join(text)

def Hill(text, key):
    """
    This is the Hill Cipher

    It takes a String, and a key

    and returns the encrypted text
    """
    
    text = list(text)
    size = len(key)
    count = (size - (len(text)%size))%size
    if len(text)%size != 0:
        for i in range(count):
            text.append('X')
    shift = ord('A')
    temp = list()
    for letter in text:
        temp.append(ord(letter)-shift)
    temp = np.array(temp)
    plain = np.reshape(temp,(size, -1))
    print(plain)
    print(key)
    cipher = np.matmul(key,plain)%26
    cipher = list(np.array(np.reshape(cipher, -1))[0])
    print(cipher)
    temp = list()
    for letter in cipher:
        temp.append(chr(letter+shift))
    text = ''.join(temp[:len(temp)-count])
    print(text)
    


    

    

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
            temp = text[len(text)-1:]
            if text[len(text)-1:] == '\n':
                file.write(playFair(text=text[:len(text)-1], key=key)+'\n')
            else:
                file.write(playFair(text=text, key=key))
    print("Default PlayFair Cipher Done")

def defaultCaesar():
    abs_path = path.split(path.abspath(__file__))[0]
    file_path = path.join(abs_path, 'Input Files/Caesar/caesar_plain.txt')
    file = open(file_path, 'r')
    caesarPlain = file.readlines()
    file.close()
    for key in [3, 6, 12]:
        file_path = path.join(
            abs_path, f'Input Files/Caesar/caesar_ciphered_{key}.txt')
        file = open(file_path, 'w')
        for text in caesarPlain:
            if text[len(text)-1:] == '\n':
                file.write(caesar(text=text[:len(text)-1], key=key)+'\n')
            else:
                file.write(caesar(text=text, key=key))
    print("Default Caesar Cipher Done") 

""" defaultCaesar()
defaultPlayFair() """
Hill('VVMSQFGA',np.matrix('5 17; 8 3'))
