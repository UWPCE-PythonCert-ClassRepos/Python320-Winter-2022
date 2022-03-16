"""
The model definitions for the social network app

not much here, as DataSet does all the work.
"""

from pathlib import Path

from playhouse.dataset import DataSet

HERE = Path(__file__).parent

DEFAULT_DB_NAME = HERE / "social.db"


def get_dataset(filename=None, clear=False):
    """
    setup and return a database to use for the models

    :param filename: name of DB file, or ":memory:" for in=memory temp DB

    :param clear=False: Whether to clear out the old db and return an
                        empty one.

    :returns: PeeWee Dataset object
    """

    if filename == ":memory:":
        dataset = DataSet('sqlite:///:memory:')
    else:  # pragma: no cover (not used in tests)
        if filename is None:
            filename = DEFAULT_DB_NAME
        if clear:
            Path(filename).unlink(missing_ok=True)
        dataset = DataSet(f'sqlite:///{filename}')

    # set up the user's table
    users = dataset['users']
    # insert a dummy record to get the table set up
    users.insert(user_id='temp',
                 user_name='ausername',
                 user_last_name='Example',
                 user_email='example@nothing.com')
    # create index to make user_id unique
    users.create_index(['user_id'], unique=True)
    # Delete the dummy record afterwards.
    users.delete(user_id='temp')

    statuses = dataset['statuses']
    # insert a dummy record to get the table set up
    statuses.insert(status_id='temp',
                    user_id='xxx',
                    status_text='an example status message')
    # create index to make status_id unique
    statuses.create_index(['status_id'], unique=True)
    # Delete the dummy record afterwards.
    statuses.delete(status_id='temp')

    return dataset
