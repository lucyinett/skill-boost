import numpy as np
import re

import json


def normalize_vector_linalg(vector):
    norm = np.linalg.norm(vector)
    normalized_vector = vector / norm if norm != 0 else vector
    return normalized_vector


"""Extracting the NLP terms from the wikipedia dictionary"""
def extract_dictionary_words(text):
    # Split text into lines
    lines = text.split('\n')
    dictionary_words = []

    # Define a regular expression pattern for dictionary entries
    pattern = r'^\b[a-z]+\b(?:\s+[a-z]+\b)*$'

    acronym_pattern = r'^\([A-Z]+\)$'

    punctuation_pattern = r'[^\w\s(?!)]'
    ref_pattern = r'^\([0-9]+\)$'


    # Iterate through each line and extract dictionary words
    for line in lines:
        dictionary_item = {}
        size = len(line.split())

        # print("Number of words in the line: " + str(size))
        if (size > 0 and
                not line.split()[0].lower() == "the" and
                not line.split()[0].lower() == "a" and
                not len(line.split()[0]) == 1

                             ):
            # if the line is all lowercase
            if line.islower():
     
                dictionary_item["phrase"] = line
                dictionary_item["acronym"] = None
            # if the line is just one word but not a single letter
            elif len(line.split()) == 1 and not len(line.split()[0]) == 1:
                #dictionary_words.append(line + ": one word match")
                dictionary_item["phrase"] = line.lower()
                dictionary_item["acronym"] = None
            # if the line has an acronym ([A-Z]+) at the end
            elif re.match(acronym_pattern, line.split()[size-1]):
                line = line.lower()
                arr = line.split()
                acronym = arr.pop()
                phrase = ' '.join(arr)
                
                dictionary_item["phrase"] = phrase
               
                dictionary_item["acronym"] = acronym

            elif not re.search(punctuation_pattern, line):
                dictionary_item["phrase"] = line.lower()
                dictionary_item["acronym"] = None

            if line.lower().split()[0] == "also":
                # the previous dictionary item needs to be edited
                prev_item = dictionary_words[len(dictionary_words) - 1]
              
                line = line.lower()
                aka = line.strip("also")
                if aka.split()[0] == "simply":
                    simply = aka.split()
                    simply.pop(0)
                    no_simply = ' '.join(simply)
                else:
                    no_simply = aka

                aka_word = no_simply.split(".")[0]
           
                no_ref = re.sub(r'\[\d+\]', '', aka_word)


                if ", differs" in no_ref:
                    clean_sent = no_ref.split(", differs")[0]

                elif "due to" in no_ref:
                    clean_sent = no_ref.split("due to")[0]
                elif ", is a" in no_ref:
                    clean_sent = no_ref.split(", is a")[0]

                else:
                    clean_sent = no_ref

                print("AKA is of {} is : {}".format(prev_item["phrase"], clean_sent))
                prev_item["aka"] = clean_sent


            if dictionary_item:
                dictionary_words.append(dictionary_item)


    return dictionary_words



    





