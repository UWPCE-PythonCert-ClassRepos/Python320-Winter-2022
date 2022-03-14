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



Break Time!
===========

10min break


