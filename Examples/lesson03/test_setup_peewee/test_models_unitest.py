"""
example of using unitest fixtures to test models
"""

# pylint: disable=no-self-use
# pylint: disable=invalid-name

import unittest

from models import start_database

import users


class TestUsersEmpty(unittest.TestCase):
    """
    test that start with an empty database
    """

    def setUp(self):
        """start up a populated database"""
        self.db = start_database(":memory:", clear=True)

    def tearDown(self):
        """probably not necceasry for memory db, but good form"""
        self.db.close()

    def test_init_empty(self):
        """
        This is mostly testing the fixture, but good to do
        """
        user_col = users.UserCollection()
        assert len(user_col) == 0

    def test_add_user(self):
        """Does adding a user work"""
        user_col = users.UserCollection()
        start_len = len(user_col)
        result = user_col.add_user('username', 'name')
        assert result is True
        assert len(user_col) == 1 + start_len


class TestUsersPopulated(unittest.TestCase):
    """
    test that start with an empty database
    """

    def setUp(self):
        """start up a populated database"""
        self.db = start_database(":memory:", clear=True)
        # put some stuff in it
        user_col = users.UserCollection()
        user_col.add_user(user_id="cb1234", user_name="cbarker")
        user_col.add_user(user_id="fb4444", user_name="fbarnes")

    def tearDown(self):
        """probably not necceasry for memory db, but good form"""
        self.db.close()

    def test_init_populated(self):
        """
        This is mostly testing the fixture, but good to do
        """
        user_col = users.UserCollection()
        assert len(user_col) == 2

    def test_search_user(self):
        """
        can it find an existing user
        """
        user_col = users.UserCollection()
        user = user_col.search_user("cb1234")
        assert user.user_id == "cb1234"
        assert user.user_name == "cbarker"
