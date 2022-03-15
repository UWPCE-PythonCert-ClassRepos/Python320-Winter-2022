:orphan:

.. _notes_lesson10:

#####################
3/15/2022: API Design
#####################


A collection of notes to go over in class, to keep things organized.

**NOTES:**

I'll try to have a break every hour or so -- ping me if I forget!

backslashes in strings
----------------------

The backslash is the escape character in string literals:

::

  'this\nthat'

A little metaprogramming:
-------------------------

I don't like repeated code -- that's the DRY principle:

    **Don't Repeat Yourself**

So when I found myself writing the same code three times to validate the input for the DataSet solution, I did a little metaprogramming:

..code-block:: python

    restrictions = {'user_id': 30,
                    'user_name': 30,
                    'user_last_name': 100}
    vars_ = vars()
    for fieldname, limit in restrictions.items():
        value = vars_[fieldname]
        if len(value) > limit:
            logger.error(f"{fieldname}: {value} too long, not added")
            return False

Managing global state
---------------------

This is one to be very, very careful of. Make sure that anything that is truly global state -- like what database you are working with, is managaged carefully.

Where things can get stick is where you manage the same thing (like the database name) in more than one place, e.g. menu.py, social_network.py, etc. If you use the smae name for the DB: "socal.db" then it all appears to work, but things can get very ugly if you want to use a different DB!



Break Time!
===========

10min break:


JSON
====

Ultra quick JSON tutorial.

JSON (JavaScript Object Notation) is a text format for storing javascript, that look very much like a subset of Python. So you can very easily move between them. I like to use the term:

"JSON compatible Python" for Python data that can be converted to/from JSON losslessly. Essentially, You can use:

- dicts (with string keys)
- lists
- strings
- numbers (int and float)
- Bools (``True`` and ``False``)
- ``None``

``True``, ``False``, and ``None`` are spelled differently in JSON, but otherwise it's the same.

You can go to and from JSON with the built in json lib:

.. code-block:: python

    In [1]: import json

    In [4]: data = {'this': 'something',
       ...:         'that': [4,5,6,7.0],
       ...:         'a_flag': True,
       ...:         'nothing': None
       ...:         }

    In [5]: # to put json in a string:

    In [10]: js_string = json.dumps(data, indent=4)

    In [11]: print(js_string)
    {
        "this": "something",
        "that": [
            4,
            5,
            6,
            7.0
        ],
        "a_flag": true,
        "nothing": null
    }

    In [12]: # to get python objects from json

    In [13]: data2 = json.loads(js_string)

    In [14]: data2
    Out[14]: {'this': 'something', 'that': [4, 5, 6, 7.0], 'a_flag': True, 'nothing': None}

    In [15]: data == data2
    Out[15]: True


To dump / load JSON directly to a file, use ``json.dump`` and ``json.load`` and pass in an open file object.

NOTE: In JSON, whitespace is insignificant, so be default it's all crammed on one line. If you want it to be readable -- pass a value in for ``indent`` to ``dump``(s) -- if you give a value for indent, the JSON will be nicely formatted with newlines and indentation.

That's it!


Break Time!
===========

10min break


flask
=====

The gitHub CI:
--------------

Depending on what you accepted the assignment, flask may or may not be in the ``requirements.txt`` file. If you are having trouble with the CI failing -- you may need to add it. Here's mine::

    loguru
    peewee
    flask
    pytest



The final assignment is to build a JSON API for your social network app.

Flask is a very simple, streamlined framework, and well documented. But I'm going to take a bit of time now to show you how to set it up for testing, so you can do TDD right off the bat.

NOTE: WE are not building a "complete" Flask application -- no need to set up everything the way it's done in the full tutorial.

In fact, you already have the database and all that -- so you really only need a small amount of code for the web API.

The Flask Quickstart is a good place to dive in.

https://flask.palletsprojects.com/en/2.0.x/quickstart/

Flask Testing:
--------------

Flask comes out of the box with some testing utilities -- built on pytest:

https://flask.palletsprojects.com/en/2.0.x/testing/

Let's dive right in!

I'm working in the class repo:

Examples/lesson10/flask_example



