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

NOTE: mongo_files is a good example!


Opening a Mongo Connection with every interaction
-------------------------------------------------

One of you wrote a solution that used the context manger to open (and close) the MongoDB connection.

Are you willing to share? Did you profile it?


Profiling / Performance
-----------------------

Anyone willing to share how your profiling went?

Did you find a bottleneck to speed up?


MongoDB with more complex documents:
------------------------------------

The real benefits of using a Database like MongoDB is that you can store documents that are complex nested data structures -- you don't need to do a lot of work to keep tables in sync with foreign keys and all that.

Did anyone write their Social Network code that way? Willing to share?

Or you can look at mine:

Solutions/assignment_05_B

If we have time:
----------------

As you've seen, if you want nice Python objects (rather than working with dicts), there's a bit of work to make them serialize / deserialize to Mongo-Compatible dicts. You can automate that more.


I wrote a system for the NOAA ADIOS Oil Database:

Which I extracted into its own (poorly tested) package:

https://github.com/PythonCHB/flexi


See the third-party packages: attrs and pydantic


Break Time!
===========

10min break:


Concurrency
===========

Is a **BIG** topic.

Please do the reading / watch the videos, and try to run through the examples.

But we don't expect you to "get" it all -- but to have an appreciation of the tools, so you can learn them for real when you need them.

Any thoughts / questions so far?


Threading and Multiprocessing
=============================

Let's take a really fast and furious look at the basics of threading and multiprocessing -- it should be enough to get you started in the assignment:


In the class repo:

`Python320-Winter-2022/Examples/lesson07/threading_module`


Break Time!
===========

10min break:


This week's assignment:
-----------------------

Shall we take a look?


A few notes:

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


What does join() mean?
----------------------

Both threads an processes have a ``.join()`` method

What ``join(a_thread)`` means is "wait until a_thread has terminated". Why it's not called something like "wait_until_done" is beyond me.





