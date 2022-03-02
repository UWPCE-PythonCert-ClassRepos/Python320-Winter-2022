"""
tests for Social Network code

NOTE: most functionality is tested by test_main
"""

# pylint: disable=missing-function-docstring

import copy

from social_network import User, StatusUpdate, SocialNetwork

from data_for_tests import (empty_db,
                            SAMPLE_USERS_DATA,
                            SAMPLE_STATUS_DATA
                            )


def test_status_to_dict():
    """
    does a StatusUpdate create a correct dict?
    """
    sud = StatusUpdate('xxxx', 'a simple message')

    sud = sud.to_dict()

    assert sud['status_id'] == 'xxxx'
    assert sud['status_text'] == 'a simple message'


def test_user_to_dict():
    user = User('xxxx', 'cbarker@this.that', 'cbarker', 'Barker')

    udict = user.to_dict()

    assert 'user_id' not in udict

    assert udict['_id'] == 'xxxx'
    assert udict['email'] == 'cbarker@this.that'
    assert udict['user_name'] == 'cbarker'
    assert udict['user_last_name'] == 'Barker'


def test_user_from_dict():
    user = User('xxxx', 'cbarker', 'Barker', 'cbarker@this.that')

    _dict = user.to_dict()

    user2 = User.from_dict(_dict)

    assert user == user2


def test_user_with_status_messages():
    user = User('xxxx',
                'cbarker@this.that',
                'cbarker',
                'Barker',
                [StatusUpdate('xxxx_01', 'a new message')])

    user.status_updates.append(StatusUpdate('xxxx_02', "A random message"))
    udict = user.to_dict()

    assert 'user_id' not in udict
    assert udict['_id'] == 'xxxx'
    assert udict['status_updates'] == [{'status_id': 'xxxx_01','status_text': "a new message"},
                                       {'status_id': 'xxxx_02','status_text': "A random message"},
                                       ]

    user2 = User.from_dict(udict)
    assert user == user2


def test_add_users(empty_db):
    """
    Tests adding a batch of users to the database
    """
    snw = SocialNetwork(empty_db)

    # just to make sure
    assert len(snw) == 0
    # make sure it works with an iterator
    result = snw.add_users(iter(SAMPLE_USERS_DATA))
    assert result == 3
    assert len(snw) == 3


def test_add_users_one_duplicate(empty_db):
    """
    Tests adding a batch of users to the database
    """
    snw = SocialNetwork(empty_db)

    # just to make sure
    assert len(snw) == 0
    result = snw.add_users(SAMPLE_USERS_DATA)

    assert result == 3
    assert len(snw) == 3

    # Try to add some with one duplicate in the middle
    data = copy.deepcopy(SAMPLE_USERS_DATA)
    data[0]['user_id'] = 'xxxyyyzzz'
    data[2]['user_id'] = 'iiijjjkkk'
    result = snw.add_users(data)

    assert result == 2
    assert len(snw) == 5


def test_add_users_duplicate(empty_db):
    """
    Tests adding a batch of users to the database
    """
    snw = SocialNetwork(empty_db)

    # just to make sure
    assert len(snw) == 0
    result = snw.add_users(SAMPLE_USERS_DATA)

    assert result == 3
    assert len(snw) == 3

    # Try to add them again
    result = snw.add_users(SAMPLE_USERS_DATA)

    assert result == 0
    assert len(snw) == 3


def test_add_statuses(empty_db):
    """
    Tests adding a batch of users to the database
    """
    snw = SocialNetwork(empty_db)

    # Pre-populate with users
    snw.add_users(SAMPLE_USERS_DATA)
    result = snw.add_statuses(SAMPLE_STATUS_DATA)
    assert result == 4

    # need to check if at least one was correct
    # user: 'bwinkle678' should have status: 'st12455'
    user = snw.search_user('bwinkle678')
    for status_update in user.status_updates:
        if status_update.status_id == 'st12455':
            break
    else:
        assert False, "id: 'st12455' not found in user 'bwinkle678'"


def test_add_statuses_user_not_there(empty_db):
    """
    Tests adding a batch of users to the database

    When some of the users are not there.
    """
    statuses = SAMPLE_STATUS_DATA
    # Add one more for non-existant user
    statuses.append({'user_id': 'xxxyyy',
                     'status_id': 'xxxyyyzzz',
                     'status_text': 'A second simple message from user: cbarker12'
                     })
    snw = SocialNetwork(empty_db)

    # Pre-populate with users
    snw.add_users(SAMPLE_USERS_DATA)

    # need to really do the test
    result = snw.add_statuses(statuses)

    assert snw.search_user('xxxyyy') is None
    assert result == 4



