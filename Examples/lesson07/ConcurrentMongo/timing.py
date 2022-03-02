"""
timing.py

Some timings of the mongodb code
"""
import time
from datetime import datetime

from loguru import logger

import social_network
import main


def setup_logger():  # pragma: no cover
    """
    Set up the default logging for the CLI
    """
    # create a logfile with today's date
    logfilename = f"timing_logfile-{datetime.now().date().isoformat()}.txt"
    logger.add(logfilename,
               mode='a',  # append, so the file sticks around
               encoding='utf-8',
               format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
               level="INFO"
               )


def time_load_users():
    """
    timeloading users in various ways
    """
    for load_func in (
                      # main.load_users,
                      main.load_users_many,
                      # main.load_users_mp,
                      # main.load_users_thread,
                      ):
        with social_network.start_mongo() as client:
            client.drop_database('timing_db')

        snw = social_network.SocialNetwork('timing_db')

        start = time.perf_counter()
        load_func('accounts.csv', snw)
        finish = time.perf_counter()
        print(f"{load_func.__name__} took: {finish-start:.2f} seconds")


def time_multiprocessing():
    """
    time loading users using multiprocessing
    """
    with social_network.start_mongo() as client:
        client.drop_database('timing_db')

    start = time.perf_counter()
    main.load_users_mp('accounts.csv', 'timing_db')
    finish = time.perf_counter()
    print(f"load_users_mp took: {finish-start:.2f} seconds")


def time_queue():
    """
    time loading users using multiprocessing and a queue
    """
    with social_network.start_mongo() as client:
        client.drop_database('timing_db')

    start = time.perf_counter()
    main.load_users_queue('accounts.csv', 'timing_db')
    finish = time.perf_counter()
    print(f"load_users_queue took: {finish-start:.2f} seconds")



def time_load_status():
    """
    time ways to load status updates
    """
    for load_func in (main.load_status_updates, main.load_status_updates_many):
        with social_network.start_mongo() as client:
            client.drop_database('timing_db')
            database = client['timing_db']

            snw = social_network.SocialNetwork(database)
            main.load_users_many('accounts.csv', snw)
            start = time.perf_counter()
            load_func('status_updates_medium.csv', snw)
            finish = time.perf_counter()
            print(f"{load_func.__name__} took: {finish-start:.2f} seconds")


if __name__ == "__main__":
    setup_logger()
    # time_load_users()
    time_multiprocessing()
    # time_queue()
