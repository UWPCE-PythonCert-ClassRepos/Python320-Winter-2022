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

The backslash is the escape charactor in string literals:

::

  'this\nthat'

Keeping track of global state
-----------------------------

This is one to be very, very careful of. Make sure that anything that is truly global state -- like what database you are working with, is managaged carefully.

Where things can get stick is where you manage the same thing (like the database name) in more than one place, e.g. menu.py, social_network.py, etc. If you use the smae name for the DB: "socal.db" then it all appears to work, but things can get very ugly if you want to use a different DB!



Break Time!
===========

10min break:



Break Time!
===========

10min break


