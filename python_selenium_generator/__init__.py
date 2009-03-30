"""
Module for creating Selenium test code based on an HTML form

Selenium currently provides a method for finding all elements on a page,
but does not provide adequate access to form-specific elements (e.g, the 
elements within a form). Also, you must currently specify to fill in everything
in a piecemeal.

This module hopes to help by allowing you to create code for the form you want
to test on a page (in case there are multiple forms) and to fill in data based on
field types.

Todo:

- Include the form element's label info in the FormElement object so that behavior can
also change depending on the attributes of the label (class=required, etc.)

Dependecies:

- BeautifulSoup for URL functionality
- simplejson or Python 2.6 for JSON functionality

"""
__author__ = 'Rob Ballou (rob.ballou@gmail.com)'
__version__ = '0.1'
__license__ = 'MIT'

import optparse
import re
import readurl
import readhtml

class TestGenerator(object):
    """
    Basic TestGenerator class
    
    Currently generates PHP-friendly test code, but can be extended to change either
    the code that is generated for other languages or to change the behavior of some of
    form fulliment code.
    
    """
    def __init__(self, form, tester='$this->selenium->'):
        self.form = form
        self.tester = tester
    
    def build_command(self, action, target, value=None):
        # update the value field if necessary
        if value:
            value = ", '%s'" % value.replace("'", "\'")
        else:
            # if there is no value, we don't want to insert that into the command
            value = ""
        return "%s%s('%s'%s)%s" % (self.get_tester(), action, target, value, self.end_command())
    
    def check_input(self, element):
        """
        Check this checkbox on the form.
        
        By default, this will check all checkboxes in the form.
        
        """
        return self.build_command('check', element.attrs['id'])

    def create(self):
        """
        Create the test code
        
        """
        test = ""
        for e in self.form.elements:
            this_test = ""
            if (e.tag == 'input' and e.attrs['type'] == 'text') or e.tag == 'textarea':
                if e.attrs['name'].count('email') > 0:
                    this_test = self.fill_email(e)
                else:
                    this_test = self.fill_text(e)
            elif e.tag == 'input' and e.attrs['type'] == 'checkbox':
                this_test = self.check_input(e)
            elif e.tag == 'select':
                this_test = self.select_option(e)
            if this_test:
                test = "%s%s\n" % (test, this_test)
        return test.strip()
    
    def end_command(self):
        """
        Used to append a common string to the end of commands used in the 
        fulliment methods
        
        """
        return ";"
    
    def fill_email(self, element):
        """
        Places an example email value in the form
        
        This method is trigged when 'email' is present in the text input element's name attribute.
        
        """
        return self.fill_text(element, value='example@example.org')

    def fill_text(self, element, value='Lorem'):
        """
        Insert a value into the text field
        
        """
        return self.build_command('type', element.attrs['id'], value)
    
    def get_tester(self):
        """
        Provide the value for the 'tester' or the selenium object in the code to be generated.
        
        """
        return self.tester
    
    def select_option(self, element):
        """
        Choose an option in a select box
        
        By default this will select the first option that has a value that is not empty
        """
        return self.build_command('select', element.attrs['id'], 'value=regexp:.+')
    
class HTMLGenerator(TestGenerator):
    def build_command(self, action, target, value=None):
        if not value:
            value = ''
        return "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (action, target, value)
    
    def create(self, url=""):
        if url:
            url = """<link rel="selenium.base" href="%s" />""" % url
        test = super(HTMLGenerator, self).create()
        html = """<?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
        <head profile="http://selenium-ide.openqa.org/profiles/test-case">
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <title>simple</title>
        %s
        </head>
        <body>
        <table cellpadding="1" cellspacing="1" border="1">
        <thead>
        <tr><td rowspan="1" colspan="3">simple</td></tr>
        </thead><tbody>
        %s</tbody></table>
        </body>
        </html>""" % (url, test)
        return '\n'.join([line.strip() for line in html.splitlines()])

def is_url(str):
    """
    Determines if the string is an HTTP URL.
    
    """
    if re.match(r'https?://(.+)', str):
        return True
    return False

if __name__ == '__main__':
    # provide some basic functionality to the module
    parser = optparse.OptionParser()
    parser.add_option('-j', '--json', action='store_true', dest='json', default=False)
    (options, args) = parser.parse_args()
    
    if is_url(args[0]):
        # read web page and generate test
        page = readurl.get_page(args[0])
        forms = readurl.get_forms(page)
        for form in forms:
            if not options.json:
                test = TestGenerator(form)
                print test.create()
            else:
                print form.to_json()
