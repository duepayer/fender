# Fender Product Checkout Test

## Requirements

**Python v2.7**

Python Modules

* [Unittest](https://docs.python.org/2/library/unittest.html) (Standard Library)
* [Selenium Webdriver](http://selenium-python.readthedocs.io/index.html)
* [Nose Test Runner](http://nose.readthedocs.io/en/latest/) (not hard requirement but used to run script and output x-unit result in anticipation of CI integration)

Python Command Line Tools

* [VirtualEnv](https://pypi.python.org/pypi/virtualenv)
* [VirtualEnvWrapper](https://pypi.python.org/pypi/virtualenvwrapper)

> Virtualenv is used to create a separate instance of Python in order to install script dependencies and to avoid clashing with the system Python on Mac OS X & Windows. There is also an excellent plugin available called virtualenvwrapper that provides additional command line tools to make creating, configuring and switching between virtualenvs much easier. These tools will help protect your system from misconfiguration and compatibility issues on your local machine as you work with various Python projects that have different dependencies.


## Installation

1. Create a new Python virtualenv in the **Terminal** using the virtualenvwrapper command ```mkvirtualenv name_of_virtualenv``` This will create and activate the virtualenv we'll use for this project.
2. Pull down the project from GitHub .
3. Navigate to the root **fender** directory. There you'll find a **requirements.txt** file listing the dependencies for this project. 
4. Run `pip install -r requirements.txt` from the Terminal to install the required dependencies.
5. Run `pip freeze` to verify that both **selenium** and **nose** are present in the output.


## Running the script locally

There are two options for running the test script locally. First, make sure that you're in the root **fender** directory. Secondly you can run either of the following commands:

**Basic unittest command**

```
	python test_fender_shop.py
```

**Nose test runner with XML result output for CI integration**

```
	nosetests -v -s --with-x-unit
```

## Refactoring checklist

* Review entire site and create a UML document covering all of the different page and product types and their behaviors.
* Simplify/rethink locator retrieval functionality so that no extraneous locators remain from previous locator dictionary overriding when instantiating a new Page Object.
* Clean up variable names so that page objects read more clearly in test scripts.
* Use more intelligent selenium wait strategy (e.g. waiting until page elements are present on page rather than using `time.sleep` to allow more time for page to load).
* Use API/Database to supply test data dynamically and for verification. 