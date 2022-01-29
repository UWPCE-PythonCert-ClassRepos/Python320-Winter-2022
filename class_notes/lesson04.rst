:orphan:

.. _notes_lesson04:

###################
2/1/2022: Iteration
###################


A collection of notes to go over in class, to keep things organized.

**NOTES:**

I'll try to have a break every hour or so -- ping me if I forget!



Things we noticed in reviewing your work
========================================

useful logging messages
-----------------------

logging can be used to debug, but more at the application level than the code level. So you really want your messages to be meaningful to someone operating / configuring the app that may not be familiar with the code.

e.g.
``f"delete status message failed, id:{status_id} not in database"``
rather than:

"delete_status returned False"



Break Time!
===========

10min break:

Notes about PeeWee
==================

Initializing the database
-------------------------

PeeWee models require a ``Meta`` class with a database attribute:

.. code-block:: python

   class Meta:
        database = db

Which usually goes in the Base model class.

All the examples in the PeeWee docs have you initializing the database at the top of the models file. That's really not the best place for it -- ideally, your models are independent of the back-end database.

But the database does need to be defined when the model classes are defined.

Solution?

Put the model definition in its own file, and import that in your models file. That way, it can be updated independently. And also mocked for testing, etc.

Also: in real-world code, the database configuration would likely be read from a config file or the like.





Break Time!
===========

10min break


