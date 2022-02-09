"""
tests for the PeeWee based UserCollection class
"""

# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument


from users import UserCollection
from user_status import UserStatusCollection

from utilities_for_tests import empty_db, full_db  # pylint: disable=unused-import


def test_init_empty(empty_db):
    """
    initiliaze and empty UserCollection
    """
    uc = UserCollection()

    assert isinstance(uc, UserCollection)

    assert len(uc) == 0


def test_init_full(full_db):
    """
    initiliaze a UserCollection from a database with data
    """
    print(full_db)

    uc = UserCollection()

    assert isinstance(uc, UserCollection)

    assert len(uc) == 3


def test_search_user(full_db):
    uc = UserCollection()

    user = uc.search_user('bwinkle678')


    assert user.user_id == 'bwinkle678'
    assert user.user_name == 'bwinkle'


def test_search_user_not_there(full_db):
    uc = UserCollection()

    user = uc.search_user('xxxx')

    assert user is None


def test_delete_user(full_db):
    """
    does delete_user actually delete a user?
    """
    uc = UserCollection()

    start_len = len(uc)
    uid = 'bwinkle678'
    result = uc.delete_user(uid)

    assert result is True
    assert len(uc) == start_len - 1

    assert uc.search_user(uid) is None


def test_delete_user_not_there(full_db):
    """
    deleting an non-existant user should return False
    """
    uc = UserCollection()

    start_len = len(uc)

    uid = 'x1x2x3x4'
    result = uc.delete_user(uid)

    assert result is False
    assert len(uc) == start_len

    assert uc.search_user(uid) is None


def test_add_user_new(empty_db):
    """
    tests adding a new user
    """
    uc = UserCollection()

    status = uc.add_user('xxxxx',
                         'this@that.com',
                         'cbarker',
                         'Barker')

    assert status is True
    assert len(uc) == 1

def test_add_user_already_there(full_db):
    """
    tests adding a new user
    """
    uc = UserCollection()

    start_len = len(uc)
    status = uc.add_user('cbarker12',
                         'this@something.com',
                         'fjones',
                         'Jones',
                         )

    assert status is False
    # but did it overwrite the user?
    assert uc.search_user('cbarker12').user_name != 'fjones'
    assert start_len == len(uc)


def test_update_user(full_db):
    uc = UserCollection()

    # some test data
    user_id = 'bwinkle678'
    user_email = 'this@that.com'
    user_name = 'fbarnes'
    user_last_name = 'Barnes'

    result = uc.modify_user(user_id,
                            user_email,
                            user_name,
                            user_last_name,
                            )

    assert result is True

    user = uc.search_user(user_id)
    assert user.user_email == user_email
    assert user.user_name == user_name
    assert user.user_last_name == user_last_name

def test_update_user_not_there(full_db):

    uc = UserCollection()
    user_id = 'xxxxx'
    user_email = 'this@that.com'
    user_name = 'fbarnes'
    user_last_name = 'Barnes'
    result = uc.modify_user(user_id, user_email, user_name, user_last_name)

    assert result is False
    assert uc.search_user('xxxxx') is None


def test_delete_user_deletes_status(full_db):
    """
    when a user is delted, all the status updates associated with it should
    be deleted as well
    """
    uc = UserCollection()
    sc = UserStatusCollection()

    uid = 'cbarker12'
    sid = 'st55555'
    # Check that there's a status for this user
    assert sc.search_status(sid).user_id.user_id == uid

    success = uc.delete_user(uid)

    # Just make the sure the test is valid
    assert success

    # that user should be gone
    assert uc.search_user(uid) is None

    assert sc.search_status(sid) is None

    # two should have been removed
    assert len(sc) == 2
