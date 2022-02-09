"""
tests for the PeeWee based UserStatusCollection class
"""

# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument

from user_status import UserStatusCollection

from utilities_for_tests import empty_db, full_db # pylint: disable=unused-import


def test_init_empty(empty_db):
    """
    initiliaze and empty UserStatusCollection

    NOTE: really a test of the fixture
    """
    usc = UserStatusCollection()

    assert isinstance(usc, UserStatusCollection)

    assert len(usc) == 0


def test_init_full(full_db):
    """
    initiliaze a UserStatusCollection from a database with data

    NOTE: really a test of the fixture
    """
    usc = UserStatusCollection()

    assert isinstance(usc, UserStatusCollection)

    assert len(usc) == 4


def test_search_status(full_db):
    usc = UserStatusCollection()

    sid = 'st12455'
    status = usc.search_status(sid)


    assert status.status_id == sid
    # user_id is the foreign key so we get a User object back
    assert status.user_id.user_id == 'bwinkle678'


def test_search_status_not_there(full_db):
    usc = UserStatusCollection()

    status = usc.search_status('xxxx')

    assert status is None


def test_delete_status(full_db):
    """
    does delete_status actually delete a status?
    """
    usc = UserStatusCollection()

    start_len = len(usc)
    sid = 'st55555'
    result = usc.delete_status(sid)

    assert result is True
    assert len(usc) == start_len - 1

    assert usc.search_status(sid) is None


def test_delete_status_not_there(full_db):
    """
    deleting an non-existant status should return False
    """
    usc = UserStatusCollection()

    start_len = len(usc)

    sid = 'x1x2x3x4'
    result = usc.delete_status(sid)

    assert result is False
    assert len(usc) == start_len

    assert usc.search_status(sid) is None


def test_add_status_new(empty_db):
    """
    tests adding a new status

    NOTE: for this test, there is no user corresponding to the sstatus
    """
    usc = UserStatusCollection()

    sid = 'xxxxxx'
    result = usc.add_status(sid, 'yyyyy', 'just some text')

    assert result is True
    assert usc.search_status(sid).status_id == sid

    assert len(usc) == 1

def test_add_status_already_there(full_db):
    """
    tests adding a new status
    """
    usc = UserStatusCollection()

    start_len = len(usc)
    result = usc.add_status(user_id='new_user_id',
                            status_id='st12355',
                            status_text='A simple message from user: fjones34'
                            )

    assert result is False
    # but did it overwrite the status?
    assert usc.search_status('st12355').user_id != 'new_user_id'
    assert start_len == len(usc)


def test_modify_status_not_there(full_db):
    usc = UserStatusCollection()
    stat_id = '1111111'
    user_id = '12345'
    status_text = 'new status text'
    result = usc.modify_status(stat_id, user_id, status_text)
    assert result is False


def test_modify_status_there(full_db):
    usc = UserStatusCollection()
    stat_id = 'st12355'
    user_id = 'cbarker12'
    status_text = 'new status text'

    print(usc.search_status(stat_id))
    result = usc.modify_status(stat_id, user_id, status_text)
    assert result is True

    # check if the modify "took"
    status = usc.search_status(stat_id)
    assert status.status_id == stat_id
    assert status.status_text == 'new status text'
