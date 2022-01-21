:orphan:

.. _notes_lesson03:

###############################
1/25/2022: Relational Databases
###############################

**NOTES:**

A reminder: everything you need to know should be in the Canvas modules -- or linked from there.
There may be some things missing, but if so , that's an oversight, so do let us know so we can improve the course in the future.

What that means is that I spend class time on "extras" -- more on process, and style, and detail, not things like: "how to write a logging message".

And a lot of this is inspired by what we learn when reviewing your work and answering your questions. When we see sticking points, confusions, etc -- I"ll try to address those in class, rather than the basics of how to do new things.

So I may not seem to be talking much about the topic of the week -- but **do** try to talk about what you really need to know to become better Python programmers.


With that in mind...

Notes from homework review:
---------------------------

(Names have been omitted to protect the innocent)

You don't need to type check:
.............................

I saw some code in some of your submissions that looked like this:

::

    try:
        assert isinstance(user_collection, users.UserCollection)
    except AssertionError:
        print('user_collection argument is not a users.UserCollection.')
        return False

You really don't need to be type checking your inputs like that. The rule of thumb is that you don't care if it's particular type, you care if it works :-)

And this doesn't raise an error, it simply returns False. If the caller has called the function improperly, why do we think it's going to handle the False return properly? An Exception do to improper calling of the function should absolutely rise to up the call stack!

Also -- assertions are for testing -- if you really do need to check something for a type, a plain old:

::

    if not isinstance(user_collection, users.UserCollection):
        raise TypeError('user_collection argument is not a users.UserCollection.')

is more straight forward.

**Side Note**

When I say "assertions are for testing" I mean that quite strictly. In fact, when Python is run in "optimized" mode, assertions are ignored completely.

So I use a style (based on the the idea of complete testing) where I only use assertions in dedicated tests, as we have been.

However, there is a style where some assertions are put directly in the code. The idea is that particularly in programs that interact a lot with external systems, you want to be able to run the entire application in "test mode", with assertions turned on, to catch integration errors.

I have zero experience with that, so can't really advise you on it -- but I can suggest that even in that case, the checks should be at the "boundaries" of the code -- where is is being called by external, not-being-tested-by-you, code.

And for this class, keep your asserts in your tests.



Don't check for strings for filenames!
--------------------------------------

::

    try:
        assert isinstance(filename, str)
    except AssertionError:
        print('filename must be a string.')
        return False

Remember: Python is "Duck Typed" -- we don't care if the filename is a string, all we care is that it can be used to open a file.
And in fact, in recent versions, all the Python standard library functions (like ``open()``) can take *either* a string *or* a ``Path`` object.
So this code is actually preventing a perfectly reasonable use!

If you do need a string path (for instance, to save it in a file, or pass it to a non-python system), you can use the ``os.fspath`` function to make a string path our of anything that is supported by the propocol.

pylint hint
-----------

A number of folks (Including me) used a few short names in places where it made sense -- particually the tests. But pylint doesn't like that.

Kelton found a nice solution: Putting this in a ``.pylintrc`` file:

::
    [BASIC]

    # Good variable names which should always be accepted, separated by a comma.
    good-names=df,uc,u,us

nice find!


Another important note on testing
.................................

The goal of testing is to make sure that your code is working as it should.


Relevant Tangent:
.................

"Pure" functions and "Side Effects"

All functions take zero or more parameters, and

 1) Return values
 and / or
 2) Change something in the system

Functions that only return values are sometimes called "pure" functions.

Functions that change something in the system are said to have "side effects"

Simple Pure function:

.. code-block:: python

    def mult(a, b):
        return a * b

This is an (admittedly trivial) pure function -- it does not alter a or b, and does not change anything else in the system. It will only have an impact at all if the return value is used for something:

.. code-block:: python

    x = mult(a, b)

The nice thing about pure functions is that you don't have to know anything about what's in them to know what will happen when you run that line of code -- only the value of x will be affected.

Functions with side effects ("impure" functions?) on the other hand, will make something happen *inside* the function, and you need to read the documentation to know what that is.

Simple function with side effects:

.. code-block::  python

  print("this")

Think about it -- what does ``print`` do? It writes what you ask it to write to standard output (``sys.stdout``). That's it. So it alters the system, but you have no way of knowing how the system is altered by looking at the code where it is called. We all know what print does, so it's generally not problematic, but what if there's this line of code elsewhere in the program:

.. code-block:: python

  sys.stdout = open('temp_output.txt', 'w', encoding='utf-8')

Now what will ``print()`` do?

Let's check that out. In the class repo:

``Examples/lesson03/redirect.py``

The point here is that when you look at even a simple print() statement, you can't know for sure what's going to happen.

"types" of side effects:
........................

I'm not sure there are clear definitions here, but you can group side effects into three categories:

System Effects:

    That would be like ``print()`` -- something changes in the system somewhere, you need to know what the function does to know what.

Methods on mutable classes:

    Mutable classes often have methods that change the instance itself. e.g.:

    ``list.sort()``

    In that case, the list is sorted in place, as a "side effect" of the function call. But it doesn't change anything else -- only the instance you called it on, so that's pretty clear in the code.

    And it's a Python convention for such mutating methods to return None, so that's it's clear that it's a mutating method. If you do:

    ``sorted_list = a_list.sort()``

    You will get a ``None``, and it will be really obvious that that isn't what you wanted to do.

    Contrast this with non-mutating methods, like:

    ``list.copy()`` which returns a new list, and has not altered the original.

Functions that alter passed in arguments:

    This is a case where you pass a mutable object into a function and, and that function alters the actual object passed in. For example:

.. code-block:: python

    def cap_names(user_info):
        """
        Properly capitalize the names in user_info dict

        The user_info dict is altered in place, and None is returned.
        """
        for k in {'first_name', 'last_name', 'middle_name'}:
            user_info[k] = user_info[k].capitalize()

``Examples/lesson03/mutating.py``

These can be more confusing, because it's not clear without reading the documentation what might get altered. Not too bad in this example, but when a function has multiple arguments, it can be confusing.

NOTE: One thing that helps in Python is immutable types. If you pass an immutable in to a function, you know for sure that it won't be altered.

Back to testing:
----------------

Why did I take you on that fascinating side tangent now?

Think a bit about testing:

Pure functions are pretty easy to test: make sure they return what they are expected to return. You may need to test a variety of input, but it's still clear what to look for as a result.

Functions with side effects, on the other hand, can be a lot harder to test.

It can be hard to figure out what you expect the side effect to be, and it can be hard to actually test that side effect.

In the system we are building here -- many of the function are impure, so you need to think carefully about how to test them.

The simplest case:

A Pure Function:

search_user

A Mutated Argument:

Many of them fall into this category -- e.g. a UserCollection is passed in, and it may be altered in some way.

System Side Effect:

The `save_users()` function saves the contents of a UserCollection to a file. So it returns only a success flag, and does not alter the passed-in UserCollection.

What is does do is create a new CSV file. So that's a system side effect. So how do you test it?

Well, first, you do need to test that it is successful and unsuccessful when it should be -- that's straightforward.

Second, you want to test that it actually created the file correctly. Perhaps:

.. code-block::python

    result = main.save_users(filename, uc)

    assert result is True
    assert filename.is_file()

But you also want to know that the contents of the file is correct. In this case, that's not too hard, as we also have code to read the file.

.. code-block::python

    def test_save_users_correct(self):
        """
        make sure the file was written correctly
        """
        # reload it to see if it worked
        # this is tough -- as this test depends on the load_users
        # working. You could look at the generated csv file.

        uc = self.full_user_collection

        filename = HERE / "temp_accounts.csv"
        result = main.save_users(filename, uc)

        uc = self.empty_user_collection
        main.load_users(filename, uc)

        uid = 'bwinkle678'
        assert main.search_user(uid, uc).user_id == uid

If you don't have code to read and validate the output, then it's tricker -- you could open the file and validate the contents directly.

Or, perhaps niftier, you could mock the ``open()`` function so the the file gets written to memory, and you can look at that.


Break Time!
===========

10min break:



Break Time!
===========

10min break


