:orphan:

.. _notes_lesson04:

###################
2/1/2022: Iteration
###################



A collection of notes to go over in class, to keep things organized.

**NOTES:**

As always -- I'll try to have a break every hour or so -- ping me if I forget!

Assignment03
============

This week's assignment was challenging!

There was a lot to learn and figure out. A number of you (including me!) struggled a bit with getting even the first bit of code to run: e.g. adding a new user to the User table.

Some notes about that:

The goal of this class is not for you to make a Social Media application.

It's not even for you to learn to use PeeWee.

The goal of this class is for you to:

*learn to code in Python*.

A big part of that is learning how to use a new library, with the basic tutorials and documentation available.

So while it may have been frustrating to feel like you were flailing without getting anything done, you were, in fact, learning to read docs, debug, and generally how to learn a new library to solve a new problem.

That being said: I could have provided more guidance as to how to get started on this one -- I'll try to do better with the rest of the class.

A few notes on the development process:
---------------------------------------

One of the key things, particularly when learning a new library or system is to use **incremental development**.

First get the tiniest bit of code working, (maybe starting from example code), then add to it bit by bit. That way, when something stops working, you know exactly what new code broke it.

Ideally, you would use TDD to do this. But sometimes getting things working enough to even write tests can be a challenge. But you can still use a similar process.

* Write a tiny little program that does just a little bit.
* Once it's working, copy and paste the code into your real code.
* Run your "real" code.
* Later, rinse, and repeat until you are done.

Example from this assignment:

* First make just the User Model -- in its simplest form, without constraints, etc.

* Make sure you can add users, etc with that model

* Then try adding the UserStatus model, in it's simplest form.

* get it working

* then set up the ForeignKeyField

* get that working

* then start adding constraints

* ...


Here's my "trail.py" file that I used to experiment before putting everything together:

``/Examples/lesson04/trial.py`` in the class repo.


Luis' Demo of PeeWee
====================

For all of you that may still be confused, Luis will demo building a PeeWee app:


Take away, Luis!



Break Time!
===========

10min break:


A few additional thoughts on PeeWee
===================================


Initializing the database
-------------------------

PeeWee models require a ``Meta`` class with a database attribute:

.. code-block:: python

   class Meta:
        database = db

Which usually goes in the Base model class.

All the examples in the PeeWee docs have you initializing the database at the top of the models file. That's a easy way to do it for small demos, but not ideal for a full application, and especially not for tests.


Also: in real-world code, the database configuration would likely be read from a config file or the like.

**Solution?**

Put your database creation code in a function:

.. code-block:: python

    def get_database(filename=None, clear=False):
        """
        setup and return a database to use for the models

        :param filename: name of DB file, or ":memory:" for in=memory temp DB

        :param clear=False: Whether to clear out the old db and return an
                            empty one.
        """

        if filename == ":memory:":
            db = pw.SqliteDatabase(':memory:',
                                    pragmas={'foreign_keys': 1}
                                   )

        else:
            if filename is None:
                filename = DEFAULT_DB_NAME
            if clear:
                Path(filename).unlink(missing_ok=True)
            db = pw.SqliteDatabase(HERE / filename,
                                   pragmas={'foreign_keys': 1}
                                   )
        return db

This one can create an in-memory database, or a file based one, and either delete or not the previous data.

You base model can still use the defaults:


.. code-block:: python

    class BaseModel(pw.Model):
        """
        base model for all tables
        """
        class Meta:
            database = get_database()


Testing the database functionality:
-----------------------------------

When you are doing unit tests, you really don't want to use the production database!

Which means that you need to configure the database differently in tests that on your main code.

The above function makes that pretty easy.

But there is a complication:

When you import your models file, that database gets hooked up by the Meta class:

.. code-block:: python

    class BaseModel(pw.Model):
        """
        base model for all tables
        """
        class Meta:
            database = get_database()

But with tests, you may (really should!) use a clean database for each of your tests. So how do we do that?

The PeeWee docs have a section on this:

https://docs.peewee-orm.com/en/latest/peewee/database.html#testing-peewee-applications

Turns out that you don't have to statically define the database that the models use in your code. You can "Bind" the database to the models, at run time, over and over again ....

PeeWee actually has multiple ways of doing this, including context managers. But I used the simplest:

``database.Bind()``

That way, I could write startup code that would start the database in different ways, and fixtures that could start it up in different ways for the tests.

Here's my function to start up the database:

.. code-block:: python

    def start_database(filename='social.db', clear=False):
        """
        initialize an empty databse
        """
        models = [User, UserStatus]
        db = get_database(filename, clear)
        db.bind(models,
                bind_refs=False,
                bind_backrefs=False)
        db.connect()
        db.create_tables(models)

        return db

So this gets the database, binds it to the models, connects to the database, and then creates the tables.

By having this in a function, I can re-run it whenever a clean database is required.

My menu.py starts up this way:

.. code-block:: python

    if __name__ == '__main__':  # pragma: no cover
        setup_logger()
        clear = True if len(sys.argv) > 1 and sys.argv[1] == "clear" else False
        socialnetwork_model.start_database('social.db', clear)
        init_collections()
        mainloop()

In fact, once I'm doing this -- I don't need to set up the database in the Meta class at all :-)

And once that's all in place, I created some fixtures for the tests:

(in a separate file, so all the test files could use it)

.. code-block:: python

    def cleanup_database(db):
        """
        close and cleanup the database
        """
        db.drop_tables(MODELS)
        db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        db.close()


    def make_empty_db():
        '''
        make an empty database

        Here so it can be used in both pytest and unittest fixtures
        '''
        start_database(":memory:", clear=True)

    @pytest.fixture
    def empty_db():
        """
        initialize and empty database
        """
        # setup
        db = start_database()
        yield

        # teardown
        cleanup_database(db)


    @pytest.fixture
    def full_db():
        """
        initialize a database with some data in it
        """
        # setup
        # setup
        db = start_database(":memory:", clear=True)

        # populate the User table
        for user in SAMPLE_USERS_DATA:
            new_user = User.create(**user)
            new_user.save()

        # populate the Status table
        for stat in SAMPLE_STATUS_DATA:
            new_stat = UserStatus.create(**stat)
            new_stat.save()

        yield

        # teardown
        cleanup_database(db)


Foreign Keys
------------

See notes in PeeWee docs about Foreign Keys:

https://docs.peewee-orm.com/en/latest/peewee/relationships.html#relationships-and-joins

"In SQLite, foreign keys are not enabled by default. ... To avoid problems, I recommend that you enable foreign-key constraints when using SQLite, "

::

    # Ensure foreign-key constraints are enforced.
    db = SqliteDatabase('my_app.db',
                        pragmas={'foreign_keys': 1})

Note that you can pass the pragmas in at database startup.

When I added that, a handful of my tests failed -- that's what the tests are for!



max_length vs constraints, vs...
--------------------------------

It would seem obvious that using max_length on a char field would, well, restrict its length.

It turns out that PeeWee passes max_length on to the underlying database.

But SQLlite doesn't support restricted length fields, so nothing happens if you pass in a long string.

Constraints, on the other hand, are enforced by PeeWee itself.

The other option is to check or truncate the length in your own code.


Things I noticed in reviewing your work
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

10min break


Iterators and Iterables
=======================

The next assignment is to extend your social media app with a some iterators. For the most part, the hard part of that is the PeeWee stuff, but I'd like to take a bit of time to go over the Iterator Protocol.


Iterator Protocol
=================

**Iteration** is going through all the objects in a container.

"An iterator is an object that enables a programmer to traverse a container"

So an **Iterator** is a thing that lets you get all the items in a container one by one.

**Wait!** don't we just use ``for`` loops for that?

Indeed we do, and that's the way to go for the common case, but directly working with iterators can provide more flexibility. And for loops are are using the Iterator Protocol under the hood.

An **Iterable** is an object that can provide an iterator.

One key point is that there is no one "type" of Iterator or Iterable -- an Iterator is not a particular class.

Rather, in Python, an Iterator or Iterable is anything that conforms to a particular protocol -- known as the **Iterator Protocol**.

That protocol has two sides: the one users of a iterator see, and the one that you need to make to implement an iterator.

Using Iterators
---------------

How to get an Iterator
......................

The first thing you need to do to iterate over a iterable is to abtian its iterator.

The built in function ``iter()`` will retrieve an iterator from an iterable:

.. code-block:: ipython

    # a list is a common "iterable"

    In [1]: l = [1, 2, 3, 4]

    In [2]: it = iter(l)

    In [3]: it
    Out[3]: <list_iterator at 0x103e46800>

You can see that the object returned is not the list -- but a special "iterator" object.


How to use an Iterator
......................

Once you obtained an iterator, it's easy to use, when you want the next item from the iterator, call ``next()``

.. code-block:: ipython

    In [4]: next(it)
    Out[4]: 1

    In [5]: next(it)
    Out[5]: 2

What happens when there are no more items?

.. code-block:: ipython

    In [6]: next(it)
    Out[6]: 3

    In [7]: next(it)
    Out[7]: 4

    In [8]: next(it)
    ---------------------------------------------------------------------------
    StopIteration                             Traceback (most recent call last)
    <ipython-input-8-bc1ab118995a> in <module>
    ----> 1 next(it)

    StopIteration:

When an iterator is "exhausted", it raises a special type of Exception: ``StopIteration``.

So you can emulate a ``for`` loop with a ``while`` loop like so:

The for loop:

.. code-block:: ipython

    In [10]: for item in l:
        ...:     print(item)
        ...:
    1
    2
    3
    4

Built with ``while`` and the Iterator Protocol

.. code-block:: ipython

    In [14]: while True:
        ...:     try:
        ...:         item = next(it)
        ...:     except StopIteration:
        ...:         break
        ...:     print(item)
        ...:
    1
    2
    3
    4

So what ``for`` is doing is really just convenient shorthand for the above.


Iterators preserve state
------------------------

One of the key things about iterators is that they "preserve state" -- that is, they remember where they are in the iteration order. So you can get a few items out, then later on, a few more -- just keep calling next().

And once one has been "exhausted", it's done:

.. code-block:: ipython

    In [15]: it = iter(l)

    In [16]: next(it)
    Out[16]: 1

    In [17]: next(it)
    Out[17]: 2

    In [18]: next(it)
    Out[18]: 3

    In [19]: next(it)
    Out[19]: 4

    In [20]: next(it)
    ---------------------------------------------------------------------------
    StopIteration                             Traceback (most recent call last)
    <ipython-input-20-bc1ab118995a> in <module>
    ----> 1 next(it)

    StopIteration:

    In [21]: next(it)
    ---------------------------------------------------------------------------
    StopIteration                             Traceback (most recent call last)
    <ipython-input-21-bc1ab118995a> in <module>
    ----> 1 next(it)

    StopIteration:

``StopIteration`` will keep getting raised forever.

What if I want to iterate through the same thing again?

Call ``iter`` again:

.. code-block:: ipython

    In [23]: it = iter(l)

    In [24]: next(it)
    Out[24]: 1

In fact, each time you call ``iter(obj)``, you get a new, independent iterator, each keeping its own state:

.. code-block:: ipython

    In [25]: it1 = iter(l)

    In [26]: it2 = iter(l)

    In [27]: next(it1)
    Out[27]: 1

    In [28]: next(it1)
    Out[28]: 2

    In [29]: next(it2)
    Out[29]: 1

It's not common to do that, but it can be done :-)

Getting the iterator from an iterator?
--------------------------------------

Often you don't know whether what you want to iterate through is an iterable or an iterator:

.. code-block:: ipython

    In [30]: it = iter(l)

    In [31]: next(it)
    Out[31]: 1

    In [32]: next(it)
    Out[32]: 2

    # I want to loop through the rest -- it's already an iterator
    In [33]: for i in it:
        ...:     print(i)
        ...:
    3
    4

Python has a nifty trick -- you don't have to explicitly call iter() in most cases, e.g. for loops:

.. code-block:: python

    for i in iter(a_list):
        ...

Wouldn't that be ugly?

Python implicitly calls iter() when it needs an iterable. But we DO want to be able to loop through an iterator as well. So the Iterator Protocol specifies that iterables should return themselves when iter() is called on them:

.. code-block:: python

    In [35]: it = iter(l)

    In [36]: it
    Out[36]: <list_iterator at 0x103e94a00>

    In [37]: it2 = iter(it)

    In [38]: it2
    Out[38]: <list_iterator at 0x103e94a00>

    In [39]: it is it2
    Out[39]: True

So calling iter() on an existing on iterator is a no-op. Seems a bit odd, but it's handy, as you can then chain iterators easily.

The definitions:
................

**Iterator**
  An object that returns items when passed to ``next()``. And raises StopIteration when there are no items left.

**Iterable**
  An object that returns an iterator when passed to ``iter()``

So all iterators are ALSO iterables!

**Note:** Iterators to not need to terminate -- some can be infinite!

Making a custom Iterator or Iterable
------------------------------------

The other half of the iterator protocol is the dunders used to make custom iterators:

**iter()**

When ``iter()`` is called on an object, its ``__iter__`` method is called. This method should return an iterator.

**next()**

When ``next()`` is called on an object, its ``__next__`` method is called. This method should return the next item.

Sp a class is an **Iterable** if it has a ``__iter__`` method that returns an iterator

A class is a **Iterator** if it has a ``__next__`` method that returns items and raise StopIteration when done, and has an ``__iter__`` method that returns itself.

So we can make a custom Iterator by defining a class with an ``__iter__`` method and a __next__method.

Here's how to make a simple one like the built in ``range()``

.. code-block:: python

    class class_range:
        def __init__(self, start, stop, step=1):
            self.current = start
            self.stop = stop
            self.step = step

        def __iter__(self):
            return self

        def __next__(self):
            if self.current >= self.stop:
                raise StopIteration
            else:
                current = self.current
                self.current += self.step
                return current

And in use:

.. code-block:: ipython

    In [16]: for i in class_range(0, 10, 2):
        ...:     print(i)
        ...:
    0
    2
    4
    6
    8


Generators
==========

See above: an Iterator is not a type -- it is any object that conforms to the protocol. Generators are a particularly nifty way to make a custom iterator. It's a larger topic, but this is the very short version:

A generator function is a function that has a the ``yield`` keyword in it:

.. code-block:: python

    def genfun(something):

        do_some_stuff

        yield something

        do_something_else

        yield something_else

Calling a generator function, returns a *generator* object. A *generator* is a Iterator, So when the generator function is called, the code inside it runs until it hits a yield statement. Then it waits until next() is called on it, when it "yields" a value.

When the end of the function is reached, ``StopIteration`` is raised.

.. code-block:: python

    In [47]: def genfun():
        ...:     yield "yes"
        ...:     yield "no"
        ...:     yield "maybe"
        ...:

    In [48]: gf = genfun()

    In [49]: next(gf)
    Out[49]: 'yes'

    In [50]: next(gf)
    Out[50]: 'no'

    In [51]: next(gf)
    Out[51]: 'maybe'

    In [52]: next(gf)
    ---------------------------------------------------------------------------
    StopIteration                             Traceback (most recent call last)
    <ipython-input-52-c9712ab0ce22> in <module>
    ----> 1 next(gf)

    StopIteration:

This makes it very easy to make "lazy" iterators -- iterators that "generate" values on the fly.

Here's a simple version of the built in ``range`` function:

.. code-block:: python

    def gen_range(start, stop, step=1):
        i = start
        while i < stop:
            yield i
            i += step

And in use:

.. code-block:: ipython

    In [14]: for j in gen_range(0, 10, 2):
        ...:     print(j)
        ...:
    0
    2
    4
    6
    8

Isn't that a **lot** easier? The ability to pause and keep state makes for a lot less bookkeeping code!

.. code-block:: python

    class genclass_range:
        def __init__(self, start, stop, step=1):
            self.start = start
            self.stop = stop
            self.step = step

        def __iter__(self):
            i = self.start
            while i < self.stop:
                yield i
                i += self.step

And in use:

.. code-block:: ipython

    In [21]: for k in genclass_range(0, 10, 2):
        ...:     print(k)
        ...:
    0
    2
    4
    6
    8

In this case, the class is adding nothing, but it could if you had a class that was an iterable, and also had other functionality. In fact, the built in range() is also a Sequence:

.. code-block:: ipython

    In [37]: r = range(10)

    In [38]: r[3]
    Out[38]: 3

Also -- look carefully -- are they exactly the same? what would happen if you stopped it in the middle and restarted it?


Here's what happens with the built in ``range()``:

.. code-block:: ipython

    In [27]: r = range(10)

    In [28]: for i in r:
        ...:     print(i)
        ...:     if i > 3:
        ...:         break
        ...:
    0
    1
    2
    3
    4

    In [29]: for i in r:
        ...:     print(i)
        ...:
    0
    1
    2
    3
    4
    5
    6
    7
    8
    9

So it "resets" when you loop through again (remember, for calls ``iter()`` on the object)

What will the three implementations above do?

Try it!

What's the difference?

Exercise for the reader:

How would you make one that was rentrant


Coroutines
----------

Generators are kind of like functions, except they can be stopped in the middle, and maintain their state. It turns out this kind of "pausable" function is known as a "coroutine", and can be useful for things other than classic iterators.

You will see the term "coroutine" in discussions of asynchronous programming. Actually, technically, a generator is a "semicoroutine", but close enough :-)


One example of a use of genrators that isn't iteration is ``pytest`` fixtures -- they take advantage of generator functions to make the setup and tear down easy:

.. code-block:: python

    @pytest.fixture
    def empty_db():
        """
        Initialize an empty database
        """
        # setup
        db = start_database()
        yield db

        # teardown
        cleanup_database(db)

pytest calls next() on the fixture, and it yields (returns) something (in this case an instance of the database), and then waits to call next again until after the test is done.

This is really handy, as you don't need to store any of the variables anywhere to use them in the tear down part.


