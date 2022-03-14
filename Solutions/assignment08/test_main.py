"""
tests for the main driver code of the Social Network
"""

# less picky about style for test code
# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name

import io
from pathlib import Path
from unittest import mock

from loguru import logger

import main

from data_for_tests import empty_db, full_db  # pylint: disable=(unused-import

HERE = Path(__file__).parent


def setup_logger():
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


# ############
# Tests of the users table

# def test_init_empty_users(empty_db):
#     """
#     initiliaze and empty UserCollection
#     """
#     uc = main.init_user_collection(empty_db)

#     assert len(uc['users'])  == 0


# def test_init_full_users(full_db):
#     """
#     initiliaze a UserCollection from a database with data
#     """
#     uc = main.init_user_collection(full_db)

#     assert len(uc['users'])  == 3


def test_search_user(full_db):

    user = main.search_user('bwinkle678', full_db)

    assert user['user_id'] == 'bwinkle678'
    assert user['user_name'] == 'bwinkle'


def test_search_user_not_there(full_db):

    user = main.search_user('xxxx', full_db)

    assert user is None

def test_delete_user(full_db):
    """
    does delete_user actually delete a user?
    """
    uc = full_db

    start_len = len(uc['users'])
    uid = 'bwinkle678'
    result = main.delete_user(uid, uc)

    assert result is True
    assert len(uc['users'])  == start_len - 1

    assert main.search_user(uid, uc) is None


def test_delete_user_not_there(full_db):
    """
    deleting an non-existant user should return False
    """
    uc = full_db

    start_len = len(uc['users'])

    uid = 'x1x2x3x4'
    result = main.delete_user(uid, uc)

    assert result is False
    assert len(uc['users'])  == start_len

    assert main.search_user(uid, uc) is None


def test_add_user_new(empty_db):
    """
    tests adding a new user
    """
    uc = empty_db

    status = main.add_user('xxxxx',
                           'this@that.com',
                           'cbarker',
                           'Barker',
                           uc)

    assert status is True
    assert len(uc['users'])  == 1


def test_add_user_id_too_long(empty_db):
    """
    user_id can not be over 30 chars
    """
    uc = empty_db

    status = main.add_user('x' * 31,
                           'this@that.com',
                           'cbarker',
                           'Barker',
                           uc)

    assert status is False
    assert len(uc['users'])  == 0


def test_add_user_name_too_long(empty_db):
    """
    user_id can not be over 30 chars
    """
    uc = empty_db

    status = main.add_user('xxxxx',
                           'this@that.com',
                           'cbarker' * 5,
                           'Barker',
                           uc)

    assert status is False
    assert len(uc['users'])  == 0

def test_add_user_last_name_too_long(empty_db):
    """
    user_id can not be over 30 chars
    """
    uc = empty_db

    status = main.add_user('xxxxx',
                           'this@that.com',
                           'cbarker',
                           'Barker' * 17,
                           uc)

    assert status is False
    assert len(uc['users'])  == 0

def test_add_user_already_there(full_db):
    """
    tests adding a new user
    """
    uc = full_db

    start_len = len(uc['users'])
    status = main.add_user('cbarker12',
                         'this@something.com',
                         'fjones',
                         'Jones',
                         uc)

    assert status is False
    # but did it overwrite the user?
    assert main.search_user('cbarker12', uc)['user_name'] != 'fjones'
    assert start_len == len(uc['users'])


def test_update_user(full_db):
    uc = full_db

    # some test data
    user_id = 'bwinkle678'
    user_email = 'this@that.com'
    user_name = 'fbarnes'
    user_last_name = 'Barnes'

    result = main.update_user(user_id,
                              user_email,
                              user_name,
                              user_last_name,
                              uc)

    assert result is True

    user = main.search_user(user_id, uc)
    assert user['user_email'] == user_email
    assert user['user_name'] == user_name
    assert user['user_last_name'] == user_last_name

def test_update_user_not_there(full_db):

    uc = full_db

    user_id = 'xxxxx'
    user_email = 'this@that.com'
    user_name = 'fbarnes'
    user_last_name = 'Barnes'
    result = main.update_user(user_id, user_email, user_name, user_last_name, uc)

    assert result is False
    assert main.search_user('xxxxx', uc) is None

# ############
# Tests of the statuses table

def test_init_empty_status(empty_db):
    """
    initiliaze and empty UserStatusCollection

    NOTE: really a test of the fixture
    """

    assert len(empty_db['statuses']) == 0
    assert len(empty_db['users']) == 0


def test_init_full_status(full_db):
    """
    initiliaze a UserStatusCollection from a database with data

    NOTE: really a test of the fixture
    """
    usc = full_db

    assert len(usc['statuses']) == 4


def test_search_status(full_db):
    usc = full_db

    sid = 'st12455'
    status = main.search_status(sid, usc)

    assert status['status_id'] == sid
    assert status['user_id'] == 'bwinkle678'


def test_search_status_not_there(full_db):
    usc = full_db

    status = main.search_status('xxxx', usc)

    assert status is None


def test_delete_status(full_db):
    """
    does delete_status actually delete a status?
    """
    usc = full_db

    start_len = len(usc['statuses'])
    sid = 'st55555'
    result = main.delete_status(sid, usc)

    assert result is True
    assert len(usc['statuses']) == start_len - 1

    assert main.search_status(sid, usc) is None


def test_delete_status_not_there(full_db):
    """
    deleting an non-existant status should return False
    """
    usc = full_db

    start_len = len(usc['statuses'])

    sid = 'x1x2x3x4'
    result = main.delete_status(sid, usc)

    assert result is False
    assert len(usc['statuses']) == start_len

    assert main.search_status(sid, usc) is None


def test_add_status_new(full_db):
    """
    tests adding a new status

    NOTE: for this test, there is no user corresponding to the status
    """
    usc = full_db
    statuses = full_db['statuses']
    users = full_db['users']
    start_len = len(statuses)

    # get a valid user_id
    user_id = next(iter(users))['user_id']

    sid = 'xxxxxx'
    result = main.add_status(sid, user_id, 'just some text', usc)

    assert result is True
    assert len(statuses) == start_len + 1
    assert main.search_status(sid, usc)['status_id'] == sid


def test_add_status_user_not_there(empty_db):
    """
    You should not be able to add a status for a non-existant user
    """
    usc = empty_db
    assert len(empty_db['statuses']) == 0

    sid = 'xxxxxx'
    result = main.add_status(sid, 'yyyyy', 'just some text', usc)

    assert result is False

    assert len(empty_db['statuses']) == 0


def test_add_status_already_there(full_db):
    """
    tests adding a new status
    """
    usc = full_db

    start_len = len(usc['statuses'])
    result = main.add_status(user_id='new_user_id',
                             status_id='st12355',
                             status_text='A simple message from user: fjones34',
                             dataset=usc)

    assert result is False
    # but did it overwrite the status?
    assert main.search_status('st12355', usc)['user_id'] != 'new_user_id'
    assert start_len == len(usc['statuses'])


def test_modify_status_not_there(full_db):
    usc = full_db
    stat_id = '1111111'
    user_id = '12345'
    status_text = 'new status text'
    result = main.update_status(stat_id, user_id, status_text, usc)
    assert result is False


def test_modify_status_there(full_db):
    usc = full_db

    stat_id = 'st12355'
    user_id = 'cbarker12'
    status_text = 'new status text'

    print(main.search_status(stat_id, usc))
    result = main.update_status(stat_id, user_id, status_text, usc)
    assert result is True

    # check if the modify "took"
    status = main.search_status(stat_id, usc)
    assert status['status_id'] == stat_id
    assert status['status_text'] == 'new status text'


def test_load_users_good(empty_db):
    """
    tests : Opens a CSV file with user data and
            adds it to an existing instance of
            UserCollection

    If successful, it it returns True.

    This uses a "good" csv file
    """
    uc = empty_db

    result = main.load_users(HERE / 'example_accounts.csv', uc)

    # It should have loaded correctly and returned True
    assert result is True
    # did the data actually get loaded?
    uid = 'Keri.Royce8'
    assert main.search_user(uid, uc)['user_id'] == uid

def test_load_status_good(empty_db):
    """
    tests that loading a conforming CSV file status data works.
    """
    sc = empty_db
    # users need to be present to load status updates
    uc = empty_db
    main.add_user('evmiles97',
                  'emiles@company.com',
                  'evmiles',
                  'miles',
                  uc)
    main.add_user('dave03',
                  'daveB@company.com',
                  'dave',
                  'Jones',
                  uc)

    filename = HERE / "example_status_updates.csv"
    result = main.load_status_updates(filename, sc)

    # It should have loaded correctly and returned True
    assert result is True

    # did the data actually get loaded?
    assert len(empty_db['statuses']) == 3

    # is it correct?
    # dave03_00001,dave03,Sunny in Seattle this morning
    sid = 'dave03_00001'
    stat = main.search_status(sid, sc)
    assert stat['status_id'] == sid
    assert stat['user_id'] == 'dave03'
    assert stat['status_text'] == 'Sunny in Seattle this morning'


@mock.patch('builtins.open')
def test_load_users_bad(mocked_open, empty_db):
    """
    tests : Opens a CSV file with user data and
            adds it to an existing instance of
            UserCollection

        - Returns False if there are any errors
        (such as empty fields in the source CSV file)

    This uses a "bad" csv file
    """
    # this CSV snippet has an empty field in the last row.
    mocked_open.return_value = io.StringIO("""USER_ID,EMAIL,NAME,LASTNAME
evmiles97, eve.miles@uw.edu,Eve,Miles
dave03,david.yuen@gmail.com,,Yuen
""")

    uc = empty_db

    result = main.load_users("dummy file name", uc)

    # It should have failed loading and returned False
    assert result is False
    # did the data at the error line actually get loaded?

    assert main.search_user('dave03', uc) is None
    # did the data before the error line get loaded?
    # Note: this wasn't clear in the specifcation, but
    #       it's a bad idea to load some of the data, but not
    #       all -- there would be no way to know the state of
    #       the database
    assert main.search_user('evmiles97', uc) is None


@mock.patch('builtins.open')
def test_load_users_bad_header(mocked_open, empty_db):
    """
    Trying to load a CSV file with the wrong header should fail
    """
    mocked_open.return_value = io.StringIO("""USER_ID,EMAIL,FIRSTNAME,LASTNAME
evmiles97, eve.miles@uw.edu,Eve,Miles
dave03,david.yuen@gmail.com,Dave,Yuen
""")
    result = main.load_users('bad_header_file', empty_db)

    # It should have failed loading and returned False
    assert result is False

    assert len(empty_db['users']) == 0

@mock.patch('builtins.open')
def test_load_users_missing_field(mocked_open, empty_db):
    """
    Trying to load a CSV file with the wrong header should fail
    """
    mocked_open.return_value = io.StringIO("""USER_ID,EMAIL,NAME,LASTNAME
evmiles97,Eve,Miles
dave03,david.yuen@gmail.com,Dave,Yuen
""")
    result = main.load_users('bad_header_file', empty_db)

    # It should have failed loading and returned False
    assert result is False

    assert len(empty_db['users']) == 0



#     def test_load_users_bad_row(self):
#         """
#         Returns False if there are any errors
#         (such as empty fields in the source CSV file)

#         This uses a csv file with a bad row
#         """
#         uc = self.empty_user_collection

#         result = main.load_users(self.bad_row_file, uc)

#         # It should have failed loading and returned False
#         assert result is False

#         # it should not have created a database
#         assert len(uc['users'])  == 0


# class TestUserCollectionFull(unittest.TestCase):
#     """
#     tests for the UserCollection functions that need a
#     database with data in it.
#     """
#     def setUp(self):
#         self.database = start_database()
#         self.full_user_collection = make_full_user_collection()

#     def tearDown(self):
#         cleanup_database(self.database)

#     @classmethod
#     def setUpClass(cls):
#         """
#         create a couple data files with bad data
#         """
#         cls.bad_header_file = write_bad_header(HERE / "bad_header.csv")
#         cls.bad_row_file = write_bad_row(HERE / "bad_row.csv")

#     @classmethod
#     def tearDownClass(cls):
#         os.remove(HERE / "bad_header.csv")
#         os.remove(HERE / "bad_row.csv")

#     def test_init_full_user_status_collection(self):
#         """
#         make sure you get a new, UserStatusCollection
#         with some data in it

#         (really testing the fixture)
#         """
#         uc = main.init_user_collection()

#         self.assertIsInstance(uc, UserCollection)
#         self.assertEqual(len(uc['users']) , 3)

#     def test_search_user_there(self):
#         """
#         tests that a user can be found in the collection
#         """
#         user = main.search_user('fjones34',
#                                 self.full_user_collection)

#         print(user)
#         assert user.user_id == 'fjones34'

#     def test_search_user_not_there(self):
#         """
#         tests that a user that isn't there gets a None user
#         """
#         user = main.search_user('somejunk',
#                                 self.full_user_collection)

#         assert user is None

#     def test_add_user_already_there(self):
#         """
#         tests adding a user to a user_collection
#         """
#         uc = self.full_user_collection

#         status = main.add_user('cbarker12',
#                                'this@something.com',
#                                'fjones',
#                                'Jones',
#                                uc)

#         assert status is False
#         # but did it overwrite the user?
#         assert main.search_user('cbarker12', uc).user_name != 'fjones'

#     def test_delete_user(self):
#         uc = self.full_user_collection
#         uid = 'fjones34'
#         assert main.delete_user(uid, uc) is True

#         assert main.search_user(uid, uc) is None

#     def test_delete_user_not_there(self):
#         uc = self.full_user_collection
#         uid = 'xxxxxxx'
#         assert main.delete_user(uid, uc) is False

#     def test_update_user(self):
#         uc = self.full_user_collection
#         user_id = 'bwinkle678'
#         email = 'this@that.com'
#         user_name = 'fbarnes'
#         user_last_name = 'Barnes'

#         result = main.update_user(user_id,
#                                   email,
#                                   user_name,
#                                   user_last_name,
#                                   uc)

#         assert result is True

#         user = main.search_user(user_id, uc)
#         assert user.user_email == email
#         assert user.user_name == user_name
#         assert user.user_last_name == user_last_name

#     def test_update_user_not_there(self):
#         uc = self.full_user_collection
#         user_id = 'xxxxx'
#         email = 'this@that.com'
#         user_name = 'fbarnes'
#         user_last_name = 'Barnes'
#         result = main.update_user(user_id, email, user_name, user_last_name, uc)

#         assert result is False


# class TestStatusCollectionEmpty(unittest.TestCase):
#     """
#     tests for the StatusCollection functions
#     """
#     def setUp(self):
#         self.database = start_database()
#         self.empty_status_collection = main.init_status_collection()

#     def tearDown(self):
#         cleanup_database(self.database)

#     def test_init_status_collection(self):
#         """make sure you get a new, empty UserStatusCollection"""
#         sc = main.init_status_collection()

#         self.assertIsInstance(sc, UserStatusCollection)
#         self.assertEqual(len(sc), 0)


#     @mock.patch('builtins.open')
#     def test_load_status_bad_header(self, mocked_open):
#         """
#         a csv file with a bad header should fail
#         """
#         mocked_open.return_value = io.StringIO("STATUS_ID,USER_IDSTATUS_TEXT")

#         sc = self.empty_status_collection
#         result = main.load_status_updates(HERE / "status_updates.csv", sc)
#         # It should have not loaded correctly
#         assert result is False

#     @mock.patch('builtins.open')
#     def test_load_status_missing_field(self, mocked_open):
#         """
#         a csv file with a bad header should fail
#         """
#         mocked_open.return_value = io.StringIO("""STATUS_ID,USER_ID,STATUS_TEXT
# evmiles97_00001,evmiles97,"Code is finally compiling"
# dave03_00001dave03,"Sunny in Seattle this morning"
# evmiles97_00002,evmiles97,"Perfect weather for a hike"
# """)

#         sc = self.empty_status_collection
#         result = main.load_status_updates(HERE / "status_updates.csv", sc)
#         # It should have loaded correctly and returned True
#         assert result is False

#         # the StatusCollection should be empty
#         assert len(sc) == 0

#     @mock.patch('builtins.open')
#     def test_load_status_empty_field(self, mocked_open):
#         """
#         a csv file with a bad header should fail
#         """
#         mocked_open.return_value = io.StringIO("""STATUS_ID,USER_ID,STATUS_TEXT
# evmiles97_00001,evmiles97,"Code is finally compiling"
# dave03_00001, dave03,"Sunny in Seattle this morning"
# evmiles97_00002, ,"Perfect weather for a hike"
# """)

#         sc = self.empty_status_collection
#         result = main.load_status_updates(HERE / "status_updates.csv", sc)
#         # It should have loaded correctly and returned True
#         assert result is False

#         # the StatusCollection should be empty
#         assert len(sc) == 0


# class TestStatusCollectionFull(unittest.TestCase):
#     """
#     tests for the StatusCollection functions that require
#     a pre-loaded database
#     """
#     def setUp(self):
#         self.database = start_database()
#         fuc, fsc = populate_collections()
#         self.full_user_collection = fuc
#         self.full_status_collection = fsc

#     def tearDown(self):
#         cleanup_database(self.database)

#     def test_init_status_collection(self):
#         """
#         make sure you get a new, populated UserStatusCollection

#         Really testing the fixture
#         """

#         sc = main.init_status_collection()

#         self.assertIsInstance(sc, UserStatusCollection)
#         self.assertEqual(len(sc), 4)

#     def test_add_status(self):
#         """
#         tests adding a new status

#         note: the user_id must exist
#         """

#         usc = self.full_status_collection

#         start_len = len(usc['statuses']

#         sid = 'xxxxxx'
#         # make sure to use a user_id that exists in the User table
#         result = main.add_status(sid, 'cbarker12', 'just some text', usc)

#         assert result is True

#         assert len(usc['statuses']) == start_len + 1

#     def test_search_status(self):
#         """
#         checks that a valid status is found, and is the right one
#         """

#         status_id = 'st12345'
#         result = main.search_status(status_id, self.full_status_collection)

#         assert result['status_id'] == status_id

#     def test_search_status_not_there(self):
#         """
#         checks that a valid status is found, and is the right one
#         """

#         status_id = 'xxxxx'
#         result = main.search_status(status_id, self.full_status_collection)

#         assert result is None

#     def test_delete_status_not_there(self):
#         sc = self.full_status_collection
#         stat_id = 'xxxxxx'
#         result = main.delete_status(stat_id, sc)

#         assert result is False

#     def test_delete_status_there(self):
#         sc = self.full_status_collection
#         stat_id = 'st12355'
#         result = main.delete_status(stat_id, sc)
#         assert result is True

#         # check that it was really deleted
#         result = main.search_status(stat_id, sc)
#         assert result is None

#     def test_update_status_not_there(self):
#         sc = self.full_status_collection
#         stat_id = '1111111'
#         user_id = '12345'
#         status_text = 'new status text'
#         result = main.update_status(stat_id, user_id, status_text, sc)
#         assert result is False

#     def test_update_status_there(self):
#         sc = self.full_status_collection
#         stat_id = 'st12355'
#         user_id = '12345'
#         status_text = 'new status text'
#         result = main.update_status(stat_id, user_id, status_text, sc)
#         assert result is True

#         # check if the update "took"
#         status = main.search_status(stat_id, sc)
#         assert status.status_id == stat_id
#         assert status.status_text == 'new status text'

#     def test_add_status_already_there(self):
#         sc = self.full_status_collection
#         sid = 'st12345'

#         result = main.add_status('yyyyy', sid, 'just some text', sc)

#         assert result is False
#         assert main.search_status(sid, sc).user_id != 'yyyyy'
