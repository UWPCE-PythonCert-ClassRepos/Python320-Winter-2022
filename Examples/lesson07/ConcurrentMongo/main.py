'''
Serves as proxy between the user interface
and the execution code
'''
import csv
import pandas as pd

import multiprocessing
import threading

import social_network


def init_social_network(database):
    '''
    Creates and returns a new instance of SocialNetwork manager

    :param database: name of the Mongo database to use.
    '''
    return social_network.SocialNetwork(database)


def load_users(filename, user_collection):
    '''
    Opens a CSV file with user data and
    adds it to an existing instance of
    UserCollection

    Requirements:
    - If a user_id already exists, it
    will ignore it and continue to the
    next.
    - Returns False if there are any errors
    (such as empty fields in the source CSV file)
    - Otherwise, it returns True.
    '''
    with open(filename, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            user_collection.add_user(row['USER_ID'], row['EMAIL'], row['NAME'], row['LASTNAME'])
    return True

def load_users_many(filename, snw):
    '''
    Opens a CSV file with user data and
    adds it to an existing instance of
    UserCollection

    Requirements:
    - If a user_id already exists, it
    will ignore it and continue to the
    next.
    - Returns False if there are any errors
    (such as empty fields in the source CSV file)
    - Otherwise, it returns True.
    '''
    with open(filename, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data = ({'user_id': row['USER_ID'],
                 'email': row['EMAIL'],
                 'user_name': row['NAME'],
                 'user_last_name': row['LASTNAME']} for row in reader)
        snw.add_users(data)
    return True


def multi_process_load_users(database_name, chunk):
    """
    multiprocessing compatible chunk loading

    The trick is that the mongo client needs to be created
    in the process -- so we are making a new SocialNetwork
    manager for each chunk.
    """
    snw = social_network.SocialNetwork(database_name)
    snw.add_users(chunk)


class LoadUsers(multiprocessing.Process):
    """
    Multiprocessing Process to load chunks of users.
    """
    def __init__(self, task_queue, database_name):
        super().__init__()
        self.task_queue = task_queue
        self.database_name = database_name

    def run(self):
        snw = social_network.SocialNetwork(self.database_name)
        proc_name = self.name
        while True:
            chunk = self.task_queue.get()
            if chunk is None:
                # Poison pill means shutdown
                print(f"{proc_name}: Exiting")
                self.task_queue.task_done()
                break
            print(f"{proc_name}: adding a chunk of {len(chunk)} records")
            snw.add_users(chunk)
            self.task_queue.task_done()
        return

def load_users_queue(filename, database_name):
    CHUNK_SIZE = 200
    NUM_PROC = multiprocessing.cpu_count()

    tasks = multiprocessing.JoinableQueue()

    # Create the processes
    print(f"Creating {NUM_PROC} processes")
    processes = [LoadUsers(tasks, database_name) for i in range(NUM_PROC)]
    print("starting processes")
    for proc in processes:
        proc.start()
    print("processes started")

    # Fill the queue with chunks to process
    print("filling the queue")
    chunk_number = 1
    for chunk in pd.read_csv(filename,
                             chunksize=CHUNK_SIZE,
                             iterator=True):
        print(f"CHUNK {chunk_number}")
        data = [{'user_id': row['USER_ID'],
                 'email': row['EMAIL'],
                 'user_name': row['NAME'],
                 'user_last_name': row['LASTNAME']
                 } for index, row in chunk.iterrows()
                ]
        tasks.put(data)
        chunk_number += 1
    # Add a poison pill for each process
    for i in range(NUM_PROC):
        tasks.put(None)
    # wait for it all to finish
    tasks.join()

    return True


def load_users_mp(filename, database_name):
    '''
    Opens a CSV file with user data and
    adds it to an existing instance of database

    Uses pandas to chunk the file, and multi-processing!
    '''
    CHUNK_SIZE = 500
    chunk_number = 1
    processes = []
    for chunk in pd.read_csv(filename,
                             chunksize=CHUNK_SIZE,
                             iterator=True):
        print(f"CHUNK {chunk_number}")
        data = [{'user_id': row['USER_ID'],
                 'email': row['EMAIL'],
                 'user_name': row['NAME'],
                 'user_last_name': row['LASTNAME']
                 } for index, row in chunk.iterrows()
                ]
        # multi_process_load_users(database_name, data)
        # ctx = multiprocessing.get_context('fork')
        ctx = multiprocessing
        proc = ctx.Process(target=multi_process_load_users,
                                       args=(database_name, data))
        processes.append(proc)
        print("about to start process for CHUNK:", chunk_number)
        proc.start()
        chunk_number += 1
    print("all processes started")
    for proc in processes:
        print(f"waiting on {proc.name}")
        proc.join()

    return True



def load_users_mp_wrong(filename, snw):
    '''
    Opens a CSV file with user data and
    adds it to an existing instance of
    UserCollection

    Uses pandas to chunk the file, and multi-processing!
    '''
    CHUNK_SIZE = 100
    chunk_number = 0
    processes = []
    for chunk in pd.read_csv(filename,
                             chunksize=CHUNK_SIZE,
                             iterator=True):
        print(f"CHUNK {chunk_number}")
        data = ({'user_id': row['USER_ID'],
                 'email': row['EMAIL'],
                 'user_name': row['NAME'],
                 'user_last_name': row['LASTNAME']
                 } for index, row in chunk.iterrows()
                )
        proc = multiprocessing.Process(target=snw.add_users, args=(data,))
        processes.append(proc)
        proc.start()
        chunk_number += 1
    for proc in processes:
        proc.join()

    return True

def load_users_thread(filename, snw):
    '''
    Opens a CSV file with user data and
    adds it to an existing instance of
    UserCollection

    Uses pandas to chunk the file, and multi-processing!
    '''
    CHUNK_SIZE = 500
    chunk_number = 1
    processes = []
    for chunk in pd.read_csv(filename,
                             chunksize=CHUNK_SIZE,
                             iterator=True):
        print(f"CHUNK {chunk_number}")
        data = ({'user_id': row['USER_ID'],
                 'email': row['EMAIL'],
                 'user_name': row['NAME'],
                 'user_last_name': row['LASTNAME']
                 } for index, row in chunk.iterrows()
                )
        proc = threading.Thread(target=snw.add_users, args=(data,))
        processes.append(proc)
        proc.start()
        chunk_number += 1
    for proc in processes:
        proc.join()

    return True

def load_status_updates(filename, status_collection):
    '''
    Opens a CSV file with status data and
    adds it to an existing instance of
    UserStatusCollection

    Requirements:
    - If a status_id already exists, it
    will ignore it and continue to the
    next.
    - Returns False if there are any errors
    (such as empty fields in the source CSV file)
    - Otherwise, it returns True.
    '''
    with open(filename, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            status_collection.add_status(row['USER_ID'], row['STATUS_ID'], row['STATUS_TEXT'])
    return True


def load_status_updates_many(filename, status_collection):
    '''
    Opens a CSV file with status data and
    adds it to an existing instance of
    UserStatusCollection

    Requirements:
    - If a status_id already exists, it
    will ignore it and continue to the
    next.
    - Returns False if there are any errors
    (such as empty fields in the source CSV file)
    - Otherwise, it returns True.
    '''
    with open(filename, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data = ({'user_id': row['USER_ID'],
                 'status_id': row['STATUS_ID'],
                 'status_text': row['STATUS_TEXT']
                 } for row in reader)
        status_collection.add_statuses(data)
    return True

def add_user(user_id, email, user_name, user_last_name, user_collection):
    '''
    Creates a new instance of User and stores it in user_collection
    (which is an instance of UserCollection)

    Requirements:
    - user_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
    user_collection.add_user() returns False).
    - Otherwise, it returns True.
    '''
    return user_collection.add_user(user_id, email, user_name, user_last_name)

def update_user(user_id, email, user_name, user_last_name, user_collection):
    '''
    Updates the values of an existing user

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    '''
    # Create an instance of Users for the updated user
    return user_collection.modify_user(user_id, email, user_name, user_last_name)

def delete_user(user_id, user_collection):
    '''
    Deletes a user from user_collection.

    Requirements:
    - Returns False if there are any errors (such as user_id not found)
    - Otherwise, it returns True.
    '''
    return user_collection.delete_user(user_id)

def search_user(user_id, user_collection):
    '''
    Searches for a user in user_collection
    (which is an instance of UserCollection).

    Requirements:
    - If the user is found, returns the corresponding
    User instance.
    - Otherwise, it returns None.
    '''
    return user_collection.search_user(user_id)

def add_status(user_id, status_id, status_text, status_collection):
    '''
    Creates a new instance of UserStatus and stores it in user_collection
    (which is an instance of UserStatusCollection)

    Requirements:
    - status_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
    user_collection.add_status() returns False).
    - Otherwise, it returns True.
    '''
    return status_collection.add_status(user_id, status_id, status_text)

def update_status(status_id, status_text, status_collection):
    '''
    Updates the values of an existing status_id

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    '''
    return status_collection.modify_status(status_id, status_text)

def delete_status(status_id, status_collection):
    '''
    Deletes a status_id from user_collection.

    Requirements:
    - Returns False if there are any errors (such as status_id not found)
    - Otherwise, it returns True.
    '''
    return status_collection.delete_status(status_id)

def search_status(status_id, status_collection):
    '''
    Searches for a status in status_collection

    Requirements:
    - If the status is found, returns the corresponding
    UserStatus instance.
    - Otherwise, it returns None.
    '''
    return status_collection.search_status(status_id)

