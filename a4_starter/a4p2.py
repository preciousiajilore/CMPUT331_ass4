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
#---------------------------------------------------------------

"""
Nomenclator cipher
February 2026
Author: Precious Ajilore
"""

"""
NOTE: So basically we are looking at each word in the message, and if it is in the codebook,
we replace it with the corresponding code. Note that codebook the matching is case-insensitive,
so we can convert the word to lowercase before checking the codebook.
If it is not in the codebook, we apply a substitution cipher to each letter in the word using the provided key. 
The key is a permutation of the alphabet, where the position of each letter corresponds to its substitution.
For example, if the key is 'LFWOAYUISVKMNXPBDCRJTQEGHZ', then 'A' would be replaced by 'L', 'B' by 'F', 'C' by 'W', 
and so on.

"""

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

#---HELPER FUNCTIONS----
def substitute(ch: str, key: str, mode: str) -> str:
    """
    Substitutes a character using the given key.
    If mode is 'encrypt', returns the substitution for ch in the key.
    If mode is 'decrypt', returns the character that maps to ch in the key.
    """
    if ch.upper() not in LETTERS:
        return ch  # Non-alphabetic characters are unchanged
    

 
    if mode == 'encrypt':
            indx = LETTERS.index(ch.upper())
            mapped = key[indx]
    elif mode == 'decrypt':
            indx = key.index(ch.upper())
            mapped = LETTERS[indx]

    #return the mapped character, preserving the case of the original character
    return mapped if ch.isupper() else mapped.lower()
#-------------------------------------------------------------------------------


def translateMessage(key: str, message: str, codebook: dict, mode: str):
    """
    Encrypt or decrypt using a nomenclator.
    Takes a substitution cipher key, a message (plaintext or ciphertext),
    a codebook dictionary, and a mode string ('encrypt' or 'decrypt')
    specifying the action to be taken. Returns a string containing the
    ciphertext (if encrypting) or plaintext (if decrypting).

    """
    #Make the codebook case-insensitive by converting all keys to lowercase
    codebook = {k.lower(): v for k, v in codebook.items()}

    #make a reverse codebook for decryption
    #reverse_codebook = {v[0].lower(): k for k, v in codebook.items()}
    reverse_codebook = {}
    for word, symbols in codebook.items():
        for symbol in symbols:
            reverse_codebook[symbol.lower()] = word

    #Split the message into words and process each word
    translated_words = []
    for word in message.split():
        #for each token, split into prefix, core word (middle of the word), suffix
        prefix = ''
        suffix = ''
        core_word = word
        #Extract prefix (non-alphabetic characters at the beginning)
        while core_word and not core_word[0].isalpha():
            prefix += core_word[0]
            core_word = core_word[1:]

        #Extract suffix (non-alphabetic characters at the end)
        while core_word and not core_word[-1].isalpha():
            suffix = core_word[-1] + suffix
            core_word = core_word[:-1]

        #Now core_word should contain only the alphabetic characters
        if mode == 'encrypt':
            #find te index of the plaintext in the codebook, replace with key[index]
            if core_word and core_word.lower() in codebook:
                 translated_words.append(prefix + codebook[core_word.lower()][0] + suffix)
            else:
                token = ''.join(substitute(ch, key, mode) for ch in core_word)
                translated_words.append(prefix + token + suffix)
        
        if mode == "decrypt":
            #find the index of the ciphertext in the reverse codebook
            if core_word and core_word.lower() in reverse_codebook:
                translated_words.append(prefix + reverse_codebook[core_word.lower()] + suffix)
            else:
                token = ''.join(substitute(ch, key, mode) for ch in core_word)
                translated_words.append(prefix + token + suffix)
    
    return ' '.join(translated_words)


def encryptMessage(key: str, message: str, codebook: dict):
    return translateMessage(key, message, codebook, 'encrypt')


def decryptMessage(key: str, message: str, codebook: dict):
    return translateMessage(key, message, codebook, 'decrypt')


def test():
    # Provided tests.
    key = 'LFWOAYUISVKMNXPBDCRJTQEGHZ'
    plaintext = "X-ray machines cannot be brought here, as -ray* are very dangerous. Hello;ray! ray;"
    codebook = {'ray':['1']}
    ciphertext = encryptMessage(key, plaintext, codebook)
    assert ciphertext=="G-clh nlwisxar wlxxpj fa fcptuij iaca, lr -1* lca qach olxuacptr. Iammp;clh! 1;"
    # End of provided tests.

if __name__ == '__main__':
    test()
