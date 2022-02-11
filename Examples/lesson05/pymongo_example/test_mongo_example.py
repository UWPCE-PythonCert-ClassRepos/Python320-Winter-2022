"""
A few tests for the mongo_example code

These use pytet and pytest fixtures

You can do similar things with unittest fixtures (setUp() methods)
"""
# pylint: disable=redefined-outer-name
# pylint: disable=missing-function-docstring

import pytest

from mongo_example import start_mongo, DirectorCollection


@pytest.fixture
def empty_db():
    """
    provides an empty database to use for testing

    NOTE: you can have multiple databases in one mongo instance
          So we can use one for testing that's separte from the
          operational one
    """
    client = start_mongo()
    client.drop_database('test_database')

    # now create it again and passes it to the test
    yield client.test_database

    # probably not required as the object will get cleaned
    # when deleted, but still a good practice
    client.close()



@pytest.fixture
def full_db():
    """
    provides an empty database to use for testing

    NOTE: you can have multiple databases in one mongo instance
          So we can use one for testing that's separte from the
          operational one
    """
    client = start_mongo()
    client.drop_database('test_database')

    # now create it again
    database = client.test_database
    coll = database.directors

    # and populate it
    coll.insert_one({'_id': "scor123", 'full_name': "Martin Scorsese"})
    coll.insert_one({'_id': "spie345", 'full_name': "Steven Spielberg"})
    coll.insert_one({'_id': "kubr678", 'full_name': "Stanley Kubrick"})

    # now pass it to the test
    yield database

    # probably not required as the object will get cleaned
    # when deleted, but still a good practice
    client.close()


def test_init_director_collection_empty(empty_db):
    """
    really a test of the fixture
    """
    dircol = DirectorCollection(empty_db)

    assert len(dircol) == 0


def test_init_director_collection_full(full_db):
    """
    really a test of the fixture
    """
    dircol = DirectorCollection(full_db)

    assert len(dircol) == 3


def test_search_director(full_db):
    dircol = DirectorCollection(full_db)

    did = 'spie345'
    director = dircol.search_director(director_id=did)

    print(director)

    assert director.director_id == did
    assert director.full_name == "Steven Spielberg"


def test_search_director_not_there(full_db):
    dircol = DirectorCollection(full_db)

    did = 'xxxxxx'
    director = dircol.search_director(director_id=did)

    assert director is None


def test_add_director(empty_db):
    dircol = DirectorCollection(empty_db)

    start_len = len(dircol)
    result = dircol.add_director("bark123", "Christopher Barker")
    assert result is True

    assert len(dircol) == start_len + 1


def test_add_director_already_there(full_db):
    dircol = DirectorCollection(full_db)

    start_len = len(dircol)

    result = dircol.add_director("spie345", "Frederick Spielberg")

    assert result is False

    assert len(dircol) == start_len
