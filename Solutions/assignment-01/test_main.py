"""
tests for the main driver code of the Social Network
"""

# less picky about style for test code
# pylint: disable=C0103 # to allow short names in the tests
# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring

import os
import io
import unittest
from pathlib import Path
from unittest import mock

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


def make_full_status_collection():
    """
    Similar to before, we need a StatusCollection in order to
    test stuff.
    """
    statuses = [{'user_id': 'cbarker12',
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

    sc = main.init_status_collection()
    for stat in statuses:
        sc.add_status(**stat)

    return sc



def write_bad_header(filename):
    """
    writes an accounts csv file with a bad header
    """
    with open(filename, 'w', encoding='utf-8') as outfile:
        outfile.write("""USER_ID,EMAIL,,NAME,LASTNAME
evmiles97, eve.miles@uw.edu,Eve,Miles
dave03,david.yuen@gmail.com, David,Yuen
""")
    return filename

def write_bad_row(filename):
    """
    writes an accounts csv file with a bad row
    (one two few elements)
    """
    with open(filename, 'w', encoding='utf-8') as outfile:
        outfile.write("""USER_ID,EMAIL,NAME,LASTNAME
evmiles97, eve.miles@uw.edu,Miles
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

    @classmethod
    def setUpClass(cls):
        """
        create a couple data files with bad data
        """
        cls.bad_header_file = write_bad_header(HERE / "bad_header.csv")
        cls.bad_row_file = write_bad_row(HERE / "bad_row.csv")

    @classmethod
    def tearDownClass(cls):
        os.remove(HERE / "bad_header.csv")
        os.remove(HERE / "bad_row.csv")

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

    def test_load_users_bad_row(self):
        """
        Returns False if there are any errors
        (such as empty fields in the source CSV file)

        This uses a csv file with a bad row
        """
        uc = self.empty_user_collection

        result = main.load_users(self.bad_row_file, uc)

        # It should have failed loading and returned False
        assert result is False

        # it should not have created a database
        assert not uc.database

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

        assert result is True

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

    def test_delete_user(self):
        uc = self.full_user_collection
        uid = 'fjones34'
        assert main.delete_user(uid, uc) is True

        assert main.search_user(uid, uc).user_id is None

    def test_delete_user_not_there(self):
        uc = self.full_user_collection
        uid = 'xxxxxxx'
        assert main.delete_user(uid, uc) is False

    def test_update_user(self):
        uc = self.full_user_collection
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
        uc = self.full_user_collection
        user_id = 'xxxxx'
        email = 'this@that.com'
        user_name = 'fbarnes'
        user_last_name = 'Barnes'
        result = main.update_user(user_id, email, user_name, user_last_name, uc)

        assert result is False

class TestStatusCollection(unittest.TestCase):
    """
    tests for the StatusCollection functions
    """
    def setUp(self):
        self.empty_status_collection = main.init_status_collection()
        self.full_status_collection = make_full_status_collection()
        # self.bad_header_file = write_bad_header(HERE / "bad_header.csv")
        # self.bad_header_file = write_bad_header(HERE / "bad_header.csv")

    # @classmethod
    # def setUpClass(cls):
    #     cls.bad_header_file = write_bad_header(HERE / "bad_header.csv")

    # @classmethod
    # def tearDownClass(cls):
    #     os.remove(HERE / "bad_header.csv")

    def test_init_status_collection(self):
        """make sure you get a new, empty UserStatusCollection"""
        sc = main.init_status_collection()

        self.assertIsInstance(sc, UserStatusCollection)
        self.assertEqual(len(sc.database), 0)

    def test_search_status(self):
        """
        checks that a valid status is found, and is the right one
        """

        status_id = 'st12345'
        result = main.search_status(status_id, self.full_status_collection)

        assert result.status_id == status_id

    def test_search_status_not_there(self):
        """
        checks that a valid status is found, and is the right one
        """

        status_id = 'xxxxx'
        result = main.search_status(status_id, self.full_status_collection)

        assert result is None

    def test_delete_status_not_there(self):
        sc = self.full_status_collection
        stat_id = 'xxxxxx'
        result = main.delete_status(stat_id, sc)

        assert result is False

    def test_delete_status_there(self):
        sc = self.full_status_collection
        stat_id = 'st12355'
        result = main.delete_status(stat_id, sc)
        assert result is True

        # check that it was really deleted
        result = main.search_status(stat_id, sc)
        assert result is None

    def test_update_status_not_there(self):
        sc = self.full_status_collection
        stat_id = '1111111'
        user_id = '12345'
        status_text = 'new status text'
        result = main.update_status(stat_id, user_id, status_text, sc)
        assert result is False

    def test_update_status_there(self):
        sc = self.full_status_collection
        stat_id = 'st12355'
        user_id = '12345'
        status_text = 'new status text'
        result = main.update_status(stat_id, user_id, status_text, sc)
        assert result is True

        # check if the update "took"
        status = main.search_status(stat_id, sc)
        assert status.status_id == stat_id
        assert status.status_text == 'new status text'

    def test_add_status(self):
        sc = self.empty_status_collection

        sid = 'xxxxxx'
        main.add_status(sid, 'yyyyy', 'jsut some text', sc)

        assert main.search_status(sid, sc) is None

    def test_add_status_already_there(self):
        sc = self.full_status_collection
        sid = 'st12345'
        print(sc.database)

        result = main.add_status('yyyyy', sid, 'just some text', sc)
        print(sc.database)

        assert result is False
        assert main.search_status(sid, sc).user_id != 'yyyyy'

    def test_load_status_good(self):
        """
        tests : Opens a CSV file with user data and
                adds it to an existing instance of
                UserCollection

        If successful, it it returns True.

        This uses a "good" csv file
        """
        sc = self.empty_status_collection

        result = main.load_status_updates(HERE / "status_updates.csv", sc)

        # It should have loaded correctly and returned True
        assert result is True

        # did the data actually get loaded?
        assert main.search_status('evmiles97_00002', sc).user_id == 'evmiles97'

    @mock.patch('builtins.open')
    def test_load_status_bad_header(self, mocked_open):
        """
        a csv file with a bad header should fail
        """
        mocked_open.return_value = io.StringIO("STATUS_ID,USER_IDSTATUS_TEXT")

        sc = self.empty_status_collection
        result = main.load_status_updates(HERE / "status_updates.csv", sc)
        # It should have not loaded correctly
        assert result is False

    @mock.patch('builtins.open')
    def test_load_status_missing_field(self, mocked_open):
        """
        a csv file with a bad header should fail
        """
        mocked_open.return_value = io.StringIO("""STATUS_ID,USER_ID,STATUS_TEXT
evmiles97_00001,evmiles97,"Code is finally compiling"
dave03_00001dave03,"Sunny in Seattle this morning"
evmiles97_00002,evmiles97,"Perfect weather for a hike"
""")

        sc = self.empty_status_collection
        result = main.load_status_updates(HERE / "status_updates.csv", sc)
        # It should have loaded correctly and returned True
        assert result is False

        # the StatusCollection should be empty
        assert not sc.database

    @mock.patch('builtins.open')
    def test_load_status_empty_field(self, mocked_open):
        """
        a csv file with a bad header should fail
        """
        mocked_open.return_value = io.StringIO("""STATUS_ID,USER_ID,STATUS_TEXT
evmiles97_00001,evmiles97,"Code is finally compiling"
dave03_00001, dave03,"Sunny in Seattle this morning"
evmiles97_00002, ,"Perfect weather for a hike"
""")

        sc = self.empty_status_collection
        result = main.load_status_updates(HERE / "status_updates.csv", sc)
        # It should have loaded correctly and returned True
        assert result is False

        # the StatusCollection should be empty
        assert not sc.database

    def test_save_status_correct(self):
        """
        make sure the file was written correctly
        """

        # reload it to see if it worked
        # this is tough -- as this test depends on the load_users
        # working. You could look at the generated csv file.

        sc = self.full_status_collection

        filename = HERE / "temp_status_updates.csv"
        result = main.save_status_updates(filename, sc)

        assert result is True

        uc = self.empty_status_collection
        main.load_status_updates(filename, uc)

        sid = 'st12455'
        assert main.search_status(sid, sc).status_id == sid

    def test_save_status_bad_filename(self):
        """
        make sure the file was written correctly
        """

        # reload it to see if it worked
        # this is tough -- as this test depends on the load_users
        # working. You could look at the generated csv file.

        sc = self.full_status_collection

        filename = "/random/bad/path/filename.csv"
        result = main.save_status_updates(filename, sc)

        assert result is False


# if __name__ == "__main__":
#    unittest.main()
