"""
data_for_tests.py

assorted data that can be used for the tests
"""

# pylint: disable=invalid-name

import pytest

from socialnetwork_model import get_dataset


SAMPLE_USERS_DATA = [{'user_id': 'cbarker12',
                      'user_email': 'cbarker@some_domain.com',
                      'user_name': 'cbarker',
                      'user_last_name': 'Barker',
                      },
                     {'user_id': 'fjones34',
                      'user_email': 'jones@some_domain.com',
                      'user_name': 'fjones',
                      'user_last_name': 'Jones',
                      },
                     {'user_id': 'bwinkle678',
                      'user_email': 'cwinkle@some_domain.com',
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


# def cleanup_database(db):
#     """
#     close and cleanup the database
#     """
#     db.drop_tables(MODELS)
#     db.bind(MODELS, bind_refs=False, bind_backrefs=False)
#     db.close()


@pytest.fixture
def empty_db():
    """
    initialize and empty database
    """
    # setup
    ds = get_dataset(":memory:")
    yield ds

    # # teardown
    # cleanup_database(db)


@pytest.fixture
def full_db():
    """
    initialize a database with some data in it
    """
    # setup
    ds = get_dataset(":memory:")
    users = ds['users']
    statuses = ds['statuses']

    # populate the User table
    for user in SAMPLE_USERS_DATA:
        users.insert(**user)

    # populate the Status table
    for stat in SAMPLE_STATUS_DATA:
        statuses.insert(**stat)

    yield ds
