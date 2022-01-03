:orphan:

.. _notes_lesson01:

################################################################
1/11/2022: Introduction to Py320: Advanced Programming in Python
################################################################


In which you are introduced to this class, your instructors, your environment and your now best friend, Python.


.. image:: /_static/python.png
    :align: center
    :width: 80%


`xkcd.com/353`_

.. _xkcd.com/353: http://xkcd.com/353

 
The goal of this lesson is get us all familiar with each other, the class, and all the tools and systems we'll need to conduct the class.
That is, at the end of this lesson  we can start the actual learning about Python :-)

Who are we?
===========

Introduction to your instructors:

Chris

Luis


Who are you?
------------

Despite the common myth of the lone programmer, most software development is a collaborative activity.  As such, we encourage students in this program to work together whenever possible.

As you will be working with your fellow students for the rest of the program, we'll take 
a couple minutes now to get to know each other.

This is a lot harder to do online, but we'll try to make use of Zoom as best we can!

So we'll go around the zoom and introduce ourselves:

Tell us a tiny bit about yourself:

* Name
* Programming background: what languages have you used?
* Why do you want to learn Python?
* What's your favorite coffee shop or bar -- or was, before the Pandemic.

* What is your gitHub handle -- if you already have one.
  If not, send it to us when you get it: ``pythonCHB@gmail.com``


Introduction to This Class
==========================

The overall class is managed by a learning management system -- Canvas.

You should have gotten a link to the instance for the class sent to you.

Is everyone "hooked up" to Canvas?

NOTE: I'm not a big Canvas fan: it's where to go to find assignments and get on the Zoom, etc, but much of our interaction will be via programming tools, like gitHub, rather than Canvas.



Class Structure
---------------

We will be using a variation of a
`"flipped classroom" <https://en.wikipedia.org/wiki/Flipped_classroom>`_
for this class.

This means that the "homework" will be reading, watching videos, coding, etc.

And class time will be spent primarily coding:

 * Still some lecture -- as little as possible
 * Lots of demos
 * Working on Coding Exercises:
   - On your own, with us to help
   - In small groups (breakout groups on Zoom)
   - Instructor led.

This means that you are expected to complete the reading (and video watching) BEFORE each class. That way, we don't have to take class time introducing the basic material and can focus on questions and applying what you've read about.

Interrupt us with questions -- please!

Luis and I will be monitoring Zoom chat -- but it's easy to miss -- so feel free to speak up!

(Some of the best learning prompted by questions)


Homework:
---------

* Homework will be reading, a handful of videos, and links to optional external materials -- videos, blog posts, etc.

* Exercises will often be started in class -- but you can finish them at home (and you will need time to do that!)

* You are adults -- it's up to you to do the homework. But if you don't code, you won't learn to code. And we can't give you a certificate if you haven't demonstrated that you've done the work.

* To submit your work, we will use gitHub Classroom:

2) git / gitHub Classroom
-------------------------

The second, and harder part is gitHub classroom.

In general, most of you seem to have got the basics down:

 - Accepting the assignment
 - Cloning the assignment repo onto your machine.
 - Adding a file to git
 - Commiting your changes
 - Pushing your changes to gitHub.

Did you all get a gitHub Classroom repo working?

(zoom poll)

For a reminder:

:ref:`github_classroom`

https://uwpce-pythoncert.github.io/ProgrammingInPython/topics/01-setting_up/github_classroom.html


We'll play around with this in this session so we can get the hang of it.


Communication
-------------

MS Teams:


We will use MS Teams to communicate -- it's a good way for us to communicate as a group, rather than more directly as individuals.

`Link to the Team <https://teams.microsoft.com/l/team/19%3aQ-nZkfCZ6FCD5xc9n_X2dB6M3l-nu0rEF27WMRlXnEQ1%40thread.tacv2/conversations?groupId=b2f3f042-43c1-4709-8f31-cffa42956a3d&tenantId=f6b6dd5b-f02f-441a-99a0-162ac5060bd2>`_


Most of you should already be members (with your uw email), but if not, I think you can go to that link and request to join.

Anything Python related is fair game.  Questions and discussion about the assignments are encouraged.

We highly encourage you to work together. You will learn at a much deeper level if you work together, and it gets you ready to collaborate with colleagues.

I will also send occasional email out to the whole class -- make sure I have the email address you want me to use. (I've got your uw email addresses now).


Office Hours
------------

We will generally will hold two "office hours" sessions on Zoom each week.

Please feel free to attend even if you do not have a specific question. It is an opportunity to work with the instructors and fellow students, and learn from each other.

What are good times for you?


gitHub Classroom
----------------

Let's get you set up with gitHub classroom so you can submit your work:

:ref:`github_classroom`


About git
---------

Now that we've done that, a few thoughts on git:

Have you got the gitHub classroom "flow" down?

Do you have any conceptual Questions?


Notes:
------

git is very flexible, and does not lose data easily. However, it is **much** harder to undo things than it is to make changes.  So you will be happier if you take some extra care to not commit changes that you don't want. Some hints:

* Always do a ``git status`` before you commit -- make sure that the stuff you are going to commit is what you want!

  - note that if you do ``git commit`` it will only commit those files listed under "staged for commit". But if you do ``git commit -a`` (-a for all) then it will commit everything modified, i.e. "Changes not staged for commit:".

Note in the status report::

    $ git status
    On branch main
    Your branch is up to date with 'origin/main'.

    Changes not staged for commit:
      (use "git add <file>..." to update what will be committed)
      (use "git checkout -- <file>..." to discard changes in working directory)

        modified:   notes_for_class/source/lesson02.rst

    ...

It even tells you want to do: use ``git add`` to stage particular files, or ``git checkout`` to revert a file back to its state as of the last commit. It doesn't mention ``git commit -a``, but that will commit everything that is "not staged for commit".

If you are careful before the commit stage, then you won't have to "roll back" changes very often.

But if you do:

https://uwpce-pythoncert.github.io/ProgrammingInPython/topics/01-setting_up/git_hints.html#backing-out-a-change

There are other nifty hints on that page, if you get stuck.

Evaluation of your work
=======================

In the previous class, the focus was on getting the basics of Python down.

 * Getting the code to do what you want it to do

You were introduced to many of the concepts of good software development practices:

 * Code style / linting
 * Unit testing / TDD
 * Error handling
 * Well thought out code structure
 * Documenting the code

In this class, we will be emphasizing these ideas. The assignments will evaluated with all this in mind. In short, your code will be expected to:

* Work correctly
* Be PEP 8 compliant
* Have complete Unit Tests (ideally 100% coverage)
* Be basically documented (i.e. docstrings on functions / classes)


Unit Testing
============

The first week is about Unit Testing and TDD. You were introduced to these concepts in the previous class, but we are now taking it up a notch. In particular:

* How to use the ``unittest`` testing framework
* Fixtures
* Mocking
* Code Coverage

You may find that much of the material in the readings / videos for this week are review -- but review is a good thing !


Unit Testing Terminology
------------------------

**Unit Testing** is a concept:

    "a software testing method by which individual units of source code are tested to determine whether they are fit for use."

Unit testing can be done in any language with any number of testing frameworks and test runners, including roll-your-own asserts in an ``if __name__ == "__main__":`` block.

A **test framework** is a collection of utilities that aid in writing unit tests.

A **test runner** is a utility that makes it easy to run unit tests, including reporting the results, etc.

**test coverage** is a measure of how much of the code under test is actually used when the suite of unit tests is run.
Note that less than 100% coverage means the tests are incomplete. But even with 100% coverage, there may be many possibilities that were never tested.

**Test Driven Development (TDD)**: is "a software development process relying on software requirements being converted to test cases before software is fully developed".
In short: write the tests before the code.
It can feel pretty awkward at first: After all, we are thinking about how to make the code work -- that's what we want to focus on. But trust me: it really does lead to cleaner, more robust code.
And if you follow TDD, 100% coverage is almost guaranteed.

These are all concepts that are independent of the tools.

Python Unit Testing Tools
-------------------------

**``unittest``** is a unit testing framework that is delivered as part of the Python standard library. It is used by cPython itself, as well as a number of major packages, e.g. Django.

**``pytest``** is both a test runner *and* a unit testing framework. It can be used to run ``unittest`` tests, as well as the simpler tests based on the pytest test framework.

**``coverage``** is a python package that helps you determine the coverage of a set of unit tests.
It can be run by itself, or along with pytest, via pytest-cov.


Unit testing for this class
---------------------------

As ``unittest`` is part of the standard library, every Python developer should be familiar with it.
So this week's exercise should be completed using the ``unittest`` framework.
For the rest of the class, you are free to use either ``unittest`` or ``pytest`` tests -- which ever you find most productive.
But in either case, we expect you to follow TDD and have comprehensive test coverage

Any thoughts / questions about Unit Testing before we jump in?


``unittest`` in practice
========================

Usually, you will have completed all the reading / videos before class. So we'd be ready to jump right in to the Exercises.

But since you all should be familiar with testing already,let's jump right in anyway!


Handy references for unittest:
------------------------------

The official docs:

https://docs.python.org/3/library/unittest.html

A cheat sheet for the asserts:

https://kapeli.com/cheat_sheets/Python_unittest_Assertions.docset/Contents/Resources/Documents/index
