:orphan:

.. _notes_lesson08:

###############################
3/1/2022: Functional Techniques
###############################


A collection of notes to go over in class, to keep things organized.

**NOTES:**

I'll try to have a break every hour or so -- ping me if I forget!



One small note: ``for: else``
-----------------------------

The ``else`` option for a for loop is confusing, and rarely used. But really handy when you do need it. Example from one of my tests:

.. code-block:: python

    # need to check if at least one was correct
    # user: 'bwinkle678' should have status: 'st12455'
    user = snw.search_user('bwinkle678')
    for status_update in user.status_updates:
        if status_update.status_id == 'st12455':
            break
    else:
        assert False, "id: 'st12455' not found in user 'bwinkle678'"

As a mnemonic, I like to think of it as "else not break".


Results from the pymongo ``insert_many()`` call
-----------------------------------------------

One of the tricks of using pymongo's insert_many() is that when you pass in a whole bunch of stuff to insert, there is no single result -- they all could have passed, they all could have failed.

If anything went wrong, then it raises a ``BulkWriteError``.

But what went wrong? and what went right?

pymongo adds a ``.details`` attribute to the ``BulkWriteError``, that has a lot of information.

::
        except BulkWriteError as err:
            details = err.details
            for error in  details['writeErrors']:
                logger.error(f"user_id: {error['keyValue']['_id']} Failed to write")
            return details['nInserted']



Lets look at this in my example solution:

Examples/lesson07/ConcurrentMongo

Look in social_network.py: ``SocialNetwork.add_users()``



DataSet
=======

This week's assignment involves building a version of your Social Network code with a functional approach, using an extension to PeeWee known as DataSet:

https://docs.peewee-orm.com/en/latest/peewee/playhouse.html#dataset

ONE thing I note: in the docs:

"The aims of the DataSet module are to provide: A simplified API for working with relational data, along the lines of working with JSON. ..."

Which aligns with my impression of DataSet -- it feels a bit like working with Mongo.

Luis has more experience than I do with DAtaSet, so he's going to give you an introduction.



Break Time!
===========

10min break:


Multiprocessing Issues
======================


MultiProcessing and pickling
----------------------------

A number of you saw this error:

::

    File "/Users/chris/miniconda3/envs/py3/lib/python3.10/multiprocessing/popen_spawn_posix.py", line 47, in _launch
    reduction.dump(process_obj, fp)
    File "/Users/chris/miniconda3/envs/py3/lib/python3.10/multiprocessing/reduction.py", line 60, in dump
    ForkingPickler(file, protocol).dump(obj)

    TypeError: cannot pickle '_thread.lock' object

I got that too, when I tried to set it up this way:

.. code-block:: python

    for chunk in pd.read_csv(filename,
                             chunksize=CHUNK_SIZE,
                             iterator=True):
        print(f"CHUNK {chunk_number}")
        data = ({'user_id': row['USER_ID'],
                 'email': row['EMAIL'],
                 'user_name': row['NAME'],
                 'user_last_name': row['LASTNAME']
                 } for index, row in chunk.iterrows()
                )
        proc = multiprocessing.Process(target=snw.add_users, args=(data,))
        processes.append(proc)
        proc.start()
        chunk_number += 1
    for proc in processes:
        proc.join()

So what's wrong here?

**NOTE:**

This same code DOES work with multithreading -- why is that???

Would one of you like to share your successful solution? Or look at mine?



"multiprocessing must be in ``__name__ == "__main__"``
------------------------------------------------------

In the official docs:

https://docs.python.org/3/library/multiprocessing.html#the-spawn-and-forkserver-start-methods

And in various googlable sources, we are told that the starting of Processes must be in a if ``__name__ == "__main__":`` block.

Really? could that possibly be true?

Well, sort of.

It does NOT mean that you can't put Process creating (and starting) in functions, classes, etc -- pretty much anywhere.

The examples are very misleading:

[look at the examples in docs (under "Safe importing of main module")]

Let's see what it actually says:

"Make sure that the main module can be safely imported by a new Python interpreter without causing unintended side effects (such a starting a new process)."


Let's look at my timer code:

Examples/lesson07/ConcurrentMongo/timing.py



Windows vs \*nix
----------------

Stephen did some experiments with the same code on Windows and a Raspberry Pi running Linux.

Let's take a look.

https://docs.google.com/spreadsheets/d/17879dX9pvfTGF5Dpjsikm-MHKIs5oyakgm6J2S1K7bQ/edit#gid=1860662791


Using a Queue
-------------

A Queue makes a lot of sense for this goalL you probably don't know how large a CSV file you are going to read in -- so how big should the chunks be?

But you do know how many processers you have.

A Queue lets you create one or more "tasks" and then set up a defeined number of processes to work on them.

But is is a bit tricky to manage -- when do you put the tasks on the queue? when do you know it's done?

I did it with a ``JoinableQueue`` which is pretty slick.

Shall we look?

Jared did it with a regular Queue but had an issue -- let's check that out.


Break Time!
===========

10min break


Closures
========

Closures can be a tricky topic.

A key part of it is understanding "Scope" in Python.

There's notes and examples in Canvas, but if have a bit of time, let's go over some notes:

https://uwpce-pythoncert.github.io/ProgrammingInPython/modules/Closures.html

(These are found in the PY310 "Extra Topics")

