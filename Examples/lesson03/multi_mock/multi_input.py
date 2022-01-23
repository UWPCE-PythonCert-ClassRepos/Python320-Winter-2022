"""
multi_input.py

an example where input() is called multiple times within one function
"""

import time

def single_input():
    response = input("give me anything >")

    return response


def chant():
    letters = []
    letters.append(input("give me an T >"))
    letters.append(input("give me an E >"))
    letters.append(input("give me an S >"))
    letters.append(input("give me an T >"))
    word = "".join(letters)

    time.sleep(0.5)

    print("what does it spell?")
    print(word.upper() + "!!!!")

    return word

if __name__ == "__main__":
    chant()



