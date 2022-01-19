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

NOTE: It's a known pain to use MS Teams with your UW account if you also use it with another account, e.g. at work. I think the easiest solution is to have two different computers, or two user accounts on one computer.

Has anyone found a solution to managing two MS Teams accounts?



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

**NOTE:** We kind of threw you into the deep end with this assignment -- lots to learn all at once!

If you were unable to complete it -- do not despair! You will have a chance to re-submit.

In fact, the next assignments build on this one -- so you *will* need to finish it!

Tonight will be a bit of a catch-up -- we probably won't be able to get to much of the new material - but the you're building skill that will carry through.


The GitHub CI
-------------

I talked about this last week -- but it's worth repeating -- gitHub telling you your PR "failed" is scary, but all it means is that the linting or coverage failed, NOT that you failed the assignment!

Let's see what that looks like.

Linting Errors
--------------

We are being particularly Pedantic about pylint for this class -- this is to get you used to good habits. So we expect Zero errors flagged by pylint.

But, as it says in PEP 8:

    "A Foolish Consistency is the Hobgoblin of Little Minds"

So pylint gives you ways to ignore certain Issues. See the pylint docs for the details, but in short:

You can ignore certain errors for the whole project by putting them in a ``.pylintrc`` file in the dir with your code. This is only a good idea for things that really apply to the whole project -- avoid it.


Disabling a particular message in one file:

Put:

# pylint: disable=XXXXX

Near the top of the file.

Where XXXXXX is the error code (e.g. C0103) or error name:

::

    # pylint: disable=C0103 # to allow short names in the tests
    # pylint: disable=invalid-name

Do the same thing -- the error code is easier to add, the name is easier to read :-)

https://pylint.pycqa.org/en/latest/faq.html#is-there-a-way-to-disable-a-message-for-a-particular-module-only

Disabling an error on just one line: Sometimes there's one line where you need to break the rules. In that case, you can put the same comment on that very line:

::

    uc = self.empty_user_collection() # pylint: disable=unused-variable

https://pylint.pycqa.org/en/latest/faq.html#how-to-disable-a-particular-message

As a rule, don't disable errors until you are "done" with the code, and are sure you're not going to fix them. They really are helpful while code is still under development.

https://pylint.pycqa.org/en/latest/faq.html#how-to-disable-a-particular-message

Let's look at some examples from my code:


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

The special assertXXXXX methods
...............................

There was some chat on MS Teams about the ``unitest assertXXX`` methods.

Here's a little secret:

All most of the special assert methods do is wrap a regular assert, and provide a nice error message if it fails.

But if you use ``pytest`` -- pytest can provide that helpful message anyway!

Why!?!?  -- ``unitest`` was ported from the JAVA ``jUnit`` library. At the time, ``jUnit`` was maybe the only well accepted, well used unit testing framework out there. So porting it made some sense.

But "Python is not Java" -- Python is highly dynamic and introspectable -- so test runners can be written (like pytest) that don't need help providing helpful error messages.

So feel free to just use a plain old assert.

I particularly find funny: ``assertTrue`` -- really? we are supposed to write::

    self.assertTrue(something)

instead of just plain::

    assert something

Really ?!?!

Also:

The is no way that you'd have all teh special asserts you need! and some of them may not even do what you thing they will. For example::

  assertTrue(something)

Doesn't check if ``something is True``, it checks if it's "truthy". With bare asserts, you can make the precise assert you want. If you want Truthy::

  assert something

If you want the actual ``True`` singleton::

  assert something is True

Done.


Break Time!
===========

10min break:


Unit testing hints
==================

Unit testing, and TDD is pretty hard to wrap your head around -- it seems pretty backwards at first. So I've written up a list of hints for how I go about it here:

:ref:`testing_hints`

I'll now take you through my solution to Assigment01, demonstrating many of those hints.


I'll also try to use the debugger a bit -- as an intro.


On to Chris' code ....


Break Time!
===========

10min break


Logging and Debugging
=====================

Debugging:
----------

If there's time, maybe we can debug some of your code: anyone have a sticky bug they'd like us to look at?

Logging:
--------

We may not have much time left -- but let's take a look at next week's assignment, and give logaru a quick try:

python3 -m pip install loguru

The docs:

https://github.com/Delgan/loguru

