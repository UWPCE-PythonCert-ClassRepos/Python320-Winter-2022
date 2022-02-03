"""
minimal UsersCollection class
"""


from loguru import logger
import peewee as pw
import models


class UserCollection():
    '''
    Contains a collection of Users objects
    '''
    def __init__(self):
        """
        Initialise a UserCollection

        Database should already be intialized
        """
        self.User = models.User  # pylint: disable=invalid-name

    def __len__(self):
        """
        The total number of users

        particularly handy for tests
        """
        return len(self.User)

    def add_user(self, user_id, user_name):
        '''
        Adds a new user to the collection
        '''
        try:
            new_user = self.User.create(user_id=user_id,
                                        user_name=user_name,
                                        )
            new_user.save()
            logger.debug(f"Added new user, id: {user_id}")
            return True
        except pw.IntegrityError:
            logger.debug(f"Could not add new user, id: {user_id} already there")
            return False

    def search_user(self, user_id):
        '''
        Searches for user data
        '''
        try:
            user = self.User.get(self.User.user_id == user_id)
            return user
        except pw.DoesNotExist:
            return None
