"""
Simple Example of a pymongo application

with a single collection and a simple model
"""


from dataclasses import dataclass
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


def start_mongo():
    """
    start up a connection to MongoDB

    :returns: A pymongo client object, and a database object
    """

    # In production code, these would be read from a config file, or ...
    # these values should match what's in mongo_config_dev.yml
    client = MongoClient(host='127.0.0.1', port=27017)

    return client

# Now the actual code for your project

# you don't need to use dataclasses, but it saves some boilerplate!
@dataclass
class Director:
    """
    Dataclass to hold director information
    """
    director_id: str
    full_name: str


class DirectorCollection():
    """
    class to hold movie directors, and information about them

    At this point, just a name, but it could be all sorts of other stuff
    """
    def __init__(self, mongodb):
        """
        Initialize a DirectorsCollection with the provided database
        """
        self.mongodb = mongodb  # just in case we need it
        self.dircol = mongodb.directors

    def __len__(self):
        """ number of Directors in the collection """
        return self.dircol.count_documents({})

    def add_director(self, director_id, full_name):
        """ Add a new director to the Collection """
        new_director = {'_id': director_id,
                        'full_name': full_name,
                        }
        try:
            self.dircol.insert_one(new_director)
        except DuplicateKeyError:
            return False
        return True

    def search_director(self, director_id):
        '''
        Searches for a director in the collection
        '''
        direct = self.dircol.find_one({"_id": director_id})
        if direct is None:
            return None
        return Director(direct['_id'], direct['full_name'])
