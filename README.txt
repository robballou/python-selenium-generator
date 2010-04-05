This is a Python module for creating Selenium test code based on an HTML form.

Selenium currently provides a method for finding all elements on a page, but does not provide adequate access to form-specific elements (e.g, the elements within a form). Also, you must currently specify to fill in everything in a piecemeal.

This module hopes to help by allowing you to create code for the form you want to test on a page (in case there are multiple forms) and to fill in data based on field types.

‘example.py’ Usage
==================
Usage: example.py [options] url

Options:
  -h, --help  show this help message and exit
  -j, --json  Return JSON representation of the form instead of the Selenium
              code
  -m, --html  Return HTML representation of the test instead of the Selenium
              code
  --stdin     Read data from STDIN rather than a URLL

Example:

python-selenium-generator$: python example.py http://example.org/form/
$this->selenium->type('firstName', 'Lorem');
$this->selenium->type('lastName', 'Lorem');

Textmate Commands
=================
There are also several provided Textmate commands (which may work with e text editor as well) that help use this module while in the editor. Note that these commands use $SELENIUM_GENERATOR to locate where the module is installed.