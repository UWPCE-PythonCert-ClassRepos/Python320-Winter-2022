"""
This is where you set up the database and the models you need

In a larger app, you might split out the models to different
files, but in this case, it's OK to put it all here
"""

# pylint: disable=invalid-name

from pathlib import Path
import peewee as pw

HERE = Path(__file__).parent

DEFAULT_DB_NAME = "the_database.db"


def get_models():
    """
    returns a list of the models you have defined

    This is in a function so that the models can be defined
    afeter this function

    You need to add the models you want to use to this list
    """
    return [User]


def start_database(filename=None, clear=False):
    """
    Setup and return a database to use for the models

    If called with no arguments, it will set up a SQLlite database
    using the DEFAULT_DB_NAME, in the dir this file is in.

    :param filename: name of DB file, or ":memory:" for in=memory temp DB

    :param clear=False: Whether to clear out the old db and return an
                        empty one.

    """
    # Create the Database
    if filename == ":memory:":
        db = pw.SqliteDatabase(':memory:',
                               pragmas={'foreign_keys': 1}
                               )
    else:
        if filename is None:
            filename = DEFAULT_DB_NAME
        if clear:
            Path(filename).unlink(missing_ok=True)
        db = pw.SqliteDatabase(HERE / filename,
                               pragmas={'foreign_keys': 1}
                               )

    # Initialize the database
    # If the file exists and is already populated, then
    # this will initialize with the existing data

    models = get_models()

    # this dynamically binds the database to the models
    db.bind(models,
            bind_refs=False,
            bind_backrefs=False)
    db.connect()
    db.create_tables(models)

    # The initialized database is returned for use elsewhere.
    return db


class BaseModel(pw.Model):
    """
    base model for all tables
    """
    # You don't need to put the databae here,
    # As it's going to get dynamically bound

    # Keeping the base class so there is a place
    # for future shared data.
    # class Meta:
    #     database = get_database()


class User(BaseModel):
    """
    table with user information
    """
    # note that with SQLlite, max_length is not enforced
    user_id = pw.CharField(primary_key=True, max_length=30)
    user_name = pw.CharField(max_length=30)
