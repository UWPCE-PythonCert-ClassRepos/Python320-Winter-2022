"""
tests for the menu module

These tests mock the input() function so they can run

Note: they do not test actual functionality implimented by main,
as that is tested in test_main.py

These tests use pytest fixtures, and don't use unittest
"""

# pylint: disable=unused-argument
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=assignment-from-no-return
# pylint: disable=duplicate-code


from pathlib import Path
from unittest import mock
from types import SimpleNamespace
import pytest

import main
import menu
import test_main


HERE = Path(__file__).parent

EXAMPLE_USER = SimpleNamespace(user_id="cb1234",
                               email="cbarker@some_company.com",
                               user_name="cbarker",
                               user_last_name="Barker",
                               )

EXAMPLE_STATUS = SimpleNamespace(status_id='c1234_00001',
                                 user_id='cb1234',
                                 status_text='All tests are complete',
                                 )


@pytest.fixture
def init_collections():
    print("initializing the collections")
    menu.init_collections()

    yield None

    print("deleting the collections")
    del menu.user_collection
    del menu.status_collection


@pytest.fixture
def full_collections():
    menu.init_collections()
    print("initializing the collections with data")

    for user in test_main.SAMPLE_USERS_DATA:
        menu.user_collection.add_user(**user)

    main.init_status_collection()
    for stat in test_main.SAMPLE_STATUS_DATA:
        menu.status_collection.add_status(**stat)

    yield None

    print("deleting the collections")
    del menu.user_collection
    del menu.status_collection


class MultiInputMock:  #pylint: disable=too-few-public-methods
    """
    A mocked input() function that can be called multiple times
    and return different results each time
    """

    def __init__(self, inputs):
        """
        :param inputs: list of input responses
        """
        self.inputs = inputs
        self.current_input = -1

    def __call__(self, prompt):
        print("mocked_input called with:", prompt)
        self.current_input += 1
        try:
            return self.inputs[self.current_input]
        except IndexError:  # pragma: no cover
            # this shouldn't happen if used correctly
            raise ValueError("input called too many times")  #pylint: disable=W0707


inputs = [str(HERE / "accounts.csv")]


@mock.patch('builtins.input', wraps=MultiInputMock(
    [str(HERE / "accounts.csv"),
     ]))
def test_load_users(mocked_input, init_collections):
    # just checking that it ran without error
    result = menu.load_users()
    assert result is None


@mock.patch('builtins.input', wraps=MultiInputMock(
    [str(HERE / "status_updates.csv"),
     ]))
def test_load_status_updates(mocked_input, init_collections):
    # just checking that it ran without error
    result = menu.load_status_updates()
    assert result is None


@mock.patch('builtins.input', wraps=MultiInputMock(
    [EXAMPLE_USER.user_id,
     EXAMPLE_USER.email,
     EXAMPLE_USER.user_name,
     EXAMPLE_USER.user_last_name,
     ]))
def test_add_user(mocked_input, init_collections):
    # just checking that it ran without error
    result = menu.add_user()
    assert result is None


@mock.patch('builtins.input', wraps=MultiInputMock(
    ['bwinkle678',
     EXAMPLE_USER.email,
     EXAMPLE_USER.user_name,
     EXAMPLE_USER.user_last_name,
     ]))
def test_add_user_there(mocked_input, full_collections):
    # just checking that it ran without error
    result = menu.add_user()
    assert result is None


@mock.patch('builtins.input', wraps=MultiInputMock(
    ['fjones34',
     'jones@new_company.com',
     'fjones',
     'Jones',
     ]))
def test_update_user(mocked_input, full_collections):
    # just checking that it ran without error
    result = menu.update_user()
    assert result is None

@mock.patch('builtins.input', wraps=MultiInputMock(
    ['fjonesxxx',
     'jones@new_company.com',
     'fjones',
     'Jones',
     ]))
def test_update_user_not_there(mocked_input, full_collections):
    # just checking that it ran without error
    result = menu.update_user()
    assert result is None



@mock.patch('builtins.input', wraps=MultiInputMock(
    ['fjones34',
     ]))
def test_search_user(mocked_input, full_collections):
    # just checking that it ran without error
    result = menu.search_user()
    assert result is None

@mock.patch('builtins.input', wraps=MultiInputMock(
    ['xxxxxxx',
     ]))
def test_search_user_not_there(mocked_input, full_collections):
    # just checking that it ran without error
    result = menu.search_user()
    assert result is None


@mock.patch('builtins.input', wraps=MultiInputMock(
    ['fjones34',
     ]))
def test_delete_user(mocked_input, full_collections):
    # just checking that it ran without error
    result = menu.delete_user()
    assert result is None

@mock.patch('builtins.input', wraps=MultiInputMock(
    ['xxxxxxx',
     ]))
def test_delete_user_not_there(mocked_input, full_collections):
    # just checking that it ran without error
    result = menu.delete_user()
    assert result is None


@mock.patch('builtins.input', wraps=MultiInputMock(
    [str(HERE / 'temp_accounts_data.csv'),
     ]))
def test_save_users(mocked_input, full_collections):
    # just checking that it ran without error
    menu.save_users()
    print(vars(mocked_input))
    assert (HERE / 'temp_accounts_data.csv').is_file()


@mock.patch('builtins.input', wraps=MultiInputMock(
    [EXAMPLE_STATUS.user_id,
     EXAMPLE_STATUS.status_id,
     EXAMPLE_STATUS.status_text,
     ]))
def test_add_status(mocked_input, init_collections):
    # just checking that it ran without error
    result = menu.add_status()
    assert result is None


@mock.patch('builtins.input', wraps=MultiInputMock(
    ['cbarker12',
     'st55555',
     'A second simple message from user: cbarker12'
     ]))
def test_add_status_already_there(mocked_input, full_collections):
    # just checking that it ran without error
    result = menu.add_status()
    assert result is None


@mock.patch('builtins.input', wraps=MultiInputMock(
    ['fjones34',
     'st12355',
     "darn -- coverage 90% more tests to run",
     ]))
def test_update_status(mocked_input, full_collections):
    # just checking that it ran without error
    result = menu.update_status()
    assert result is None


@mock.patch('builtins.input', wraps=MultiInputMock(
    ["xxxxxx",
     EXAMPLE_STATUS.status_id,
     "darn -- coverage 90% more tests to run",
     ]))
def test_update_status_not_there(mocked_input, full_collections):
    # just checking that it ran without error
    result = menu.update_status()
    assert result is None


@mock.patch('builtins.input', wraps=MultiInputMock(
    ['st12455',
     ]))
def test_search_status(mocked_input, full_collections):
    # just checking that it ran without error
    result = menu.search_status()
    assert result is None

@mock.patch('builtins.input', wraps=MultiInputMock(
    ['xxxxxxx',
     ]))
def test_search_status_not_there(mocked_input, full_collections):
    # just checking that it ran without error
    result = menu.search_status()
    assert result is None


@mock.patch('builtins.input', wraps=MultiInputMock(
    ['st12455',
     ]))
def test_delete_status(mocked_input, full_collections):
    # just checking that it ran without error
    result = menu.delete_status()
    assert result is None

@mock.patch('builtins.input', wraps=MultiInputMock(
    ['xxxxxxx',
     ]))
def test_delete_status_not_there(mocked_input, full_collections):
    # just checking that it ran without error
    result = menu.delete_status()
    assert result is None

@mock.patch('builtins.input', wraps=MultiInputMock(
    [str(HERE / 'temp_status_data.csv'),
     ]))
def test_save_status(mocked_input, full_collections):
    # just checking that it ran without error
    result = menu.save_status()
    assert result is None
    assert (HERE / 'temp_status_data.csv').is_file()


@mock.patch('builtins.input', wraps=MultiInputMock(
    ['a',
     str(HERE / 'accounts.csv'),
     'Q',
     ]))
def test_mainloop(mock_input, init_collections):
    with pytest.raises(SystemExit):
        menu.mainloop()


@mock.patch('builtins.input', wraps=MultiInputMock(
    ['zed',
     'Q',
     ]))
def test_mainloop_bad_option(mock_input, init_collections):
    with pytest.raises(SystemExit):
        menu.mainloop()
