"""
Function that takes in an input string and a dictionary array and
return the values from the dictionary, that start with the input string.

If there are more than 5 matches, restricts the output to the first 5 results.
If there are no matches, returns an empty array.
Non-letters not counts.

Example:
autocomplete('ai', ['airplane','airport','apple','ball'])

Result:
['airplane','airport']
"""

import re


def autocomplete(string, lst=None):

    lst = lst or []
    letter_filter = lambda letter: letter.isalpha()
    for index, word in enumerate(lst):
        lst[index] = "".join(filter(letter_filter, word))
    pattern = r'\b{}.*'.format(string)
    search_filter = lambda word: re.findall(pattern, word, flags=re.I)
    result = list(filter(search_filter, lst))
    if len(result) > 5:
        del(result[5:len(result)])
    return result

print (autocomplete('Ai', ['Airpl132454ane', 'aIrpo!@#~rt', 'appaile', 'baill']))
