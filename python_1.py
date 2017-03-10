# Grab the output you get, and assign it
# to a string variable in a new python script

L = '''The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!'''

# Take your personal email as a second string and
# concatenate it with L. Print the length of L

L = 'kirgenvall@gmail.com:\n\n' + L
print ('Variable length: ' + str(len(L)))

# Print the count all the vowels in L

Lv = ''.join([i for i in L if i in 'AEUIOaeuio'])
print ('Vowels count: ' + str(len(Lv)))

# Print each 18th symbol of the string,
# but do it in case opposite to the original,
# adding the position of that letter in the string

for i in range(len(L))[18::18]:
    char = L[i]
    if char.isalpha():
        if char.isupper(): char = char.lower()
        else: char = char.upper()
    print (str(i) + char)