"""
tests for Social Network code

NOTE: most functionality is tested by test_main
"""

# pylint: disable=missing-function-docstring

import copy

from dc_example import User, StatusUpdate


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
