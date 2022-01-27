###############################
gitHub actions/workflows and CI
###############################


In this class, we are using the "gitHub actions" Continuous Integration (CI) system to check your code when it is pushed to gitHub.

Whenever you push your assignments to gitHub, the "actions" will run, and if they don't all pass, you will get an email from gitHub about it.

In some cases, even if you're code is perfect, it will still fail.
That's because it's set up in a very generic way: lint all .py files, run all tests, expect 100% test coverage, and don't require any non-standard modules.

The fact is that CI scripts are always customized to the project. And we don't know, when we set up the CI, what exactly your project is going to need.

But there may always be some customizing required.

The CI should be set up to be easy to customize.

### The CI configuration:

gitHub actions looks for CI configuration in:

`.github/workflows/`

In there, if there is a `*.yml` file, github will look in there for defined actions. (`*.yml` uses the Yet Another Markup Language (YAML) format -- google for details, but it's pretty easy to read).


There is an example of how I updated mine in the class repo:

Examples/lesson03/pylint.yaml
