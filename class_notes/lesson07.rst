:orphan:

.. _notes_lesson07:

################################
2/22/2022: Concurrency and Async
################################


A collection of notes to go over in class, to keep things organized.

**NOTES:**

I'll try to have a break every hour or so -- ping me if I forget!

Some issues that came up during the week.

Extra files in git
------------------

**BE CARFUL WHEN YOU GIT ADD**

You really don't want to put a bunch of cruft in git that you don't need -- for instance all the working files from MongoDB in mongo_files.

Avoid ``git add .`` or ``git add *``.

Add each files as you need.

If you do do ``git add . or *``, then make sure it did what you want before committing. And look at ``git status`` first to see what it will add (untracked files)


Opening a Mongo Connection with every interaction
-------------------------------------------------

One of you wrote a solution that used the context manger to open (and close) the MongoDB connection


Break Time!
===========

10min break:


Mongo Clients
-------------

MongoDB is a full multi-user database server. Even though you can start it up with a single simple command -- it's ready to work with multiple users.

Which makes it easy to have multiple clients running at once in your code:

    In [1]: import pymongo

    In [2]: client1 = pymongo.MongoClient()

    In [3]: client1.list_database_names()
    Out[3]: ['SocialNetwork', 'admin', 'config', 'local', 'social_network']

    In [4]: client2 = pymongo.MongoClient()

    In [5]: client2.list_database_names()
    Out[5]: ['SocialNetwork', 'admin', 'config', 'local', 'social_network']

    In [6]: client1.drop_database('SocialNetwork')

    In [7]: client1.list_database_names()
    Out[7]: ['admin', 'config', 'local', 'social_network']


This is pretty handy for the multiprocessing assignment!


what does join() mean?
----------------------

Both threads an processes have a ``.join()`` method

What ``join(a_thread)`` means is "wait until a_thread has terminated". Why it's not called something like "wait_until_done" is beyond me.





Break Time!
===========

10min break


