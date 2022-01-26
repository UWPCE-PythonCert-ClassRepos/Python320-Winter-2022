## Debugging Log for menu.py

Note: all menu functions run from unit_tests in test_menu.py

### load_users()

Error:
```
>       main.load_users(filename, user_selection)
E       NameError: name 'user_selection' is not defined

menu.py:13: NameError
```

Too easy -- that's supposed to be `user_collection`

### update_users()

Error:

```
    def update_user():
        '''
        Updates information for an existing user
        '''
        user_id = input('User ID: ')
        email = input('User email: ')
        user_name = input('User name: ')
        user_last_name = input('User last name: ')
>       if not main.update_user(user_id, email, user_name, user_last_name):
E       TypeError: update_user() missing 1 required positional argument: 'user_collection'

menu.py:50: TypeError
```

also too easy -- add the user_collection parameter

### search_user

```
    def search_user():
        '''
        Searches a user in the database
        '''
        user_id = input('Enter user ID to search: ')
        result = main.search_user(user_id, user_collection)
>       if not result.name:
E       AttributeError: 'Users' object has no attribute 'name'

menu.py:66: AttributeError
```

OK -- also really easy, but for fun, let's put a breakpoint in right before that error:

```
(Pdb) l
 62         Searches a user in the database
 63         '''
 64         user_id = input('Enter user ID to search: ')
 65         result = main.search_user(user_id, user_collection)
 66         breakpoint()
 67  ->     if not result.name:
 68             print("ERROR: User does not exist")
 69         else:
 70             print(f"User ID: {result.user_id}")
 71             print(f"Email: {result.email}")
 72             print(f"Name: {result.user_name}")
(Pdb) result
<users.Users object at 0x10b12a9e0>
(Pdb) vars(result)
{'user_id': 'evmiles97', 'email': 'eve.miles@uw.edu', 'user_name': 'Eve', 'user_last_name': 'Miles'}
(Pdb) result.name
*** AttributeError: 'Users' object has no attribute 'name'
(Pdb) result.user_name
'Eve'
```

Ahh -- so it's `user_name`, not `name` -- fixed!

### search_status

```
    def search_status():
        '''
        Searches a status in the database
        '''
        status_id = input('Enter status ID to search: ')
        result = main.search_status(status_id, status_collection)
>       if not result.user_id:
E       AttributeError: 'NoneType' object has no attribute 'user_id'

menu.py:127: AttributeError
```

a bit too easy, but what the heck -- add a breakpoint:

```
(Pdb) l
122         '''
123         Searches a status in the database
124         '''
125         status_id = input('Enter status ID to search: ')
126         breakpoint()
127  ->     result = main.search_status(status_id, status_collection)
128         if not result.user_id:
129             print("ERROR: Status does not exist")
130         else:
131             print(f"User ID: {result.user_id}")
132             print(f"Status ID: {result.status_id}")
(Pdb) s
--Call--
> /Users/chris/UWPCE/Py320/MyAssignments/python-320-assignment-02-PythonCHB/main.py(247)search_status()
-> def search_status(status_id, status_collection):
(Pdb) n
> /Users/chris/UWPCE/Py320/MyAssignments/python-320-assignment-02-PythonCHB/main.py(256)search_status()
-> status = status_collection.search_status(status_id)
(Pdb) n
> /Users/chris/UWPCE/Py320/MyAssignments/python-320-assignment-02-PythonCHB/main.py(258)search_status()
-> if status.status_id is None:
(Pdb) status
<user_status.UserStatus object at 0x107aee500>
(Pdb) status.status_id
(Pdb) status.status_id is None
True
(Pdb) n
> /Users/chris/UWPCE/Py320/MyAssignments/python-320-assignment-02-PythonCHB/main.py(259)search_status()
-> return None
(Pdb) n
--Return--
> /Users/chris/UWPCE/Py320/MyAssignments/python-320-assignment-02-PythonCHB/main.py(259)search_status()->None
-> return None
(Pdb) n
> /Users/chris/UWPCE/Py320/MyAssignments/python-320-assignment-02-PythonCHB/menu.py(128)search_status()
-> if not result.user_id:
(Pdb) result
(Pdb) str(result)
'None'
```
OK, so search_status retruns None when it's not found. so I change that to:

```
if result is None:
   ...
```

And all good.
