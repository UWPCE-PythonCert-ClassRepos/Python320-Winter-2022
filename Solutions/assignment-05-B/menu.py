#!/usr/bin/env python

'''
Provides a basic CLI frontend
'''
from datetime import datetime
import sys
import textwrap

from loguru import logger

import social_network
import main


def load_users():
    '''
    Loads user accounts from a file
    '''
    filename = input('Enter filename of user file: ')
    result = main.load_users(filename, user_collection)
    if result is not True:
        logger.warning(f"user file: {filename} did not load")


def load_status_updates():
    '''
    Loads status updates from a file
    '''
    filename = input('Enter filename for status file: ')
    main.load_status_updates(filename, status_collection)


def add_user():
    '''
    Adds a new user into the database
    '''
    user_id = input('User ID: ')
    email = input('User email: ')
    user_name = input('User name: ')
    user_last_name = input('User last name: ')
    if not main.add_user(user_id,
                         email,
                         user_name,
                         user_last_name,
                         user_collection):
        print("An error occurred while trying to add new user")
    else:
        print("User was successfully added")


def update_user():
    '''
    Updates information for an existing user
    '''
    user_id = input('User ID: ')
    email = input('User email: ')
    user_name = input('User name: ')
    user_last_name = input('User last name: ')
    print()
    if not main.update_user(user_id,
                            email,
                            user_name,
                            user_last_name,
                            user_collection):
        print("An error occurred while trying to update user")
    else:
        print("User was successfully updated")


def search_user():
    '''
    Searches a user in the database
    '''
    user_id = input('Enter user ID to search: ')
    result = main.search_user(user_id, user_collection)
    if result is None:
        print("ERROR: User does not exist")
    else:
        print(f"User ID: {result.user_id}")
        print(f"Email: {result.email}")
        print(f"Name: {result.user_name}")
        print(f"Last name: {result.user_last_name}")


def delete_user():
    '''
    Deletes user from the database
    '''
    user_id = input('User ID: ')
    if not main.delete_user(user_id, user_collection):
        print("An error occurred while trying to delete user")
    else:
        print("User was successfully deleted")


# def save_users():
#     '''
#     Saves user database into a file
#     '''
#     filename = input('Enter filename for users file: ')
#     main.save_users(filename, user_collection)


def add_status():
    '''
    Adds a new status into the database
    '''
    user_id = input('User ID: ')
    status_id = input('Status ID: ')
    status_text = input('Status text: ')
    if not main.add_status(user_id, status_id, status_text, status_collection):
        print("An error occurred while trying to add new status")
    else:
        print("New status was successfully added")


def update_status():
    '''
    Updates information for an existing status
    '''
#    user_id = input('User ID: ')
    status_id = input('Status ID: ')
    status_text = input('Status text: ')
    if not main.update_status(status_id, status_text, status_collection):
        print("An error occurred while trying to update status")
    else:
        print("Status was successfully updated")


def search_status():
    '''
    Searches a status in the database
    '''
    status_id = input('Enter status ID to search: ')
    result = main.search_status(status_id, status_collection)
    if result is None:
        print("ERROR: Status does not exist")
    else:
#        print(f"User ID: {result.user_id}")
        print(f"Status ID: {result.status_id}")
        print(f"Status text: {result.status_text}")


def delete_status():
    '''
    Deletes status from the database
    '''
    status_id = input('Status ID: ')
    if not main.delete_status(status_id, status_collection):
        print("An error occurred while trying to delete status")
    else:
        print("Status was successfully deleted")


# def save_status():
#     '''
#     Saves status database into a file
#     '''
#     filename = input('Enter filename for status file: ')
#     main.save_status_updates(filename, status_collection)


def quit_program():
    '''
    Quits program
    '''
    sys.exit()

def mainloop():
    '''
    Run the interactive prompt mainloop
    '''
    logger.info("Application Started")
    menu_options = {
        'A': load_users,
        'B': load_status_updates,
        'C': add_user,
        'D': update_user,
        'E': search_user,
        'F': delete_user,
#        'G': save_users,
        'H': add_status,
        'I': update_status,
        'J': search_status,
        'K': delete_status,
#        'L': save_status,
        'Q': quit_program
    }
    while True:
        user_selection = input(textwrap.dedent("""
                            A: Load user database
                            B: Load status database
                            C: Add user
                            D: Update user
                            E: Search user
                            F: Delete user
                            H: Add status
                            I: Update status
                            J: Search status
                            K: Delete status
                            Q: Quit

                            Please enter your choice: """))
        user_selection = user_selection.upper()
        try:
            menu_options[user_selection]()
        except KeyError:
            print("Invalid option")


def setup_logger():  # pragma: no cover
    """
    Set up the default logging for the CLI
    """
    # create a logfile with today's date
    logfilename = f"logfile-{datetime.now().date().isoformat()}.txt"
    logger.add(logfilename,
               mode='a',  # append, so the file sticks around
               encoding='utf-8',
               format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
               )


if __name__ == '__main__':  # pragma: no cover
    setup_logger()
    client = social_network.start_mongo()

    if (len(sys.argv) > 1) and (sys.argv[1] == "clear"):
        client.drop_database('social_network')
    database = client.social_network
    user_collection = status_collection = main.init_social_network(database)
    mainloop()
