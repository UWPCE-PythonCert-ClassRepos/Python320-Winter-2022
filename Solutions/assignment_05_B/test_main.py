"""
tests for the main driver code of the Social Network
"""

# less picky about style for test code
# pylint: disable=C0103 # to allow short names in the tests
# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring
# pylint: disable=duplicate-code

import unittest
from pathlib import Path

from loguru import logger

import main
from social_network import SocialNetwork, StatusUpdate, start_mongo

HERE = Path(__file__).parent

good_account_file = HERE / "accounts_small.csv"
bad_account_file = HERE / "accounts_bad.csv"

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

def setup_logger():  # pragma: no cover
    """
    Set up the logger for the test runs
    """
    # create a logfile with today's date
    logfilename = "logfile_for_test_runs.txt"
    logger.add(logfilename,
               mode='a',  # append, so the file sticks around
               encoding='utf-8',
               format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
               retention=3  # keep the last 3 logfile
               )


setup_logger()


class TestSocialNetwork(unittest.TestCase):
    """
    tests for the UserCollection functions
    """

    def setUp(self):
        self.client = start_mongo()
        self.client.drop_database('test_database')
        self.database = self.client['test_database']
        self.full_social_network = SocialNetwork(self.database)
        for user in SAMPLE_USERS_DATA:
            self.full_social_network.add_user(**user)
        for stat in SAMPLE_STATUS_DATA:
            self.full_social_network.add_status(**stat)

    def tearDown(self):
        self.client.drop_database(self.database)
        self.client.close()

    def test_init_social_network(self):
        """
        Make sure you get a new UserCollection with test data in it

        Really a test of the fixture
        """
        uc = main.init_social_network(self.database)

        self.assertIsInstance(uc, SocialNetwork)
        self.assertEqual(len(uc), 3)

    def test_search_user_there(self):
        """
        tests that a user can be found in the collection
        """
        user = main.search_user('fjones34',
                                self.full_social_network)

        print(user)
        assert user.user_id == 'fjones34'

        print(user.status_updates)
        assert user.status_updates == [StatusUpdate(
                              status_id='st12355',
                              status_text='A simple message from user: fjones34')
                              ]

    def test_search_user_not_there(self):
        """
        tests that a user that isn't there gets a None user
        """
        user = main.search_user('somejunk',
                                self.full_social_network)

        assert user is None

    def test_add_user(self):
        """
        tests adding a user to a user_collection
        """
        uc = self.full_social_network

        status = main.add_user('xxxxx',
                               'this@that.com',
                               'cbarker',
                               'Barker',
                               uc)

        assert status is True

        # but did it actually add the user?
        user = main.search_user('xxxxx', uc)
        assert user.user_id == 'xxxxx'
        assert user.email == 'this@that.com'

    def test_add_user_already_there(self):
        """
        Tests adding a user to a user_collection

        If the user with that id is already there, it should not add anything.
        """
        uc = self.full_social_network

        status = main.add_user('cbarker12',
                               'this@something.com',
                               'fjones',
                               'Jones',
                               uc)

        assert status is False
        # but did it overwrite the user?
        assert main.search_user('cbarker12', uc).user_name != 'fjones'


    def test_delete_user(self):
        uc = self.full_social_network
        uid = 'fjones34'

        assert main.delete_user(uid, uc) is True

        assert main.search_user(uid, uc) is None

    def test_delete_user_not_there(self):
        uc = self.full_social_network
        uid = 'xxxxxxx'
        assert main.delete_user(uid, uc) is False

    def test_update_user(self):
        uc = self.full_social_network
        user_id = 'bwinkle678'
        email = 'this@that.com'
        user_name = 'fbarnes'
        user_last_name = 'Barnes'

        result = main.update_user(user_id,
                                  email,
                                  user_name,
                                  user_last_name,
                                  uc)

        assert result is True

        user = main.search_user(user_id, uc)
        assert user.email == email
        assert user.user_name == user_name
        assert user.user_last_name == user_last_name

    def test_update_user_not_there(self):
        uc = self.full_social_network
        user_id = 'xxxxx'
        email = 'this@that.com'
        user_name = 'fbarnes'
        user_last_name = 'Barnes'
        result = main.update_user(user_id, email, user_name, user_last_name, uc)

        assert result is False

    def test_search_status(self):
        """
        checks that a valid status is found, and is the right one
        """

        status_id = 'st12345'
        result = main.search_status(status_id, self.full_social_network)

        print("****result:", result)
        assert result.status_id == status_id

    def test_search_status_not_there(self):
        """
        checks that a non-existant status returns None
        """

        status_id = 'xxxxx'
        result = main.search_status(status_id, self.full_social_network)

        assert result is None

    def test_delete_status_not_there(self):
        sc = self.full_social_network
        stat_id = 'xxxxxx'
        result = main.delete_status(stat_id, sc)
        assert result is False

    def test_delete_status_there(self):
        sc = self.full_social_network
        stat_id = 'st12355'
        result = main.delete_status(stat_id, sc)
        assert result

        # check that it was really deleted
        result = main.search_status(stat_id, sc)
        assert result is None

    def test_update_status_not_there(self):
        sc = self.full_social_network
        stat_id = '1111111'
        status_text = 'new status text'
        result = main.update_status(stat_id, status_text, sc)
        assert result is False

    def test_update_status_there(self):
        sc = self.full_social_network
        stat_id = 'st12355'
        status_text = 'new status text'
        result = main.update_status(stat_id, status_text, sc)
        assert bool(result) is True

        # check if the update "took"
        status = main.search_status(stat_id, sc)
        assert status.status_id == stat_id
        assert status.status_text == 'new status text'

    def test_add_status(self):
        """
        add a status to an existing user
        """
        snw = self.full_social_network

        uid = 'bwinkle678'
        status_text = "just some text"
        main.add_status(user_id=uid,
                        status_id='yyyyyy',
                        status_text=status_text,
                        status_collection=snw)

        user = main.search_user(uid, snw)

        assert status_text in [ud.status_text for ud in user.status_updates]


    def test_add_status_already_there(self):
        sc = self.full_social_network
        sid = 'st12345'

        result = main.add_status('yyyyy', sid, 'just some text', sc)

        assert result is False

        assert main.search_status(sid, sc).status_text != 'just some text'


class TestSocialNetworkEmpty(unittest.TestCase):
    """
    tests that require an empty database
    """
    def setUp(self):
        self.client = start_mongo()
        self.client.drop_database('test_database')
        self.database = self.client['test_database']
        self.full_social_network = SocialNetwork(self.database)

    def tearDown(self):
        self.client.drop_database(self.database)
        self.client.close()

    def test_load_status_good(self):
        """
        tests : Opens a CSV file with user data and
                adds it to an existing instance of
                UserCollection

        If successful, it it returns True.

        This uses a "good" csv file
        """
        snw = self.full_social_network

        # have to load users first
        main.load_users(HERE / "accounts_small.csv", snw)
        result = main.load_status_updates(HERE / "status_updates_small.csv", snw)

        # It should have loaded correctly and returned True
        assert result is True

        # did the data actually get loaded?
        user = main.search_user('evmiles97', snw)
        assert user.status_updates[0].status_text == 'Code is finally compiling'
        assert user.status_updates[1].status_text == 'My second post!'

    def test_load_users_good(self):
        """
        tests : Opens a CSV file with user data and
                adds it to an existing instance of
                UserCollection

        If successful, it it returns True.

        This uses a "good" csv file
        """
        uc = self.full_social_network

        result = main.load_users(good_account_file, uc)

        # It should have loaded correctly and returned True
        assert result is True
        # did the data actually get loaded?
        assert main.search_user('dave03', uc).user_id == 'dave03'
