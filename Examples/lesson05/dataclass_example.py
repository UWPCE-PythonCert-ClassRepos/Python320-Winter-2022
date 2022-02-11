from dataclasses import dataclass


@dataclass
class User:
    user_name: None
    user_id: None
    email: None = ""


# this is shorthand for this, but with more features
class User2:
    def __init__(self, user_name, user_id, email=""):
        self.user_name = user_name
        self.user_id = user_id
        self.email = email

# Make one:

user = User('cbarker', '12234', 'Chris@this.com')

user = User(user_name='cbarker', user_id='12234', email='Chris@this.com')

user_data = {'user_name': 'cbarker',
             'user_id': '12234',
             'email': 'Chris@this.com'}

user2 = User(**user_data)
print(user2)

user_tup = ('cbarker', '12234', 'Chris@this.com')
user3 = User(*user_tup)
print(user3)

