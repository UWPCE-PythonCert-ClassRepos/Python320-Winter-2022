:orphan:

.. _notes_lesson02:

################################
1/18/2022: Logging and Debugging
################################


A collection of notes to go over in class, to keep things organized.

==========

I'll try to have a break every hour or so -- ping me if I forget!

Communication:
--------------

So we have WAY too many ways to communicate, so I'd like to narrow it down a bit.

Mailing List
............

The class mailing list (this I set up at the last minute -- new feature that UW provides).

``python320a_wi22@uw.edu``

You should all be receiving mail from this list, and be able to send notes to it as well.


You can see info about the list, and archives here:

http://mailman11.u.washington.edu/mailman/listinfo/python320a_wi22

(that should be in the footer of emails) -- you will probably need to be logged in to your UW account to see it.

I'd like to use this primarily as a way to make announcements for all of you. But feel free to post questions / comments of general interest, like "when are the office hours?"

MS Teams
........

MS Teams has been working pretty well -- some great discussion going, and I see classmates helping each other out -- that's the goal, keep it up!

Would it be helpful to add a channel for each assignment?


gitHub Classroom
................

gitHub classroom is the primary way to submit your assignments and get your code reviewed. When you post a link to a PR in Canvas to submit your assignment, we will find that and get to it as soon as we can.

But we can also use a PR to review code in progress if you are stuck.

The trick is us noticing the PR and question: there are a LOT of repos to keep an eye on! SO you'll need to ping us one way or another to ask us to take a look. MS Teams is a fine way to do that:

Another great option it to tag us in a PR message, i.e. ::

  @pythonCHB, @ldconejo, Could you take a look please?

Then we'll get an email with the comment, and know to look for it.

Canvas
......

Canvas messaging is my lest favorite option -- it's not integrated with anything else I do, and tends to encourage less group discussion (why I like MS Teams).




Issues that come up with the homework
=====================================

Each week, I will start class talking about issues the came up when reviewing your work -- sticking points, etc, that seem to be common among the class.


Naming things is hard!
----------------------

It's very tempting to be careless about what you name things. But it can make your code massively more readable if you take some time to give things meaningful (but short) names.

And make sure not to use deceptive names.

.. code-block:: python

        new_user = add_user(user_id, email, user_name, user_last_name, user_collection)

When I read that code, I assume that ``new_user`` is some sort of object that represents a user. But ``add_user`` returns ``True`` or ``False`` -- so it's not a user at all. Maybe:

.. code-block:: python

        success = add_user(user_id, email, user_name, user_last_name, user_collection)


``unittest``:
-------------

The ``setUp()`` method:
.......................

Remember that the code in the ``setUp`` method is a "fixture" -- it gets run *before every individual test*. So if you have, e.g.:

.. code-block:: python

    class TestMain(unittest.TestCase):
        def setUp(self):
            self.user_collection = main.init_user_collection()

Then ``self.user_collection`` will *always* be empty at the start of every test. Indeed -- that's the whole point!

Note: see above, maybe that should be:

.. code-block:: python

    class TestMain(unittest.TestCase):
        def setUp(self):
            self.empty_user_collection = main.init_user_collection()

That way, in another test, you probably wouldn't make this mistake:

.. code-block:: python

    def test_save_users(self):
        su = main.save_users('accounts_saved.csv', self.empty_user_collection)
        ...



Break Time!
===========

10min break:


Unit testing hints
==================

Unit testing, and TDD is pretty hard to wrap your head around -- it seems pretty backwards at first. So I've written up a list of hints for how I go about it here:

:ref:`testing_hints`

I'll now take you through my solution to Assigment01, demonstarting many of those hints.



On to Chris' code ....


Break Time!
===========

10min break


