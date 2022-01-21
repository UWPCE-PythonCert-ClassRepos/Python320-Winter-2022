"""
demo of how stdout can be redirected
"""

import sys

print("here's the regular sys.stdout")

# now redirect it

# keep the old one around to be reset

orig_stdout = sys.stdout

sys.stdout = open('temp_output.txt', 'w', encoding='utf-8')

print("Hey! Where did the output go!")

print("What's going on ???")

# now restore it

sys.stdout = orig_stdout

print("That's better -- whew!")

