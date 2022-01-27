###############################
gitHub actions/workflows and CI
###############################

In this class, we are using the "gitHub actions" Continuous Integration (CI) system to check your code when it is pushed to gitHub.

Whenever you push your assignments to gitHub, the "actions" will run, and if they don't all pass, you will get an email from gitHub about it.

In some cases, even if you're code is perfect, it will still fail.
That's because it's set up in a very generic way: lint all .py files, run all tests, expect 100% test coverage, and don't require any non-standard modules.

The fact is that CI scripts generally need to be customized to the project. And we don't know, when we set up the CI, what exactly your project is going to need. So there may always be some customizing required.

The CI should be set up to be easy to customize.


The CI configuration:
=====================

gitHub actions looks for configuration in:

``.github/workflows/``

In there, if there is a ``*.yml`` file, github will look in there for defined actions. (``*.yml`` uses the **Y** AML **A** in't **M** arkup **L** anguage (YAML) format -- google for details, but it's pretty easy to read).

The YAML files specify various jobs that can be run when certain actions occur -- for instance, whenever someone pushes to the repo.

Files used for assignment repos:
--------------------------------

These are the files used for the class setup.
(if your assignment repo doesn't have these, you can add them by hand)

They can be found in the class repo here:

``Examples/gitHub_Actions``

``code_checks.yml``:

    This is the main YAML file that defines the gitHub actions. it should be in the ``.github/workflows`` dir in the repo.

``requirements.txt``:

    This is where you specify what non-standard libraries your project needs, e.g. pandas, loguru, peewee, ...
    See: `<https://pip.pypa.io/en/stable/reference/requirements-file-format/>`_

``.coveragerc``

    This is where you can configure how coverage is run -- in particular you can specify files to exclude. See: `<https://coverage.readthedocs.io/en/latest/config.html>`_

They can be found in the class repo here:

``Examples/gitHub_Actions``


The ``code_checks.yml`` file
----------------------------

Here is an annotated version of the workflow file:

.. code-block:: yaml

    name: CodeChecks

    # this says that this job willbe run when the repo is pushed to
    on: [push]

    jobs:
      check:  # this is the check job.
        runs-on: ubuntu-latest  # uses Ubuntu Linux

        strategy:
          matrix:  # you can run the job on multiple versions
                   # of Python -- good for testing libraries
            python-version: ["3.10"]

        steps:  # each steo to do
        - uses: actions/checkout@v2  # this checks out the repo

        - name: Set up Python ${{ matrix.python-version }}
          uses: actions/setup-python@v2  # gets python itself installed
          with:
            python-version: ${{ matrix.python-version }}

        - name: Install dependencies
          run: |
            python -m pip install --upgrade pip
            # core packages needed for testing
            pip install pylint pytest pytest-cov
            # extra requirements for this project
            # anything you add to the requirements.txt file will get installed
            pip install -r requirements.txt

        - name: Analyzing the code with pylint
          if: always()
          run: |  # runs pylint on all Python files in the repo
            pylint `ls -R|grep .py$|xargs`

        - name: Run tests
          if: always()  # runs even if pylint "failed"
          run: |
            pytest ./  # pytest will search for everything that looks like a test

        - name: Run test coverage
          if: always()  # run even if some of the tests failed
          run: |  # runs all tests, passes if 100% coverage is achieved
                  # coverage can be configured in the .coveragerc file
            pytest --cov --cov-fail-under=100 ./


