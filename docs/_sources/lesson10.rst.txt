:orphan:

.. _notes_lesson10:

#####################
3/15/2022: API Design
#####################


A collection of notes to go over in class, to keep things organized.

**NOTES:**

I'll try to have a break every hour or so -- ping me if I forget!

Last Class!
===========

This is the final class -- it went by fast!

Some logistics:
---------------

I am supposed to turn in your grades 7 days from today. So as usual, the final assignment (all the assignments!) is due a week from today, on Tuesday, March 22.

But please try not to turn it all in at once at the end! We need time to review your work.

What if I'm not all done?
-------------------------

In order to complete the class, you need to have completed most of all the assignments. Most of you have gotten full credit on most assignments, so you're in good shape.

But if you are pressed for time, and you are almost done with an assignment (maybe it's missing one feature, or doesn't score 10/10 on pylint, or ...) -- turn that in, and get working on the next one.

If you have made a good faith effort on all assignments, and completed most of the requirements -- you will pass.

Support for the Last Week
-------------------------

I will be out of town for the weekend, and will not be able to hold office hours.

However, I will monitor email and MS Teams, and may even be able to schedule an impromptu meeting or two. Reach out for help if you need it.


INTERNET PROGRAMMING WITH PYTHON
================================

The third and final class.

Luis will be teaching that one -- do you have any questions about it?


Backslashes in Strings
----------------------

The backslash is the escape character in string literals:

::

  'this\nthat'

So that puts a "newline" in instead of the slash and the "n"

What if you want a slash? You escape the slash:

::

  'this\\that'



A little metaprogramming:
-------------------------

I don't like repeated code -- that's the DRY principle:

    **Don't Repeat Yourself**

So when I found myself writing the same code three times to validate the input for the DataSet solution, I did a little metaprogramming:

.. code-block:: python

    restrictions = {'user_id': 30,
                    'user_name': 30,
                    'user_last_name': 100}
    vars_ = vars()
    for fieldname, limit in restrictions.items():
        value = vars_[fieldname]
        if len(value) > limit:
            logger.error(f"{fieldname}: {value} too long, not added")
            return False


Managing global configuration
-----------------------------

This is one to be very, very careful of. Make sure that anything that is truly global state -- like what database you are working with, is managed carefully.

Where things can get sticky is where you manage the same thing (like the database name) in more than one place, e.g. menu.py, social_network.py, etc.
If you use the same name for the DB: "social.db" then it all appears to work, but things can get very ugly if you want to use a different DB!


A config object
...............

A solution to this is to put all of your configuration in one place.

If there's a lot of complexity, you can have a ``config.py`` module just for that.

But in the simple case, a dict in the module where you define you database setup, etc. is just fine:

.. code-block:: python

    HERE = path(__file__).parent

    config = {'database_name': 'social.db',
              'data_dir': HERE / 'data',
              }


Then when you want to use that config:

.. code-block:: python

    from socialnetwork_model import config

    def create_dataset():
        dataset = DataSet(f'sqlite:///{config['database_name']}')

        ...

        return dataset

The nifty thing is that that dict is mutable -- you can change it from runtime, from anywhere:

.. code-block:: python

    # in your test code

    from socialnetwork_model import config

    # set up things for the tests:

    config['database_name'] = ":memory:"
    config['data_dir'] = HERE / 'test_data_dir'

    # And now your tests will all use the new values.

**NOTES:**

* Make sure that all code that uses the config does so in functions -- e.g. it does not run at module import time. In that case, if would be to late to change it.

* If you do want to change the config dict -- do so *in place* -- e.g. mutate the dict. If you make a new one, the changes will not be seen anywhere else:

This will **NOT** work!

.. code-block:: python

    from socialnetwork_model import config

    # set up things for the tests:

    config = {'database_name']: ":memory:",
              'data_dir': HERE / 'test_data_dir'
              }

Why not -- what's going on there that's different?

And you can't even change it in the original namespace.

This won't work right either:

.. code-block:: python

    import socialnetwork_model

    # set up things for the tests:
    social_network_model.config = {'database_name']: ":memory:",
                                   'data_dir': HERE / 'test_data_dir'
                                   }

That DOES change the object in the ``socialnetwork_model`` module, so code using it in that module will see the change. But any other module that imports it will not -- it already got a reference to the original dict.

As your application gets more complex, you can do things like have the config read from a file at startup, etc...


Any other questions / concerns?
-------------------------------

Any sticking points you want to go over?

Do a little code review?


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

NOTE: In JSON, white space is insignificant, so be default it's all crammed on one line.
If you want it to be readable -- pass a value in for ``indent`` to ``dump`` and ``dumps`` -- if you give a value for indent, the JSON will be nicely formatted with newlines and indentation.

That's it!


Break Time!
===========

10min break


Final Assignment: Flask
=======================


The gitHub CI:
--------------

Depending on what you accepted the assignment, flask may or may not be in the ``requirements.txt`` file. If you are having trouble with the CI failing -- you may need to add it. Here's mine::

    loguru
    peewee
    flask
    pytest


JSON and flask:
---------------

Nifty hint: Flask provides the ``jsonify`` utility:

.. code-block:: python

    from flask import jsonify

It converts what you pass in to JSON, and wraps it in a proper JSON response object.


TDD and Flask
-------------

The final assignment is to build a JSON API for your social network app.

Flask is a very simple, streamlined framework, and well documented.

But I'm going to take a bit of time now to show you how to set it up for testing, so you can do TDD right off the bat.

NOTE: We are not building a "complete" Flask application -- no need to set up everything the way it's done in the full tutorial.

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



