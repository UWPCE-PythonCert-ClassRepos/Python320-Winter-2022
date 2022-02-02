"""
some trial code, before putting it in the real code

User to test and experiment with PeeWee
"""

import peewee as pw

from data_for_tests import SAMPLE_USERS_DATA

database = pw.SqliteDatabase(':memory:')


class BaseModel(pw.Model):
    """
    base model for all tables
    """
    class Meta:
        database = database


class User(BaseModel):
    user_id = pw.CharField(primary_key=True, max_length=30)
    user_name = pw.CharField(max_length=30)
    user_last_name = pw.CharField(max_length=100)
    user_email = pw.CharField()


class UserStatus(BaseModel):
    status_id = pw.CharField(primary_key=True, max_length=30)
    user_id = pw.ForeignKeyField(model=User,
                                 field='user_id',
                                 backref='status_messages',
                                 on_delete='CASCADE',
                                 )  # on_delete, on_update, deferrable
    status_text = pw.TextField()

MODELS = [User, UserStatus]

#database.bind(MODELS, bind_refs=False, bind_backrefs=False)
database.connect()
database.create_tables(MODELS)


for user in SAMPLE_USERS_DATA:
    new_user = User.create(**user)
    print(new_user)
    new_user.save()
    print("after adding:", len(User))

# for user in
#     new_user = self.User(user_id=user_id,
#                          user_name=user_name,
#                          user_last_name= user_last_name,
#                          user_email=email)
#     print(new_user)
#     new_user.save()
#     print("after adding:", len(self.User))

