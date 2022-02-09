'''
classes to manage the user status messages
'''
# pylint: disable=R0903


from loguru import logger

import peewee as pw

import socialnetwork_model as snm


class UserStatusCollection():
    '''
    Collection of UserStatus messages
    '''

    def __init__(self):
        """
        Initialise a UserCollection

        Database and tables should already be intialized
        """
        logger.info("Initializing a new UserStatusCollection")
        self.UserStatus = snm.UserStatus  # pylint: disable=invalid-name

    def __len__(self):
        """
        The total number of users
        """
        return len(self.UserStatus)

    def add_status(self, status_id, user_id, status_text):
        '''
        Adds a new user to the collection
        '''
        try:
            new_status = self.UserStatus.create(user_id=user_id,
                                                status_id=status_id,
                                                status_text=status_text,
                                                )
            new_status.save()
            logger.debug(f"Added new status, id: {status_id}")
            return True
        except pw.IntegrityError:
            logger.debug(f"Could not add new status, id: {status_id} already there")
            return False

    def modify_status(self, status_id, user_id, status_text):
        '''
        Modifies a status message

        The new user_id and status_text are assigned to the existing message
        '''
        status = self.search_status(status_id)
        if status is None:
            logger.debug(f"status message can't be modified: {status_id} not there.")
            return False

        status.user_id = user_id
        status.status_text = status_text
        status.save()
        logger.debug(f"status message with id: {status_id} modified")

        return True

    def delete_status(self, status_id):
        '''
        Deletes an existing status
        '''
        status = self.search_status(status_id)
        if status is None:
            logger.debug(f"status with id: {status_id} not there, can't be deleted")
            return False

        status.delete_instance()
        logger.debug(f"status with id: {status_id} deleted")
        return True

    def search_status(self, status_id):
        '''
        Searches for status data
        '''
        try:
            status = self.UserStatus.get(self.UserStatus.status_id == status_id)
            return status
        except pw.DoesNotExist:
            return None
