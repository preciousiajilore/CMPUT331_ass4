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
Enhanced substitution cipher solver
February 2026
Author: Precious Ajilore
"""

import re
import simpleSubHacker as ssh

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def hackSimpleSub(message: str):
    """
    Simple substitution cipher hacker.
    First runs the textbook program to get an initial, potentially incomplete decipherment.
    Then uses regular expressions and a dictionary to decipher additional letters.

    run the simpleSubHacker to get a partial key/mapping, and a partially decrypted message that still has blanks for letters it couldn't figure out.
    then i jave to fill in the missing letters using dictionary-based pattern matching while keeping the one to one constraint of substitutuon keys.
    """
    #get initial mapping 
    #each cipher lettetr maps to a list of possible plaintext letters i think lol
    letterMapping = ssh.hackSimpleSub(message)

    #build the cipher -> plaintext for solved letters, this is for confirmed mappings
    fixed = {} 
    used_plain = set() #plaintext letters that are already used by a cipher lettter because subsititution is one to one
    
    #
    for c in LETTERS:
        if len(letterMapping[c]) == 1:
            p = letterMapping[c][0]
            fixed[c] = p
            used_plain.add(p)
    

    #load the dictionary
    dictionary = []
    with open('dictionary.txt', 'r') as f:
        for line in f:
            w = line.strip()
            if w and w.isalpha():
                dictionary.append(w.upper())
    
    #idea for this is using the length of cipher text to look up words matching that same length instead of looking through the entired dictionary
    dict_len = {}
    for w in dictionary:
        dict_len.setdefault(len(w), []).append(w)

    #start filling in the letters and keep doing so until i dont make any prohress, like discover a new letter mapping in each iteration
    changed = True
    while changed:
        changed = False

        #apply the fixed mapping, so we have a partially decrypted text based on what we know is the ciphertext->plaintext
        partial = mapping(message, fixed)

        cip_word = re.findall(r"[A-Za-z]+", message)
        partial_word = re.findall(r"[A-Za-z_]+", partial)


        for cw , pw in zip(cip_word, partial_word):
            #for each word, try the dictionary match 
            cw = cw.upper()
            pw = pw.upper()

            #skip words that are already solved so pw doesnt have a "_" in it
            if '_' not in pw:
                continue
            
            #chheck the dictionary for words of the same length
            L = len(cw)
            candidates = dict_len.get(L, [])
            if not candidates:
                continue

            # build a regex from the partially-known plaintext word
            # e.g. "O__ER" -> "^O..ER$" so "." is possible char, ^ is beginning of word and $ is end of word
            pattern = '^' + pw.replace('_', '.') + '$'
            rgx = re.compile(pattern)

            valid = []
            for candidate in candidates:
                # must match known letters
                if not rgx.match(candidate):
                    continue
                # check to see if the candidate  consistent with substitution rules  and repeated letters
                if it_fits(cw, candidate, fixed, used_plain):
                    valid.append(candidate)

                #too many words not informative
                if len(valid) > 20:
                    break

            # if exactly one candidate fits, then take it
            if len(valid) == 1:
                #basically commit that mapping cause one fits exactly
                make_map(cw, valid[0], fixed, used_plain)
                changed = True

    #return final plaintext
    final = mapping(message, fixed)

    return final


def mapping(text:str, fixed) -> str:
    #apply the fixed mapping that we originlly found to this essage and use underscores for the letters we dont know 
    output = []
    for char in text:
        x = char.upper()
        if x in LETTERS:
            if x in fixed:
                mapped = fixed[x]
                output.append(mapped if char.isupper() else mapped.lower())
            else:
                output.append('_')
        else:
            output.append(char)
    
    return ''.join(output)

def it_fits(cipherword: str, plainword: str, fixed: dict, used_plain: set):
    #temporary copies
    temp_fixed = dict(fixed)
    temp_plain = set(used_plain)


    for cipword, plword in zip(cipherword, plainword):
        #if the cipword has as an assigned, it must match
        if cipword in temp_fixed:
            if temp_fixed[cipword] != plword:
                #look it up and check if the cipherword matching is the same
                return False
        else:
            #try not to reuse the plaintext letter that has already been used by another cipher which is why used_plain is a set so we can keep track of duplicates
            if plword in temp_plain:
                return False
            temp_fixed[cipword] = plword
            #add it to letters that have been used
            temp_plain.add(plword)
    
    return True

def make_map(cipherword: str, plainword: str, fixed: dict, used_plain: set):
    for cipword, plword in zip(cipherword, plainword):
        if cipword not in fixed:
            fixed[cipword] = plword
            used_plain.add(plword)



def test():
    # Provided test.
    message = 'Sy l nlx sr pyyacao l ylwj eiswi upar lulsxrj isr sxrjsxwjr, ia esmm rwctjsxsza sj wmpramh, lxo txmarr jia aqsoaxwa sr pqaceiamnsxu, ia esmm caytra jp famsaqa sj. Sy, px jia pjiac ilxo, ia sr pyyacao rpnajisxu eiswi lyypcor l calrpx ypc lwjsxu sx lwwpcolxwa jp isr sxrjsxwjr, ia esmm lwwabj sj aqax px jia rmsuijarj aqsoaxwa. Jia pcsusx py nhjir sr agbmlsxao sx jisr elh. -Facjclxo Ctrramm'
    assert(hackSimpleSub(message)=="If a man is offered a fact which goes against his instincts, he will scrutinize it closely, and unless the evidence is overwhelming, he will refuse to believe it. If, on the other hand, he is offered something which affords a reason for acting in accordance to his instincts, he will accept it even on the slightest evidence. The origin of myths is explained in this way. -Bertrand Russell")
    # End of provided test.

    #print(hackSimpleSub(message))
    

if __name__ == '__main__':
    test()
