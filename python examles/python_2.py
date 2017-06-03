"""
Accepts any number of strings, and returns the same strings with all even
indexed characters in each word upper cased, and all odd indexed characters
in each word lower cased.
The indexing just explained is zero based, so the index 0 is even,
therefore that character should be upper cased.

Examples:
to_weird ("String") -> returns "StRiNg"
to_weird ("Weird string case") -> returns "WeIrD StRiNg CaSe"
"""


def to_weird(*strings):
    for c, string in enumerate(list(strings)):
        string = string.split(' ')
        for n, word in enumerate(string):
            word = list(word)
            upper_On = True
            for i, l in enumerate(word):
                if l.isalpha():
                    if upper_On:
                        word[i] = l.upper()
                        upper_On = False
                    else:
                        word[i] = l.lower()
                        upper_On = True
            string[n] = "".join(word)
        strings[c] = " ".join(string)
    return strings

def print_weirds(inpoot):
    for _ in inpoot:
        print (_)
