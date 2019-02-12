# File: statements.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis
# Revised October 2017 by Chunchuan Lyu


# PART A: Processing statements

def add(lst, item):
    if (item not in lst):
        lst.insert(len(lst), item)


class Lexicon:
    """stores known word stems of various part-of-speech categories"""

    def __init__(self):
        self.l = []

    #   pos = ["P", "N", "A", "I", "T"]

    def add(self, stem, cat):

        self.l.append((stem, cat))

    def getAll(self, cat):
        listcat = [v[0] for v in set(self.l) if v[1]==cat]

        return listcat
    # add code here


class FactBase:
    """stores unary and binary relational facts"""

    # global unary
    # global binary

    def __init__(self):
        self.unary = []
        self.binary = []

    def addUnary(self, pred, e1):
        self.unary.append((pred, e1))

    def addBinary(self, pred, e1, e2):
        self.binary.append((pred, e1, e2))

    def queryUnary(self, pred, e1):
        return ((pred, e1) in self.unary)


    def queryBinary(self, pred, e1, e2):
        return ((pred, e1, e2) in self.binary)

    # add code here


import re

from nltk.corpus import brown

words = set(brown.tagged_words())
vb =set()
vbz = set()
for (w, tag) in words:
    if (tag == "VB"):
        vb.add(w)
    elif (tag == "VBZ"):
        vbz.add(w)


def verb_stem(s):
    """extracts the stem from the 3sg form of a verb, or returns empty string"""


    vowels = "aioue"
    stem = ""

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
      #  print "verb ends in s"
        if s == "has":
            return "have"
        elif re.match("[a-z]+[^(aiouesxyz|ch|sh)]s$", s):
            stem = s[:-1]
        elif re.match("[a-z]+[aioue]ys$", s):
            stem = s[:-1]

    if (s in vbz) or (stem in vb):
        return stem
    else:
        return ""
    # add code here


def add_proper_name(w, lx):
    """adds a name to a lexicon, checking if first letter is uppercase"""
    if ('A' <= w[0] and w[0] <= 'Z'):
        lx.add(w, 'P')
        return ''
    else:
        return (w + " isn't a proper name")


def process_statement(lx, wlist, fb):
    """analyses a statement and updates lexicon and fact base accordingly;
       returns '' if successful, or error message if not."""
    # Grammar for the statement language is:
    #   S  -> P is AR Ns | P is A | P Is | P Ts P
    #   AR -> a | an
    # We parse this in an ad hoc way.
    msg = add_proper_name(wlist[0], lx)
    if (msg == ''):
        if (wlist[1] == 'is'):
            if (wlist[2] in ['a', 'an']):
                lx.add(wlist[3], 'N')
                fb.addUnary('N_' + wlist[3], wlist[0])
            else:
                lx.add(wlist[2], 'A')
                fb.addUnary('A_' + wlist[2], wlist[0])
        else:
            stem = verb_stem(wlist[1])
            if (len(wlist) == 2):
                lx.add(stem, 'I')
                fb.addUnary('I_' + stem, wlist[0])
            else:
                msg = add_proper_name(wlist[2], lx)
                if (msg == ''):
                    lx.add(stem, 'T')
                    fb.addBinary('T_' + stem, wlist[0], wlist[2])
    return msg


# def main():
#     lx = Lexicon()
#     lx.add("John", "P")
#     lx.add("Mary", "P")
#     lx.add("like", "T")
#     lx.getAll("P")
#     fb = FactBase()
#     fb.addUnary("duck", "John")
#     fb.addBinary("love", "John", "Mary")
#     print fb.queryUnary("duck", "John")  # returns True
#     print  fb.queryBinary("love", "Mary", "John")
#     print verb_stem("flies")  # returns "fly"
#     print verb_stem("flys")  # returns ""
#     print verb_stem("plays")
#     print verb_stem("goes")
#     print verb_stem("eats")
#
#
# main()
# End of PART A.
