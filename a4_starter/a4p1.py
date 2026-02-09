#!/usr/bin/env python3

#---------------------------------------------------------------
#
# CMPUT 331 Student Submission License
# Version 1.0
# Copyright 2026 Precious Ajilore
#
# Redistribution is forbidden in all circumstances. Use of this software
# without explicit authorization from the author is prohibited.
#
# This software was produced as a solution for an assignment in the course
# CMPUT 331 - Computational Cryptography at the University of
# Alberta, Canada. This solution is confidential and remains confidential 
# after it is submitted for grading.
#
# Copying any part of this solution without including this copyright notice
# is illegal.
#
# If any portion of this software is included in a solution submitted for
# grading at an educational institution, the submitter will be subject to
# the sanctions for plagiarism at that institution.
#
# If this software is found in any public website or public repository, the
# person finding it is kindly requested to immediately report, including 
# the URL or other repository locating information, to the following email
# address:
#
#          gkondrak <at> ualberta.ca
#
#----------------------------------------------------------------

#-------------------- START ASSIGNMENT HERE ---------------------
"""
General decryption program
February 2026
Author: Precious Ajilore
"""

from matplotlib import lines
from detectEnglish import isEnglish, getEnglishCount
from itertools import permutations
from cryptomath import gcd, findModInverse
import time

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

#----------CAESAR CIPHER DECRYPTION----------
def hack_caesar(ciphertext: str) -> str:
    #try all the possible key
    for key in LETTERS:
        candidate = decrypt_caesar(ciphertext, key)

        if isEnglish(candidate, wordPercentage=60, letterPercentage=85):
            return candidate
    return ciphertext  # Return the ciphertext unchanged since A = 0 shift

def decrypt_caesar(ciphertext: str, key: str) -> str:
    ciphertext = ciphertext.upper()
    key = key.upper() 

    decrypted = []
    key_shift = LETTERS.index(key)

    for char in ciphertext:
        if char in LETTERS:
            index = (LETTERS.index(char) - key_shift) % len(LETTERS)
            decrypted.append(LETTERS[index])
        else:
            decrypted.append(char)  # Non-alphabetic characters are unchanged

    return ''.join(decrypted)

#----------AFFINE CIPHER DECRYPTION----------
def decrypt_affine(ciphertext: str, a: int, b: int) -> str:
    ciphertext = ciphertext.upper()
    m = len(LETTERS) 
    a_inv = findModInverse(a, m)

    if a_inv is None:
        raise ValueError(f"No modular inverse for a={a} and m={m}. Decryption not possible.")
    
    decrypted = []
    for char in ciphertext:
        if char in LETTERS:
            c = LETTERS.index(char)
            p = (a_inv * (c - b)) % m
            decrypted.append(LETTERS[p])
        else:
            decrypted.append(char)  # Non-alphabetic characters are unchanged

    return ''.join(decrypted)


def hack_affine(ciphertext: str) -> str:
    ciphertext = ciphertext.upper()
    m = len(LETTERS)
    best_score = 0.0
    best_candidate = ciphertext

    for a in range(1, m):
        if gcd(a, m) != 1:
            continue  # Skip if a and m are not coprime

        for b in range(m):
            candidate = decrypt_affine(ciphertext, a, b)
            #print(f"Trying a={a}, b={b}: {candidate}")  # Debug output to see the candidate decryption

            score = getEnglishCount(candidate)
            if score > best_score:
                best_score = score
                best_candidate = candidate

            
    return best_candidate  # Return the best candidate decryption found


#----------TRANSPOSITION CIPHER DECRYPTION----------
def decrypt_transposition(ciphertext: str, key) -> str:
    l = len(ciphertext)
    k = len(key)

    rows = (l + k - 1) // k  # Calculate the number of rows needed
    shaded = (rows * k) - l  # Calculate the number of shaded boxes

    #column lenths in the original grid
    # first (k- shaded) columns have length rows, the rest have length rows-1
    col_lens = [rows] * k
    for col in range(k - shaded, k):
        if shaded > 0:
            col_lens[col] -= 1


    # Create an empty grid to hold the characters
    cols = [''] * k
    idx = 0

    for col in key:
        col_index = col - 1  # Convert to 0-based index
        n = col_lens[col_index]  # Number of characters in this column
        
        cols[col_index] = ciphertext[idx:idx + n]
        idx += n
    

    #read row-wise to get the decrypted message
    decrypted = []
    for row in range(rows):
        for col in range(k):
            if row < len(cols[col]):
                decrypted.append(cols[col][row])


    return ''.join(decrypted)

def hack_transposition(ciphertext: str) -> str:
    best_score = -1.0
    best_candidate = ciphertext

    for k in range(2,10):
        for key in permutations(range(1, k + 1)):
            candidate = decrypt_transposition(ciphertext, key)
            #print(f"Trying key={key}: {candidate}")  # Debug output to see the candidate decryption

            score = getEnglishCount(candidate)
            if score > best_score:
                best_score = score
                best_candidate = candidate
    
    if isEnglish(best_candidate, wordPercentage=40, letterPercentage=70):
         return best_candidate
     # Return the original ciphertext if no good candidate is found
    return ciphertext
    


#-------------------- Hack ---------------------

def hack(ciphertype: str, ciphertext: str):
    """
    Decrypt a given ciphertext with either of these algorithm: caesar, transposition, or affine.
        Input: a line from `ciphers.txt`.
        Output: the decrypted message (or plaintext).
    """
    if ciphertype == "caesar":
        # Implement Caesar cipher decryption logic here
        return hack_caesar(ciphertext)
    elif ciphertype == "transposition":
        # Implement Transposition cipher decryption logic here
        return hack_transposition(ciphertext)   
    elif ciphertype == "affine":
        # Implement Affine cipher decryption logic here
        return hack_affine(ciphertext)
    else:
        raise ValueError(f"Unknown cipher type: {ciphertype}")



def processing():
    # Add the processing steps here like reading form ciphers.txt, calling the hack function, writing to decrypted.txt, etc.
    
    #open ciphers.txt and read the lines
    #for each line: split at ";"
    #map :
    """
    C -> Caesar -> hack("caesar", ciphertext)
    T -> Transposition -> hack("transposition", ciphertext)
    A -> Affine -> hack("affine", ciphertext)
    """
    type_mapping = {
        'C': 'caesar',
        'T': 'transposition',
        'A': 'affine'
    }

    with open('ciphers.txt', 'r') as f_in, open('decrypted.txt', 'w') as f_out:
        for line in f_in:
            line = line.strip()
            if not line:
                continue  # Skip empty lines

            code, ciphertext = line.split(';', 1)
            code = code.strip()
            ciphertext = ciphertext.strip()
            cipher_type = type_mapping[code]
            plaintext = hack(cipher_type, ciphertext)
            f_out.write(plaintext + '\n')
        
    

def test():
    # Test cases for the hack function. You can add more tests as needed.
    assert hack("caesar", "GHGIQ") == "ABACK", "Caesar hack failed"
    assert hack("transposition", "IS HAUCREERNP F") == "CIPHERS ARE FUN", "Transposition hack failed"
    assert hack("affine", "IHHWVC SWFRCP") == "AFFINE CIPHER", "Affine hack failed"
    #print(hack_affine("IHHWVC SWFRCP"))  # Test the affine hack function separately to see the debug output
    #print(hack_transposition("IS HAUCREERNP F"))  # Test the transposition hack function separately to see the debug output
if __name__ == '__main__':
    time_start = time.time()
    test()
    processing()
    time_end = time.time()
    print(f"Execution time: {time_end - time_start:.2f} seconds")