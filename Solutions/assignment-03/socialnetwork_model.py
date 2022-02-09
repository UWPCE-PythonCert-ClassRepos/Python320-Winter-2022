"""
The model definitions for the social app
"""

from pathlib import Path
import peewee as pw

HERE = Path(__file__).parent

DEFAULT_DB_NAME = "social.db"


def get_database(filename=None, clear=False):
    """
    setup and return a database to use for the models

    :param filename: name of DB file, or ":memory:" for in=memory temp DB

    :param clear=False: Whether to clear out the old db and return an
                        empty one.
    """

    if filename == ":memory:":
        database = pw.SqliteDatabase(':memory:',
                               pragmas={'foreign_keys': 1}
                               )

    else:
        if filename is None:
            filename = DEFAULT_DB_NAME
        if clear:   # pragma: no cover (not used in tests)
            Path(filename).unlink(missing_ok=True)
        database = pw.SqliteDatabase(HERE / filename,
                               # pragmas={'foreign_keys': 1}
                               )
    return database


def start_database(filename='social.db', clear=False):
    """
    initialize an empty databse
    """
    models = [User, UserStatus]
    database = get_database(filename, clear)
    database.bind(models,
            bind_refs=False,
            bind_backrefs=False)
    database.connect()
    database.create_tables(models)

    return database


# pylint: disable=too-few-public-methods
class BaseModel(pw.Model):
    """
    base model for all tables
    """
    # pylint: disable=missing-class-docstring
    class Meta:
        database = get_database()


class User(BaseModel):
    """
    Model for the users in the socialnetwork
    """
    user_id = pw.CharField(primary_key=True, max_length=30)
    user_name = pw.CharField(max_length=30)
    user_last_name = pw.CharField(max_length=100)
    user_email = pw.CharField()


class UserStatus(BaseModel):
    """
    Model for the status messages
    """
    status_id = pw.CharField(primary_key=True, max_length=30)
    user_id = pw.ForeignKeyField(model=User,
                                 field='user_id',
                                 backref='status_messages',
                                 on_delete='CASCADE',
                                 )
    status_text = pw.TextField()
