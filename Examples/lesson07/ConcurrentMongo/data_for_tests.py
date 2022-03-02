"""
data_for_tests.py

common  required by tests

"""

from social_network import SocialNetwork, start_mongo

import pytest

SAMPLE_USERS_DATA = [{'user_id': 'cbarker12',
              'email': 'cbarker@some_domain.com',
              'user_name': 'cbarker',
              'user_last_name': 'Barker',
              },
             {'user_id': 'fjones34',
              'email': 'jones@some_domain.com',
              'user_name': 'fjones',
              'user_last_name': 'Jones',
              },
             {'user_id': 'bwinkle678',
              'email': 'cwinkle@some_domain.com',
              'user_name': 'bwinkle',
              'user_last_name': 'Winkle',
              }]

SAMPLE_STATUS_DATA = [{'user_id': 'cbarker12',
                 'status_id': 'st12345',
                 'status_text': 'A simple message from user: cbarker12'
                 },
                {'user_id': 'fjones34',
                 'status_id': 'st12355',
                 'status_text': 'A simple message from user: fjones34'
                 },
                {'user_id': 'bwinkle678',
                 'status_id': 'st12455',
                 'status_text': 'A simple message from user: bwinkle678'
                 },
                {'user_id': 'cbarker12',
                 'status_id': 'st55555',
                 'status_text': 'A second simple message from user: cbarker12'
                 },
                ]

@pytest.fixture
def empty_db():
    """
    creates a empty mongo database
    yields the name of the database
    """
    db_name = 'test_database'
    client = start_mongo()
    client.drop_database(db_name)
    database = client[db_name]
    yield db_name

    client.drop_database(database)
    client.close()


@pytest.fixture
def pop_social_network(empty_db):
    pop_social_network = SocialNetwork(empty_db)
    for user in SAMPLE_USERS_DATA:
        pop_social_network.add_user(**user)
    for stat in SAMPLE_STATUS_DATA:
        pop_social_network.add_status(**stat)
    yield pop_social_network
