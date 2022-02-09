from unittest import TestCase
from peewee import SqliteDatabase
from database_model import *

import directors

class TestDirectors(TestCase):
    def setUp(self):
        self.database = SqliteDatabase(':memory:')
        self.database.connect()
        self.database.pragma('foreign_keys', 1, permanent=True)
        self.database.bind([DirectorsTable])
        # Creation of the database
        self.database.create_tables([
                DirectorsTable
            ])
        self.directors_collection = directors.DirectorsCollection(self.database)

    def test_add_director(self):
        result = self.directors_collection.add_director('bdhoward', 'Bryce Dallas Howard')
        self.assertTrue(result)