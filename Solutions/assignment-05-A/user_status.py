'''
Classes for status information for the
social network project
'''
from loguru import logger
from pymongo.errors import DuplicateKeyError
logger.info("TEST MESSAGE FROM STATUS")

class UserStatusCollection():
    '''
    Contains a collection of status objects
    '''
    def __init__(self, database):
        '''
        Initializes the database
        '''
        self.database = database
        self.status_collection = database['user_status']
        self.users_collection = database['users']
        logger.info("New status collection instance created")

    def __len__(self):
        """
        defines the len() -- number of users in the collection
        """
        return self.status_collection.count_documents({})

    def add_status(self, user_id, status_id, status_text):
        '''
        Adds a new status to the database
        '''
        # Need to check if user_id exists
        mongo_query = {"_id":user_id}
        if self.users_collection.count_documents(mongo_query) > 0:
            new_status = {
                "_id":status_id,
                "user_id":user_id,
                "status_text":status_text
            }
            try:
                self.status_collection.insert_one(new_status)
                logger.info(f"Status {status_id} added to the database")
            except DuplicateKeyError:
                logger.error(f"Status {status_id} already exists in the database")
                return False
            return True
        logger.error(f"User {user_id} is not in the database, so you cannot add a status for them")
        return False

    def modify_status(self, status_id, user_id, status_text):
        '''
        Modifies an existing status
        '''
        mongo_query = {"_id":status_id}
        if self.status_collection.count_documents(mongo_query) > 0:
            new_status_data = {
                "_id":status_id,
                "user_id":user_id,
                "status_text":status_text
            }
            new_values = {"$set":new_status_data}
            return self.status_collection.update_one(mongo_query, new_values)
        logger.error(f"Status {status_id} does not exist in the database")
        return False

    def delete_status(self, status_id):
        '''
        Deletes an existing status
        '''
        mongo_query = {"_id":status_id}
        if self.status_collection.count_documents(mongo_query) > 0:
            return self.status_collection.delete_one(mongo_query)
        logger.error(f"Status ID {status_id} does not exist in the database")
        return False

    def search_status(self, status_id):
        '''
        Searches and returns the information from an existing status
        '''
        mongo_query = {"_id":status_id}
        if self.status_collection.count_documents(mongo_query) > 0:
            return self.status_collection.find_one(mongo_query)
        logger.warning(f"Status {status_id} not found in database")
        return None
