"""
demo of mutating functions
"""


def cap_names(user_info):
    for k in {'first_name', 'last_name', 'middle_name'}:
        user_info[k] = user_info[k].capitalize()


user = {'first_name': 'chris',
        'middle_name': 'h',
        'last_name': 'bArker',
        }

print("before:", user)

cap_names(user)

print("after:", user)


