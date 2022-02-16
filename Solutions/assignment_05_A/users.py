'''
Classes for user information for the
social network project
'''
from loguru import logger
from pymongo.errors import DuplicateKeyError
# pylint: disable=R0903

class UserCollection():
    '''
    Contains a collection of Users objects
    '''
    def __init__(self, database):
        self.database = database
        self.users_collection = database['users']
        self.status_collection = database['user_status']
        logger.info("New instance of UserCollection created")

    def __len__(self):
        """
        defines the len() -- number of users in the collection
        """
        return self.users_collection.count_documents({})

    def add_user(self, user_id, email, user_name, user_last_name):
        '''
        Adds a new user to the collection
        '''
        new_user = {
            "_id":user_id,
            "email":email,
            "user_name":user_name,
            "user_last_name": user_last_name
        }
        try:
            self.users_collection.insert_one(new_user)
            logger.info(f"User {user_id} added to the database")
        except DuplicateKeyError:
            logger.error(f"User {user_id} already exists in the database")
            return False
        return True

    def modify_user(self, user_id, email, user_name, user_last_name):
        '''
        Modifies an existing user
        '''
        mongo_query = {"_id":user_id}
        if self.users_collection.count_documents(mongo_query) > 0:
            new_user_data = {
                "_id":user_id,
                "email":email,
                "user_name":user_name,
                "user_last_name": user_last_name
            }
            new_values = {"$set":new_user_data}
            return bool(self.users_collection.update_one(mongo_query, new_values))
        logger.error(f"User {user_id} does not exist in the database")
        return False

    def delete_user(self, user_id):
        '''
        Deletes an existing user
        '''
        # create a session:
        client = self.database.client
        with client.start_session() as session:
            with session.start_transaction():
                mongo_query = {"_id": user_id}
                if self.users_collection.count_documents(mongo_query) > 0:
                    # Need to delete all status updates associated to the user
                    mongo_query_status = {"user_id": user_id}
                    self.status_collection.delete_many(mongo_query_status)
                    # Now delete user
                    result = self.users_collection.delete_one(mongo_query)
                    if result.deleted_count == 1:
                        return True
        logger.error(f"User {user_id} does not exist in the database")
        return False

    def search_user(self, user_id):
        '''
        Searches for user data
        '''
        mongo_query = {"_id":user_id}

        user = self.users_collection.find_one(mongo_query)
        if user is None:
            logger.warning(f"User {user_id} not found in database")
        return user
