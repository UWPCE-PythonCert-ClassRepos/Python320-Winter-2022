'''
main driver for a simple social network project

This one is a more functional approach: using

PeeWee Dataset interface.
'''

import csv

from loguru import logger

from peewee import IntegrityError


def init_user_collection(dataset):
    '''
    Creates and returns a new instance of UserCollection
    '''

    return dataset['users']


def init_status_collection(dataset):
    '''
    Creates and returns a new instance of UserStatusCollection
    '''
    return dataset['statuses']



def load_csv(filename, table, key_map):
    """
    Opens a CSV file and loads it into a dataset table

    :param filename: name of csv file

    :param table: table to load into

    :param key_map: mapping of csv column headers
                    to column names in table.
                    Example:
                    {'user_id': 'USER_ID',
                     'user_email': 'EMAIL',
                     'user_name': 'NAME',
                     'user_last_name': 'LASTNAME',
                      }
    """
    with open(filename, encoding='utf-8') as infile:
        reader = csv.DictReader(infile, delimiter=',')
        new_records = []
        for row in reader:
            try:
                # map the keys:
                record = {key: row[col_name] for key, col_name in key_map.items()}
            except KeyError:
                logger.debug(f'Bad header in CSV file: {list(row.keys())}')
                return False
            if None in record.values():
                logger.debug(f'Bad row in CSV file: {row}')
                return False
            # strip extra whitespace
            for key in record:
                record[key] = record[key].strip()
            if "" in record.values():
                logger.debug(f'Bad row in CSV file: {row}')
                return False
            new_records.append(record)
            print(record)
        for record in new_records:
            table.insert(**record)

    # if it got this far, it all worked
    return True


def load_users(filename, user_collection):
    '''
    Opens a CSV file with user data and
    adds it to an existing instance of
    UserCollection
    '''

    key_map = {'user_id': 'USER_ID',
               'user_email': 'EMAIL',
               'user_name': 'NAME',
               'user_last_name': 'LASTNAME',
               }

    return load_csv(filename, user_collection, key_map)

def load_status_updates(filename, status_collection):
    '''
    Opens a CSV file with status updates and adds it to
    an existing instance of UserCollection
    '''
    key_map = {'user_id': 'USER_ID',
               'status_text': 'STATUS_TEXT',
               'status_id': 'STATUS_ID',
               }

    return load_csv(filename, status_collection, key_map)


def add_user(user_id, user_email, user_name, user_last_name, user_collection):
    '''
    Creates a new instance of User and stores it in user_collection
    (which is an instance of UserCollection)

    Requirements:
    - user_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
      user_collection.add_user() returns False).
    - Otherwise, it returns True.
    '''
    try:
        result = user_collection.insert(user_id=user_id,
                                        user_email=user_email,
                                        user_name=user_name,
                                        user_last_name=user_last_name,
                                        )
    except IntegrityError:
        return False

    return bool(result)


def update_user(user_id, user_email, user_name, user_last_name, user_collection):
    '''
    Updates the values of an existing user

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    '''
    rec = user_collection.find_one(user_id=user_id)
    if rec is None:
        return False
    user_collection[rec['id']] = {'user_email': user_email,
                                  'user_name': user_name,
                                  'user_last_name': user_last_name}
    return True

def delete_user(user_id, user_collection):
    '''
    Deletes a user from user_collection.

    Requirements:
    - Returns False if there are any errors (such as user_id not found)
    - Otherwise, it returns True.
    '''
    return bool(user_collection.delete(user_id=user_id))


def search_user(user_id, user_collection):
    '''
    Searches for a user in user_collection (which is an instance of
    UserCollection).

    Requirements:
    - If the user is found, returns the corresponding User instance.
    - Otherwise, it returns None.
    '''
    return user_collection.find_one(user_id=user_id)


def add_status(status_id, user_id, status_text, status_collection):
    '''
    Creates a new instance of UserStatus and stores it in
    user_collection(which is an instance of UserStatusCollection)

    Requirements:
    - status_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
      user_collection.add_status() returns False).
    - Otherwise, it returns True.
    '''

    try:
        return bool(status_collection.insert(status_id=status_id,
                                             user_id=user_id,
                                             status_text=status_text))
    except IntegrityError:
        return False


def update_status(status_id, user_id, status_text, status_collection):
    '''
    Updates the values of an existing status_id

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.

    NOTE: should it be possible to change the user_id of a status message?
    '''
    rec = status_collection.find_one(status_id=status_id)
    if rec is None:
        return False
    status_collection[rec['id']] = {'user_id': user_id,
                                    'status_text': status_text,
                                    }
    return True


def delete_status(status_id, status_collection):
    '''
    Deletes a status_id from user_collection.

    Requirements:
    - Returns False if there are any errors (such as status_id not found)
    - Otherwise, it returns True.
    '''
    return bool(status_collection.delete(status_id=status_id))


def search_status(status_id, status_collection):
    '''
    Searches for a status in status_collection

    Requirements:
    - If the status is found, returns the corresponding
    UserStatus instance.
    - Otherwise, it returns None.
    '''
    return status_collection.find_one(status_id=status_id)
