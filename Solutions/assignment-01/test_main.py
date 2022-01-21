"""
tests for the main driver code of the Social Network
"""

# pylint: disable=C0103 # to allow short names in the tests
# pylint: disable=invalid-name

import os
import unittest
from pathlib import Path

import main
from users import UserCollection
from user_status import UserStatusCollection

HERE = Path(__file__).parent

good_account_file = HERE / "accounts.csv"
bad_account_file = HERE / "accounts_bad.csv"


def make_full_user_collection():
    """
    A bit of a chicken-egg problem here

    You need the function in main in order to actually test many of them

    Here we make a utility that creates some object for testing.

    It uses the stuff in users.py directly, but could be swapped out
    later if the implimentation changes.
    """
    users = [{'user_id': 'cbarker12',
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

    uc = main.init_user_collection()
    for user in users:
        uc.add_user(**user)

    return uc


def write_bad_header(filename):
    with open(filename, 'w', encoding='utf-8') as outfile:
        outfile.write("""USER_ID,EMAIL,,NAME,LASTNAME
evmiles97, eve.miles@uw.edu,Eve,Miles
dave03,david.yuen@gmail.com, David,Yuen
""")
    return filename


class TestUserCollection(unittest.TestCase):
    """
    tests for the UserCollection functions
    """

    def setUp(self):
        self.empty_user_collection = main.init_user_collection()
        self.full_user_collection = make_full_user_collection()
        # self.bad_header_file = write_bad_header(HERE / "bad_header.csv")
        # self.bad_header_file = write_bad_header(HERE / "bad_header.csv")

    @classmethod
    def setUpClass(cls):
        cls.bad_header_file = write_bad_header(HERE / "bad_header.csv")

    @classmethod
    def tearDownClass(cls):
        os.remove(HERE / "bad_header.csv")

    def test_init_user_collection(self):
        """make sure you get a new, empty UserStatusCollection"""
        uc = main.init_user_collection()

        self.assertIsInstance(uc, UserCollection)
        self.assertEqual(len(uc.database), 0)

    def test_search_user_there(self):
        """
        tests that a user can be found in the collection
        """
        user = main.search_user('fjones34',
                                self.full_user_collection)

        print(user)
        assert user.user_id == 'fjones34'

    def test_search_user_not_there(self):
        """
        tests that a user that isn't there gets a None user
        """
        user = main.search_user('somejunk',
                                self.full_user_collection)

        assert user.user_id is None

    def test_add_user(self):
        """
        tests adding a user to a user_collection
        """
        uc = self.empty_user_collection

        status = main.add_user('xxxxx',
                               'this@that.com',
                               'cbarker',
                               'Barker',
                               uc)

        assert status is True

        print(main.search_user('xxxxx', uc))
        # self.user_id = user_id
        # self.email = email
        # but did it actually add the user?
        assert main.search_user('xxxxx', uc).user_id == 'xxxxx'
        assert main.search_user('xxxxx', uc).email == 'this@that.com'

    def test_add_user_already_there(self):
        """
        tests adding a user to a user_collection
        """
        uc = self.full_user_collection

        status = main.add_user('cbarker12',
                               'this@something.com',
                               'fjones',
                               'Jones',
                               uc)

        assert status is False
        # but did it overwrite the user?
        assert main.search_user('cbarker12', uc).user_name != 'fjones'

    def test_load_users_good(self):
        """
        tests : Opens a CSV file with user data and
                adds it to an existing instance of
                UserCollection

        If successful, it it returns True.

        This uses a "good" csv file
        """
        uc = self.empty_user_collection

        result = main.load_users(good_account_file, uc)

        # It should have loaded correctly and returned True
        assert result is True
        # did the data actually get loaded?
        assert main.search_user('dave03', uc).user_id == 'dave03'

    def test_load_users_bad(self):
        """
        tests : Opens a CSV file with user data and
                adds it to an existing instance of
                UserCollection

            - Returns False if there are any errors
            (such as empty fields in the source CSV file)

        This uses a "bad" csv file
        """
        uc = self.empty_user_collection

        result = main.load_users(bad_account_file, uc)

        # It should have failed loading and returned False
        assert result is False
        # did the data at the error line actually get loaded?
        assert main.search_user('dave03', uc).user_id is None
        # did the data before the error line get loaded?
        # Note: this wasn't clear in the specifcation, but
        #       it's a bad idea to load some of the data, but not
        #       all -- there would be no way to know the state of
        #       the database
        assert main.search_user('evmiles97', uc).user_id is None

    def test_load_users_bad_header(self):
        """
        tests : Opens a CSV file with user data and
                adds it to an existing instance of
                UserCollection

            - Returns False if there are any errors
            (such as empty fields in the source CSV file)

        This uses a "bad" csv file
        """
        uc = self.empty_user_collection

        result = main.load_users(self.bad_header_file, uc)

        # It should have failed loading and returned False
        assert result is False

        assert not uc.database

        # # did the data at the error line actually get loaded?
        # assert main.search_user('dave03', uc).user_id is None
        # # did the data before the error line get loaded?
        # # Note: this wasn't clear in the specifcation, but
        # #       it's a bad idea to load some of the data, but not
        # #       all -- there would be no way to know the state of
        # #       the database
        # assert main.search_user('evmiles97', uc).user_id is None


    def test_save_users(self):
        """
        tests saving the user collection to a csv file
        """
        uc = self.full_user_collection

        filename = HERE / "temp_accounts.csv"
        result = main.save_users(filename, uc)

        assert result is True
        assert filename.is_file()

    def test_save_users_correct(self):
        """
        make sure the file was written correctly
        """

        # reload it to see if it worked
        # this is tough -- as this test depends on the load_users
        # working. You could look at the generated csv file.

        uc = self.full_user_collection

        filename = HERE / "temp_accounts.csv"
        result = main.save_users(filename, uc)

        uc = self.empty_user_collection
        main.load_users(filename, uc)

        uid = 'bwinkle678'
        assert main.search_user(uid, uc).user_id == uid

    def test_save_users_bad_file(self):
        """
        should fail if the file path is bad
        """
        uc = self.full_user_collection
        result = main.save_users(Path() / 'non' / 'existant' / 'file.csv', uc)

        assert result is False


class TestStatusCollection(unittest.TestCase):
    """
    tests for the StatusCollection functions
    """

    def test_init_status_collection(self):
        """make sure you get a new, empty UserStatusCollection"""
        sc = main.init_status_collection()

        self.assertIsInstance(sc, UserStatusCollection)
        self.assertEqual(len(sc.database), 0)


if __name__ == "__main__":
   unittest.main()
