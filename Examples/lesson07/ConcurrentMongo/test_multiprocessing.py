"""
tests of the multiprocessing / multithreading code

Keeping this separate, as there's a bunch of experimental code there.
""" 

import pytest

from social_network import start_mongo, SocialNetwork
import main

@pytest.fixture
def empty_db():
    """
    creates a empty mongo database
    yields the name of the database
    """
    db_name = 'timing_database'
    client = start_mongo()
    client.drop_database(db_name)
    database = client[db_name]
    yield db_name

    client.drop_database(database)
    client.close()


def test_add_users_queue(empty_db):
    main.load_users_queue('accounts.csv', empty_db)

    snw = SocialNetwork(empty_db)
    assert len(snw) == 2000


def test_add_users_queue_tiny(empty_db):
    main.load_users_queue('accounts_small.csv', empty_db)

    snw = SocialNetwork(empty_db)
    assert len(snw) == 3




