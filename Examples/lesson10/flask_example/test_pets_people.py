"""
Tests for the Pets ans People JSON API
"""

import pytest
from pets_people import app

# pylint: disable=redefined-outer-name

@pytest.fixture()
def testapp():
    """
    fixture for test application
    """
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here: maybe setting up
    # a test database?

    yield app
    # clean up / reset resources here


@pytest.fixture()
def client(testapp):
    """
    fixture for client
    """
    return testapp.test_client()


def test_root_url(client):
    """
    The root is a simple html page
    """
    response = client.get("/")
    page = response.get_data(True)  # makes it into a text string
    assert "<h1>Pets and People</h1>" in page


def test_pets(client):
    """
    /pets route should return a JSON list of pet dicts.
    """
    response = client.get("/pets")
    data = response.get_json()
    assert len(data) == 2
    # see if at least one expected pet is there:
    for pet in data:
        if pet['name'] == "Sesame":
            assert True
            break
    else:
        assert False
