# File: pos_tagging.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis


# PART B: POS tagging

#from typing import List, Any

from statements import *

# The tagset we shall use is:
# P  A  Ns  Np  Is  Ip  Ts  Tp  BEs  BEp  DOs  DOp  AR  AND  WHO  WHICH  ?

# Tags for words playing a special role in the grammar:

function_words_tags = [('a', 'AR'), ('an', 'AR'), ('and', 'AND'),
                       ('is', 'BEs'), ('are', 'BEp'), ('does', 'DOs'), ('do', 'DOp'),
                       ('who', 'WHO'), ('which', 'WHICH'), ('Who', 'WHO'), ('Which', 'WHICH'), ('?', '?')]
# upper or lowercase tolerated at start of question.

function_words = [p[0] for p in function_words_tags]


def unchanging_plurals():
    nn = set()
    nns = set()
    unchangedpl = set()  # type: List[String]
    with open("sentences.txt", "r") as f:
        for line in f:
            wordstags = line.split()
            for w in wordstags:
                if (w.split("|")[1] == "NN"):
                    nn.add(w.split("|")[0])
                elif w.split("|")[1] == "NNS":
                    nns.add(w.split("|")[0])


    for n in nn:
        if n in nns:
            unchangedpl.add(n)
    return unchangedpl


unchanging_plurals_list = unchanging_plurals()


def noun_stem(s):
    """extracts the stem from a plural noun, or returns empty string"""
    stem = ""
    vowels = 'aioeu'
    if s in unchanging_plurals_list:
        return s
    elif re.match("[a-z]+man$", s):
        stem = s[:-3] + "men"
    else:
        # ends in -ies
        if re.match("[a-z]+ies$", s):
            if len(s) == 4 and not s[0] in vowels:
                stem = s[:-1]
            elif re.match("[a-z]+[^aioeu]ies$", s):
                stem = s[:-3] + "y"

        # end in -es
        elif re.match("[a-z]+es$", s):
            if re.match("[a-z]+(o|x|ch|sh|ss|zz)es$", s):
                stem = s[:-2]
            elif re.match("[a-z]+[^(iosxz|ch|sh)]es$", s):
                stem = s[:-1]
            elif re.match("[a-z]+(s|z)es$", s) and (s[-4:] != "sses" or s[-4:] != "zzes"):
                stem = s[:-1]

        # end is -s
        elif re.match("[a-z]+s$", s):
            if re.match("[a-z]+[^(aiouesxyz|ch|sh)]s$", s):
                stem = s[:-1]
            elif re.match("[a-z]+[aioue]ys$", s):
                stem = s[:-1]
    return stem


def tag_word(lx, wd):
    """returns a list of all possible tags for wd relative to lx"""
    cats=[]
    if wd in function_words:
      return  [v[1] for v in function_words_tags if v[0] == wd] #return the tags based on function_words_tags
    #word is of tag A or P
    for c in ['A', 'P']:
        if wd in lx.getAll(c):
            cats.append(c)
   #word is Noun either singular or plural
    if (wd in lx.getAll("N")or noun_stem(wd) in lx.getAll("N")):
        if wd in unchanging_plurals_list:
            cats.append("Ns")
            cats.append("Np")
        elif noun_stem(wd)== "" :
            cats.append("Ns")
        else:
            cats.append("Np")
   #Word is verb either 3s form or normal form
    if wd in lx.getAll("T")or verb_stem(wd) in lx.getAll("T"):
        if verb_stem(wd)== "" :
            cats.append("Tp")
        else:
            cats.append("Ts")

    #Word is verb either 3s form or normal form
    if wd in lx.getAll("I")or verb_stem(wd) in lx.getAll("I"):
        if verb_stem(wd)== "" :
            cats.append("Ip")
        else:
            cats.append("Is")

    return cats

    # add code here


def tag_words(lx, wds):
    """returns a list of all possible taggings for a list of words"""
    if (wds == []):
        return [[]]
    else:
        tag_first = tag_word(lx, wds[0])
        tag_rest = tag_words(lx, wds[1:])
        return [[fst] + rst for fst in tag_first for rst in tag_rest]

# End of PART B.
def main():
    lx = Lexicon()
    lx.add("John", "P")
    lx.add("Mary", "P")
    lx.add("like", "T")
    lx.add("orange", "A")
    lx.add("orange", "N")
    lx.add("fish", "N")
    # lx.add("fish", "N")
    lx.add("fish", "I")
    lx.add("fish", "T")
    lx.add("play","T")
    lx.add('ball','N')
    print noun_stem('balls')
    print tag_word(lx, "John")  # returns ["P"]
    print tag_word(lx, "orange")  # returns ["Ns","A"]
    print tag_word(lx, "oranges")  # returns ["Np"]
    print tag_word(lx, "fish")  # returns ["Ns","Np","Ip","Tp"]
    print tag_word(lx, "balls")  # returns ["Np","Is","Ts"]
    print tag_word(lx, "a")  # returns ["AR"]
    print tag_word(lx, "does")
    print tag_word(lx, "?")  # returns []

# main()


