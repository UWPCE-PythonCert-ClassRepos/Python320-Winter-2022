"""

An example of dataclasses -- can we add a decorator?

"""
import dataclasses as dc



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


