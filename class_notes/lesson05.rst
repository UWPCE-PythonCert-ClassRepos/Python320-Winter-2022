:orphan:

.. _notes_lesson05:

##################################
2/8/2022: Consuming APIs and NoSQL
##################################


A collection of notes to go over in class, to keep things organized.

**NOTES:**

I'll try to have a break every hour or so -- ping me if I forget!

Some Issues Brought up in reviewing your code:
==============================================

pylint
------

I know that pylint can be *VERY* annoying. But we are being pedantic in this class for good reason: good code style really is important.

Critical: As annoying as it can be: *MOST* of what pylint flags really should be fixed! Trust me on this.

It's OK to silence certain linting issues that really don't apply.

But Fix any linting issues you should fix **before** ignoring any!


Getting to 100% coverage
------------------------

Getting to 100% coverage is far more important that removing lint.

If the code is not tested, you will never know when / if it breaks. And maybe not even know if it works at all!

That being said, there may be a few lines that it's OK not to have run in your tests: For instance the ``__name__ == "__main__"`` block. Solution:

``# pragma: no cover``

on a line at the beginning of a block of code will exclude it from the coverage report:

.. code-block:: python

    if __name__ == '__main__':  # pragma: no cover
        setup_logger()
        clear = True if len(sys.argv) > 1 and sys.argv[1] == "clear" else False
        socialnetwork_model.start_database('social.db', clear)
        init_collections()
        mainloop()


Connecting to the database
--------------------------

With PeeWee, there are various places where you need to have a connection to the database, so you call

``db.connect()``

But you may have noted that that raises an error if the connection is already made. Ideally, you'd be managing your connections a bit more carefully, but a work around is to call it this way:

``db.connect(reuse_if_open=True)``

Then, if it's already connected, it will simply use the existing connection, rather than raising an error.

Note on managing connections:

The PeeWee Database object provides a number of helpful context managers to manage connections:

https://docs.peewee-orm.com/en/latest/peewee/database.html#context-managers


Setting up a DB for tests, etc.
-------------------------------


We went over this last week, but I think there is still some confusion.

The big problem is that ALL the examples, including the ones we gave you, use a static approach: the database is assigned and set up at module import time. e.g.:

.. code-block:: python

    database = SqliteDatabase('database_model.db')
    database.connect()
    database.pragma('foreign_keys', 1, permanent=True)

    class BaseModel(Model):
        """
            BaseModel class
        """
        class Meta:
            """
                Meta class
            """
            database = database

    <models defined here>

    # Creation of the database
    database.create_tables([
            DirectorsTable,
            MoviesTable
        ])

    database.close()


Why is that a problem? It works!

Yes, but it works in a way that is exactly the same every time you run the code, and it's too late to customize any of that once that models module is imported.

In practice, we generally want the database to be set up in different ways under different circumstances:

- Under development -- maybe you want a fresh empty database each time
- Operationally -- you probably want a persistent database,and maybe one running on a different machine, etc.
- Tests -- tests should be able to easily create a clean, database again and again.

PeeWee does offer an solution -- it's buried a bit in the docs under testing:

https://docs.peewee-orm.com/en/latest/peewee/database.html#testing-peewee-applications

The trick is the various ``bind`` methods -- this seems simplest to me:

``Database.bind(models)``

This, well, binds the model to the database -- that is, sets things up so that actions on the model will use that particular database instance. This is what happens automatically, when you use:

.. code-block:: python

    class Meta:
        """
            Meta class
        """
        database = database

But you need to call ``database.bind()`` if you want to change it (or set it) at run time.

So you have two options:

1) Do not set up the database connection in your models code, and call ``database.bind()`` at run time before you use the models.

or

2) Do set up a default database in your models code, and then call ``database.bind()`` if you want to override the default -- e.g. in your tests.


**But wait!**

Didn't you show us a testing example two weeks ago that didn't call ``database.bind()``?

Indeed we did -- but it turns out it was not doing what we thought it would. Here's the code:

.. code-block:: python

    def setUp(self):
        self.database = SqliteDatabase(':memory:')
        self.database.connect()
        self.database.pragma('foreign_keys', 1, permanent=True)
        # Creation of the database
        self.database.create_tables([
                DirectorsTable
            ])
        self.directors_collection = directors.DirectorsCollection(self.database)

Let's walk through that and see what it's doing.


Aren't we done with PeeWee?
---------------------------

Well, yes, we are (if you're done with assignment 4 anyway), but:

This is a general software development concept -- you should keep your configuration dynamic, and defined in one place.

And you should make sure that your tests really are isolated.

This also applies to MongoDB (but it's a bit easier)


Comprehensions
--------------


Comprehensions:
...............

Build a list:

``[expr(item) for item in an_iterable]``

Build a dict:

``[key: expr(val) for key, val in an_iterable]``

(``an_iterable`` in this case must provide a pair of values)

Build a set:

``[expr(item) for item in an_iterable]``

**NOTE:** For all of these, they loop through *any iterable* -- it doesn't have to be list, or tuple, or anything in particular -- anything that can be iterated and yield appropriate values.

But ALL of these "exhaust" the iterator, and create a fully realized container (list, dict, set).

If it's big -- it could be memory intensive.

Generator Comprehensions
........................

However -- there's a solution!

A Generator Comprehension is just like a list comprehension, except that rather than immediately creating a list, it creates an iterator. The actual iteration isn't performed until it's iterated over.

.. note:: The original term for these was "Generator Expression", because they are an expression that creates a generator. But I don't use that term, because it loses the connection with the other comprehensions -- after all, it is syntactically more related to comprehensions than generator functions (the other way to make a generator). But you will see "Generator Expression" all over the internet -- it's the same thing.

Rule of thumb: If you are writing comprehension simply to immediately loop through the result -- use a Generator Comprehension.

How does one write a Generator Comprehension? Exactly like a List Comprehension, but with parentheses, rather than square brackets:

List Comprehension:

``[expr(item) for item in an_iterable]``

Generator Comprehension:

``(expr(item) for item in an_iterable)``

That's it!

A really nifty thing is that if you are putting it in parentheses already, then you don't even need another set.

Example from this assignment:

Using a comprehension to transform a iterable of objects and produce a tuple.

``status_list = tuple([(str(x.user_id), x.status_text) for x in result])``

This code works just fine, and does the job. But let's look at what it's doing:

This is a list comprehension:

``[(str(x.user_id), x.status_text) for x in result]``

It iterates through ``result`` and turns the ``user_id`` attribute to string (It's a User object before that). Then it puts the results in a list. Then the:

``tuple( .... )`` takes the list and turns it into a tuple.

But what does the ``tuple()`` constructor take as input?

.. code-block:: ipython

    In [1]: tuple?
    Init signature: tuple(iterable=(), /)
    Docstring:
    Built-in immutable sequence.

    If no argument is given, the constructor returns an empty tuple.
    If iterable is specified the tuple is initialized from iterable's items.

So it takes an iterable, and iterates through its items, and makes a tuple out of them. So is a list an iterable? Yes -- so you can pass a list to it and it will work as expected.

But do you need a list? No -- in fact you can use any iterable -- and hey! a Generator Comprehension is an iterable! The cool thing is all we need to do is remove the square brackets, and it works the same, but more efficiently.

``status_list = tuple((str(x.user_id), x.status_text) for x in result)``

That's it! no intermediate list created.

The moral of the story is that you want to avoid "realizing" an iterable until you need to.

In fact -- see the above code -- why a tuple? is that required? or will any iterable do? If so, then:

``result`` is already an iterable -- we need to transform it a bit, but we may not need to create an actual sequence, so you could do:

``status_msgs = ((str(x.user_id), x.status_text) for x in result)``

And you'd get an iterator that an be passed on, and the result won't be generated until it's actually needed.


Code Review?
============

Is anyone unsatisfied with their solution to using interables in assignment 4 that would like a code review?




Break Time! (if we haven't already)
===================================

10min break:


A few Topic to get ready for this weeks assignment
==================================================


``dataclasses`` and the glory of ``**kwargs``
---------------------------------------------

As pymongo works directly with python dicts, rather than objects, we need some ways to make it easy to move between the two.

``**kwargs`` is a very handy way to pass a dict of arguments into a function (or class constructor)

``dataclasses`` are a nifty fairly recent addition to the python standard library

I don't have anything prepared for this -- so let's dive in!



Break Time!
===========

10min break

Working with MongoDB
====================

NOTE: I updated the Assignment Repo last night -- it should have a bit more info in the README, and the CI should be set up properly.

Five of you were proactive and had already accepted the assignment. I recommend you delete your assignment repo and re-accept.

Sorry about that -- there's no way for me to push changes once it's been accepted.



Starting up MongoDB
-------------------

MongoDB is a little different than SQLlite that we've been working with. It is designed to be completely separate server process. This means it can be run on a different machine, and in fact anywhere on the internet.

But it's also dead simple to run locally on your laptop. There's a lot to configure but you can get very far for simple use with all the defaults.

Anyway -- before you can run your Python application that uses MongoDB -- you need a running instance.

Mongo Configuration:
....................

In the assignment repo is a simple configuration file for MongoDB:

.. code-block:: yaml

    # mongo_config_dev.yaml

    # this is set up to be run from the main dir in the repo
    # to start:

    # mongod -f mongo_config_dev.yml
    # On Windows you may need the .exe:
    # mongod.exe -f mongo_config_dev.yml


    net:
      bindIp: 127.0.0.1  # Enter 0.0.0.0,:: to bind to all IPv4 and IPv6 addresses or, alternatively, use the net.bindIpAll setting.
      port: 27017  # this is the mongo default

    systemLog:
      destination: file
      path: "./mongo_files/mongod.log"
      logAppend: false

    storage:
       dbPath: "./mongo_files"
       journal:
         enabled: true

This is mostly defaults, but a few notes:

Whereas SQLlite stored everything in a single file, Mongo needs a bunch of files, and they need to go somewhere. in this case, they will go in the ``mongo_files`` dir. (on my computer the default is a system dir I can't write to).

The other thing to note is the port number: The way to have multiple network services on the same computer is that each one gets a unique port number. 27017 is the default for MongoDB -- but it's better to specify it. (which means you should specify it in your code, too!)

NOTE: don't change this configuration -- the CI is expecting it to be there!

Starting MongoDB
----------------

The command is:

``mongod -f mongo_config_dev.yml``

Which means: "Start the mongo daemon, and use this file to get configuration"

You will want to run this in the same dir as the project (so it can find the mongo_files dir). You will need to do that in a separate terminal, as it will keep running.

Once that's running, you can run your Python application, tests, etc.


Using Mongo in your code:
-------------------------

Similar to with PeeWee, **it's a really good idea** to have the database start up code in one place, in a function you can call from various locations.

Let's take a look at a complete example. It can be found in the class repo at:

``Examples/lesson05/pymongo_example``

Do a ``git pull`` !








