"""
social_network.py

An implimentation of the social network system
in one place -- abstacting out the user and status
tables
"""

# pylint: disable=too-few-public-methods)
# pylint: disable=inconsistent-return-statements
# pylint: disable=undefined-loop-variable
# pylint: disable=duplicate-code

import dataclasses as dc

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, BulkWriteError

from loguru import logger


def start_mongo():
    """
    start up a connection to MongoDB

    :returns: A pymongo client object, and a database object
    """

    # In production code, these would be read from a config file, or ...
    # these values should match what's in mongo_config_dev.yml
    client = MongoClient(host='127.0.0.1', port=27017)

    return client


# def __init__(..., status_updates=None):
#     if status_updates is None:
#         status_updates = list()

@dc.dataclass
class StatusUpdate():
    """
    dataclass to hold status update info

    Probably not really neccesary, but if there's more later
    """
    status_id: str
    status_text: str

    def to_dict(self):
        """
        Just the dataclass asdict() for a consistent interface

        And to provide customization in the future
        """
        return dc.asdict(self)

@dc.dataclass
class User():
    '''
    Contains user information
    '''
    user_id: str
    email: str
    user_name: str
    user_last_name: str = ""
    status_updates: list[StatusUpdate] = dc.field(default_factory=list)

    def to_dict(self):
        """
        Write our contents of a User to a mongo-compatible dict

        Example dict:

        {'_id': 'xxxx',
         'email': 'cbarker@this.that',
         'user_name': 'cbarker',
         'user_last_name': 'Barker',
         'status_updates': [{'status_id': 'xxxx_01',
                             'status_text': 'a new message'},
                            {'status_id': 'xxxx_02',
                             'status_text': 'A random message'}],
         }

        """
        dict_ = dc.asdict(self)

        dict_['_id'] = dict_['user_id']
        del dict_['user_id']

        # this is optional -- only if the dataclass.asdict() doesn't work.
        # dict_['status_updates'] = [sud.to_dict() for sud in self.status_updates]
        return dict_

    @classmethod
    def from_dict(cls, dict_):
        """
        Create a user from a mongo-compatible dict
        """
        dict_['user_id'] = dict_['_id']
        del dict_['_id']
        dict_['status_updates'] = [StatusUpdate(**su) for su in dict_['status_updates']]
        return cls(**dict_)

# just for demo
# class SuperUser(User):
#     def to_dict(self):
#         dict_ = super().to_dict()
#         dict_['superuser'] = True
#         return dict_



class SocialNetwork:
    """
    Class that manages the Social Network database
    """
    def __init__(self, db_name):
        """
        Initialize a SocialNetwork manager

        :param db_name: name of the Mongo database to use.

        NOTE: A MongoDB server must be running
        """
        client = start_mongo()
        self.database = client[db_name]
        self.collection = self.database['users']
        logger.info("New instance of Social Network created")

    def __len__(self):
        """
        defines the len() -- number of users in the collection
        """
        return self.collection.count_documents({})

    def add_user(self, user_id, email, user_name, user_last_name):
        '''
        Adds a new user to the collection
        '''
        new_user = User(user_id, email, user_name, user_last_name)
        try:
            self.collection.insert_one(new_user.to_dict())
#            logger.info(f"User {user_id} added to the database")
        except DuplicateKeyError:
            logger.error(f"User {user_id} already exists in the database")
            return False
        return True

    def add_users(self, users):
        '''
        Adds an iterable of new users to database

        :param users: iterable of dicts with keys:
                      user_id, email, user_name, user_last_name

        Duplicate users are ignored
        '''
        # convert to User objects
        # generator comprehension so as not to pre-calculate
        new_users = (User(**user).to_dict() for user in users)
        try:
            result = self.collection.insert_many(new_users,
                                                 ordered=False)
        except BulkWriteError as err:
            details = err.details
            for error in  details['writeErrors']:
                logger.error(f"user_id: {error['keyValue']['_id']} Failed to write")
            return details['nInserted']
        num_inserted = len(result.inserted_ids)
        logger.info(f"{len(result.inserted_ids)} Users added to the database")
        return num_inserted

    def modify_user(self, user_id, email, user_name, user_last_name):
        '''
        Modifies an existing user
        '''
        mongo_query = {"_id": user_id}
        if self.collection.count_documents(mongo_query) > 0:
            # Fixme: make sure to preserve status_updates
            new_user = User(user_id, email, user_name, user_last_name)

            new_values = {"$set":new_user.to_dict()}
            return bool(self.collection.update_one(mongo_query, new_values))
        logger.error(f"User {user_id} does not exist in the database")
        return False

    def delete_user(self, user_id):
        '''
        Deletes an existing user
        '''
        mongo_query = {"_id":user_id}
        if self.collection.count_documents(mongo_query) > 0:
            result = self.collection.delete_one(mongo_query)
            if result.deleted_count == 1:
                return True
        logger.error(f"User {user_id} does not exist in the database")
        return False

    def search_user(self, user_id):
        '''
        Searches for user data
        '''
        mongo_query = {"_id":user_id}

        user = self.collection.find_one(mongo_query)
        if user is None:
            logger.warning(f"User {user_id} not found in database")
            return None
        return User.from_dict(user)

    def add_status(self, user_id, status_id, status_text):
        '''
        Adds a new status to the user with given user_id
        '''
        # Need to check if user exists
        mongo_query = {"_id": user_id}
        user = self.collection.find_one(mongo_query)
        if user is None:
            logger.error(f"User {user_id} does not exist in the database")
            return False
        # new_user = User.from_dict(user)
        # new_user.status_updates.append(status_text)
        new_values = {'$push': {'status_updates': {'status_id': status_id,
                                                   'status_text': status_text}}}
        success = bool(self.collection.update_one(mongo_query, new_values))
        return success

    def add_statuses(self, statuses):
        '''
        Adds a iterable of dicts of status messages:

        dict keys: user_id, status_id, status_text

        '''
        num_added = 0
        for status in statuses:
            filter = {"_id": status['user_id']}
            new_values = {'$push':
                              {'status_updates':
                                  {'status_id': status['status_id'],
                                                       'status_text': status['status_text']}}
                          }
            result = self.collection.update_one(filter, update=new_values)
            num_added += result.modified_count
        return num_added



    def search_status(self, status_id):
        '''
        Searches and returns the information from an existing status
        '''
        # this finds a document with the status_id we are looking for.
        mongo_query = {"status_updates.status_id": status_id}
        result = self.collection.find_one(mongo_query)
        if result is None:
            logger.warning(f"Status {status_id} not found in database")
            return None
        # extract the status update
        for sud in result['status_updates']:
            if sud['status_id'] == status_id:
                return StatusUpdate(**sud)

    def modify_status(self, status_id, status_text):
        '''
        Modifies an existing status
        '''
        # this finds a document with the status_id we are looking for.
        mongo_query = {"status_updates.status_id": status_id}
        result = self.collection.find_one(mongo_query)
        if result is None:
            logger.warning(f"Status {status_id} not found in database")
            return False
        user = User.from_dict(result)
        # find the status update
        for sud in user.status_updates:
            if sud.status_id == status_id:
                break
        # update the text
        sud.status_text = status_text
        new_values = {"$set": user.to_dict()}
        return bool(self.collection.update_one({"_id": user.user_id},
                                               new_values))

    def delete_status(self, status_id):
        '''
        Deletes an existing status
        '''
        # this finds a document with the status_id we are looking for.
        mongo_query = {"status_updates.status_id": status_id}
        result = self.collection.find_one(mongo_query)
        if result is None:
            logger.warning(f"Status {status_id} not found in database")
            return False
        user = User.from_dict(result)
        user.status_updates = [sud for sud in user.status_updates
                               if sud.status_id != status_id]
        new_values = {"$set": user.to_dict()}
        return bool(self.collection.update_one({"_id": user.user_id},
                                               new_values))
