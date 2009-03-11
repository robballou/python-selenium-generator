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
__version__ = '0.1a'
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
    form fulliment code
    
    """
    def __init__(self, form, tester='$this->selenium->'):
        self.form = form
        self.tester = tester
    
    def check_input(self, element):
        return "%scheck('%s');" % (self.get_tester(), element.attrs['id'])

    def create(self):
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
    
    def fill_email(self, element):
        return self.fill_text(element, value='example@example.org')

    def fill_text(self, element, value='Lorem'):
        return "%stype('%s', '%s');" % (self.get_tester(), element.attrs['id'], value.replace("'", "\'"))
    
    def get_tester(self):
        return self.tester
    
    def select_option(self, element):
        return "%sselect('%s', 'value=regexp:.+');" % (self.get_tester(), element.attrs['id'])
    

def is_url(str):
    if re.match(r'https?://(.+)', str):
        return True
    return False

if __name__ == '__main__':
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
