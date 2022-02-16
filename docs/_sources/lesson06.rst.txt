:orphan:

.. _notes_lesson06:

####################################
2/15/2022: Profiling and Performance
####################################


A collection of notes to go over in class, to keep things organized.

**NOTES:**

I'll try to have a break every hour or so -- ping me if I forget!


pylint: Duplicate Code
----------------------

Now THIS is an annoying one. PyLint gives an error for duplicate code:

::

    ************* Module users
    users.py:1:0: R0801: Similar lines in 2 files
    ==user_status:[4:13]
    ==users:[4:13]
    import dataclasses
    from dataclasses import dataclass
    from typing import Optional, Dict

    from loguru import logger
    from pymongo.errors import DuplicateKeyError
    from pymongo.results import DeleteResult

    from mongo_collection import MongoCollection (duplicate-code)

This is particularly annoying, as having the same import block in multiple files is NOT an error, or code that can reasonable be de-duplicated.

Another place you may have duplicate code is tests.

In my solution, I was able to add:

::

  # pylint: disable=duplicate-code

In the files with the duplicate code, and the error sent away. But that doesn't always work.

It turns out this is a long-standing (2014!) issue in pylint:

https://github.com/PyCQA/pylint/issues/214

The solution is to disable it in a ``.pylintrc`` file:

::

    [BASIC]
        disable=
            duplicate-code

**Caution!** In many case, the duplicate-code check is a good one! So don't turn it off until you've linted your code with it on.

Packages
--------

Big topic -- but it's pretty key.

This should have been covered in the course 1 -- but as a reminder, let's take a look:

https://uwpce-pythoncert.github.io/ProgrammingInPython/modules/Packaging.html#packages-and-packaging


Context Managers
----------------

Let's talk about context managers!

There are some notes in the Course 1 materials under Extra Topics:

https://uwpce-pythoncert.github.io/ProgrammingInPython/modules/ContextManagers.html

Luis' Solution used a context manager -- let's take a look at that:

.. code-block:: python

    class MongoDBConnection():
        '''MongoDB Connection'''

        def __init__(self, host='127.0.0.1', port=27017):
            """ be sure to use the ip address not name for local windows"""
            self.host = host
            self.port = port
            self.connection = None

        def __enter__(self):
            self.connection = MongoClient(self.host, self.port)
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.connection.close()


Example Code that's getting a bit confused:

https://github.com/uw-continuum/python-320-assignment-05-busbykt


Break Time!
===========

10min break:

Mongo Issues
============

Transactions ?
--------------

Quoting the MongoDB docs:

    In MongoDB, an operation on a single document is atomic. Because you can use embedded documents and arrays to capture relationships between data in a single document structure instead of normalizing across multiple documents and collections, this single-document atomicity obviates the need for multi-document transactions for many practical use cases.

However, there are some cases where you want to operate on multiple collections as a single action.

In recent versions, MongoDB does provide a transaction option:

https://pymongo.readthedocs.io/en/stable/api/pymongo/client_session.html#transactions

If you did build your system with two collections -- one for users, and one for status updates -- then a transaction might make sense. Let's give that a try:

Luis' solution:

(not published yet)

Let's take a look.

Using Mongo in a native way
---------------------------

The way this assignment was set up, it's very natureal to use two collections, just like you did with PeeWee.

But then you needed to manually keep them in sync -- e.g. remove status messages when you removed a user

Is there another way? let's take a look!


Break Time!
===========

10min break

Profiling and Performance
=========================

Performance Approaches:
-----------------------

This week has a lot of disparate material in it.

And some of it is pretty advanced (getting your compiler set up for Cython, etc.)

So: Do read it -- Do try to do some of it, but don't worry too much if you can't figure it all out.

But hopefully you'll remember the ideas later on in your Python careers, and you can learn it for real then.


What you really should be able to do at this stage:
---------------------------------------------------

- Basic Timing of code: both whole programs and little bits.

- Basic Profiling -- where are the bottlenecks?

- An understanding of what data structures to use where.

So: for this week, once you've got everything working, do some timing, do some profiling, figure how how to make the bottlenecks faster, and report what you've found.


About performance and profiling:
--------------------------------

Here's some of my notes on the topic -- for an overview:

https://uwpce-pythoncert.github.io/ProgrammingInPython/modules/Profiling.html


A context manager timer:
------------------------

Since we just talked about context managers -- let's do this little exercise and make a handy timer:


https://uwpce-pythoncert.github.io/ProgrammingInPython/exercises/context-managers-exercise.html#timing-context-manager





