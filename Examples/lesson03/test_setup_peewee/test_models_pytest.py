"""
example of a pytest fixture, and how to use it to

test functionality of your models
"""
# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
# pylint: disable=invalid-name

import pytest

from models import start_database

import users


@pytest.fixture
def empty_db():
    """
    initialize an empty database
    """
    # setup
    db = start_database(":memory:", clear=True)
    yield db

    # teardown
    # stricly speaking, the isn't required, as a memory database
    # goes away when it's not used anymore.
    db.close()


@pytest.fixture
def populated_db():
    """
    initialize an empty database
    """
    # setup
    db = start_database(":memory:", clear=True)

    # put some stuff in it
    user_col = users.UserCollection()
    user_col.add_user(user_id="cb1234", user_name="cbarker")
    user_col.add_user(user_id="fb4444", user_name="fbarnes")

    yield db

    # teardown
    # stricly speaking, the isn't required, as a memory database
    # goes away when it's not used anymore.
    db.close()


def test_init_empty(empty_db):
    """
    This is mostly testing the fixture, but good to do
    """
    user_col = users.UserCollection()
    assert len(user_col) == 0


def test_init_populated(populated_db):
    """
    This is mostly testing the fixture, but good to do
    """
    user_col = users.UserCollection()
    assert len(user_col) == 2


def test_add_user(empty_db):
    """can we add a user"""
    user_col = users.UserCollection()
    start_len = len(user_col)
    result = user_col.add_user('username', 'name')
    assert result is True
    assert len(user_col) == 1 + start_len


def test_search_user(populated_db):
    """can it find and exsiting user """
    user_col = users.UserCollection()
    user = user_col.search_user("cb1234")
    assert user.user_id == "cb1234"
    assert user.user_name == "cbarker"
