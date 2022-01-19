.. _testing_hints:


##########################
Chris' Handy Testing Hints
##########################

Here you will find some handy hints for writing and debugging tests (and your code), with a focus on TDD.

Test Driven Development (TDD)
=============================

It's been said many times, but I'll say it again:

TDD essentially means that you write the tests before the code.

It's that simple.

But besides all the other "official" benefits, I find I can be productive for this reason:

  You need to run your code somehow in order to see if it works, even for simple things like syntax errors.

And running the code requires a bit of code-to-run-the-code anyway -- why not make them unit tests?

Before I discovered TDD, I would write a little script that would run the function I was working on. Once it worked, I'd edit that script to try out some other aspect of the code -- e.g. what if I passed in an invalid value? TDD is pretty much the same -- except that *all the tests are saved* so you know you when you break something in the future.

The other alternative to TDD is to run the entire application over an over each time to make a change. Personally, that drives me *BONKERS* -- I don't want to point and click my way through the whole app in order to see if one little change worked. And for anything but the most microscopic app (like the ones we do for classes like this), there are how many paths through the app to test?

Anyway -- on to TDD:

Chris' Unit Testing Hints
-------------------------

Write as you go:
................

When folks talk about TDD, it sounds like you are supposed to write the entire test suite before you start writing any real code. And maybe some people to that. But I write one test at a time. This is helpful, because debugging dozens of test failures all at once is a nightmare. Also, you don't really know if your test are correct until they do something real.

So what I do is:

For a single aspect of the unit being tested:
 * Write a single test
 * Run the test, and watch it fail (usually)
 * Write or fix the code until the tests passes
 * On to the next feature!

Make sure a new test fails
--------------------------

When you write a new test -- make sure that it fails at least once -- it's the only way to assure that (a) the test is being run, and (b) that it actually tests something -- hopefully what you want it to test!

Force a failure
----------------

While you are debugging the code (or the tests) it sometimes helpful to force a failure: put an ``assert False`` at the end of the test. That way pytest will not swallow any output from print statements, etc. and you can "print-debug" away.

Run just the tests you are working on
-------------------------------------

If you have a lot of tests, and are only working on one, you can sub-select with``pytest``.

The test in only file: simply pass in the filename: ::

    pytest test_simple.py

One test in a file: pass (part of) the name of the test with the ``-k`` flag:

    pytest -k reverse_sort test_simple.py

Note: you can pass in an expression for fancier selection. See the ``pytest`` docs.

(you can also comment out the tests you're not working on at the moment -- but don't forget to undo that!)

Don't put too many tests on one file
------------------------------------

You really don't want too much in one test file. As a project gets big, it gets quite unwieldy. I tend to do one test file per python module -- and use the name of the file with the ``test_`` prefix.

Make sure you actually made a new test!
---------------------------------------

It's pretty common practice to copy and paste a previous test to make a new one -- saves retyping boiler plate code. But don't forget to change the name! It's a good idea to look at the number of tests in the test report to makes sure that there's one more when you create one more.

Use data files sparingly
------------------------

Sometimes you need some data to "feed" a test.
If possible, and practical, try to have the test code create that data on the fly -- ideally in a fixture or utility function.
That puts all the information in one place, and assures that your tests stay in sync with your test data.

Make sure your data files can be found
--------------------------------------

If you do need data files, commit them to the repo, and use relative paths to get them. Here's some handy hints for how to do that:

.. code-block:: python


    # gets the dir that this test file is in.
    HERE = Path(__file__).parent

    # path to a "good" accounts file
    good_account_file = HERE / "accounts.csv"


Now you can use ``good_account_file`` anywhere you need it in your tests.


Build the pieces from the ground up
-----------------------------------

It's often the case that you can't truly test each unit completely separately -- you need some pieces in order to implement others. With TDD -- try to start from the bottom. If you find function A needs function B in order to be written, make sure to write *and test* function B first.

This also means that you should only have one failing test at time -- the one you are working on right then.

Be careful with defaults
------------------------

If you use defaults in your tests, it's very easy to not catch errors, as the actual set value may have been ignored, or used incorrectly, and but if your tests all use defaults, you'd never know that.

Corollary to the previous: vary your test data.
-----------------------------------------------

Vary your test data -- similar to above, if you have, e.g. one small test dateset, and you use it for everything, you may accidentally not be testing things!






