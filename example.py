#!/usr/bin/env python
from python_selenium_generator import readhtml, readurl, is_url, TestGenerator
import optparse
import sys

parser = optparse.OptionParser(usage='usage: %prog [options] url')
parser.add_option('-j', '--json', action='store_true', dest='json', default=False, help="Return JSON representation of the form instead of the Selenium code")
parser.add_option('--stdin', action='store_true', dest='stdin', default=False, help="Read data from STDIN rather than a URL")
(options, args) = parser.parse_args()

if len(args) != 1 and not options.stdin:
    parser.error("Must provide a URL")

if options.stdin:
    page = sys.stdin
    forms = readhtml.get_forms(page)
    for form in forms:
        if not options.json:
            test = TestGenerator(form)
            print test.create()
        else:
            print form.to_json()
elif is_url(args[0]):
    # read web page and generate test
    page = readurl.get_page(args[0])
    forms = readurl.get_forms(page)
    for form in forms:
        if not options.json:
            test = TestGenerator(form)
            print test.create()
        else:
            print form.to_json()
else:
    parser.error("Invalid URL")