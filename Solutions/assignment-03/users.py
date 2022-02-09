'''
UserCollection class -- to mange the users' data
'''

# pylint: disable=R0903

from loguru import logger

import peewee as pw

import socialnetwork_model as snm

# class Users():
#     '''
#     Contains user information
#     '''

#     def __init__(self, user_id, email, user_name, user_last_name):
#         self.user_id = user_id
#         self.email = email
#         self.user_name = user_name
#         self.user_last_name = user_last_name


class UserCollection():
    '''
    Contains a collection of Users objects
    '''

    def __init__(self):
        """
        Initialise a UserCollection

        Database and tables should already be intialized
        """
        logger.info("Initializing a new UserCollection")
        self.User = snm.User  # pylint: disable=invalid-name


    def __len__(self):
        """
        The total number of users
        """
        return len(self.User)

    def add_user(self, user_id, user_email, user_name, user_last_name):
        '''
        Adds a new user to the collection
        '''
        try:
            new_user = self.User.create(user_id=user_id,
                                        user_name=user_name,
                                        user_last_name=user_last_name,
                                        user_email=user_email)
            new_user.save()
            logger.debug(f"Added new user, id: {user_id}")
            return True
        except pw.IntegrityError:
            logger.debug(f"Could not add new user, id: {user_id} already there")
            return False

    def modify_user(self, user_id, email, user_name, user_last_name):
        '''
        Modifies an existing user
        '''
        user = self.search_user(user_id)
        if user is None:
            logger.debug(f"User can't be modified: {user_id} not there.")
            return False

        user.user_email = email
        user.user_name = user_name
        user.user_last_name = user_last_name
        user.save()
        logger.debug(f"User with id: {user_id} modified")

        return True

    def delete_user(self, user_id):
        '''
        Deletes an existing user
        '''
        user = self.search_user(user_id)
        if user is None:
            logger.debug(f"User with id: {user_id} not there, can't be deleted")
            return False

        user.delete_instance()
        logger.debug(f"User with id: {user_id} deleted")
        return True

    def search_user(self, user_id):
        '''
        Searches for user data
        '''
        try:
            user = self.User.get(self.User.user_id == user_id)
            return user
        except pw.DoesNotExist:
            return None
