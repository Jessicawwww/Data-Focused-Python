
# regex_examples.py

poem = [
    'How Doth The Little Crocodile',
    '-----------------------------',
    '',
    '            by Lewis Carroll',
    '',
    'How doth the little crocodile',
    '  Improve his shining tail',
    'And pour the waters of the Nile',
    '  On every golden scale!',
    '',
    'How cheerfully he seems to grin',
    '  How neatly spreads his claws',
    'And welcomes little fishes in',
    '  With gently smiling jaws!' ]

'''
for line in poem:
    print(line)

input('Press Enter to continue...')
'''

import re

# pat = '^H'	# line starts with the capital letter 'H'

# pat = r'^$'       # empty lines

# pat = r'^  [A-Z]' # ... line starts with two spaces
                  #   and a capital letter

# pat = r'^ *[A-Z]' # ... start with optional space '', ' ', '  ', '   ', or more space
                  #   and then a capital letter

# pat = r'e$'       # ... end with e

# pat = r'[aeiou][aeiuo]' # ... 2 lowercase vowels consecutively

# pat = r'a.*e.*i'  # ... contain a, e, i in order with optional other characters in between

# pat = r'^[^t]*$'  # ... do not contain t

# pat = r'^[^t]'  # ... start with one character that is not 't'

# pat = r'\.'	# sequence contains the full stop character

# pat = r'How|Nile|grin' # ... contain How or Nile

# pat = r'([aeiou])\1'   # ... contain a pair of
                       #    lowercase vowels
# pat = 'e+'	# the string contains one or more e's

# pat = r'(...).*\1'  # ... contains some 3-char
                    #    sequence at least twice

pat = r'(.)(.)(.).*\3\1\2' # string contains 3 chars and then the same
                            # chars but in a different order

for line in poem:
    if re.search(pat, line) != None:
        print(line)        # we found a match!

