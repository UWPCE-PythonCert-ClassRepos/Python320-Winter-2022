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

NOTE: I'm not a big Canvas fan: it's where to go to find assignemnts and get on the Zoom, etc, but much of our interaction will be via programming tools, like gitHub, rather than Canvas.

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

Subhiksha will be monitoring Zoom chat

(Some of the best learning prompted by questions)


Homework:
---------

* Homework will be reading, a handful of videos, and links to optional external materials -- videos, blog posts, etc.

* Exercises will be started in class -- but you can finish them at home (and you will need time to do that!)

* You are adults -- it's up to you to do the homework. But if you don't code, you won't learn to code. And we can't give you a certificate if you haven't demonstrated that you've done the work.

* To submit your work, we will use gitHub Classroom:

2) git / gitHub Classroom
-------------------------

The second, and harder part is gitHub classroom.

Sorry about the false start -- it was buggy!

But we've settled on a workflow, and hopefully it will suport that workflow consitently.

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

It's new to me, too!


Communication
-------------

MS Teams:

We have set up an MS Team for this class:

[Insert link here:]

Most of you are already members (with your uw email), but if not, I think you can go to that link and request to join.


Anything Python related is fair game.  Questions and discussion about the assignments are encouraged.

We highly encourage you to work together. You will learn at a much deeper level if you work together, and it gets you ready to collaborate with colleagues.

I will also send occasional email out to the whole class -- make sure I have the email address you want me to use. (I've got your uw email addresses now).


Office Hours
------------

We will generally will hold "office hours" on Zoom for a couple hours each weekend.  We will try to have one session on Saturday, and one on Sunday.

Please feel free to attend even if you do not have a specific question. It is an opportunity to work with the instructors and fellow students, and learn from each other.

What are good times for you?


gitHub Classroom
----------------

Let's get you set up with gitHub classroom so you can submit your work:

:ref:`github_classroom`


About git
---------

Now that we've done that, a few thoughts on git:

Do you have any conceptual Questions?


Notes:
------

git is very flexible, and does not lose data easily. However, it is **much** harder to undo things than it is to make changes.  So you will be happier if you take some extra care to not commit changes that you don't want. Some hints:

* Always do a ``git status`` before you commit -- make sure that the stuff you are going to commit is what you want!

  - note that if you do ``git commit`` it will only commit those files listed under "staged for commit". But if you do ``git commit -a`` (-a for all) then it will commit everything modified, i.e. "Changes not staged for commit:".

Note in the status report::

    $ git status
    On branch master
    Your branch is up to date with 'origin/master'.

    Changes not staged for commit:
      (use "git add <file>..." to update what will be committed)
      (use "git checkout -- <file>..." to discard changes in working directory)

        modified:   notes_for_class/source/lesson02.rst

    ...

It even tells you want to do: use ``git add`` to stage particular files, or ``git checkout`` to revert a file back to its state as of the last commit. It doesn't mention ``git commit -a``, but that will commmit everything that is "not staged for commit".

If you are careful before the commit stage, then you won't have to "roll back" changes very often.

But if you do:

https://uwpce-pythoncert.github.io/ProgrammingInPython/topics/01-setting_up/git_hints.html#backing-out-a-change

There are other nifty hints on that page, if you get stuck.



Exercises
=========

