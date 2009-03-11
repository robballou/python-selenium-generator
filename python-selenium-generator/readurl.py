import urllib2
from BeautifulSoup import BeautifulSoup, Tag
from form import Form

# def get_form_elements(element):
#     # don't pay attention to nav strings
#     try: element.name
#     except AttributeError, e: pass
#     else: 
#         yield element
# 
def get_forms(page):
    data = page.read()
    soup = BeautifulSoup(data)
    forms = soup.findAll('form')
    f = []
    for form in forms:
        this_form = Form()
        this_form.set_attributes(form.attrs)
        for element in form.recursiveChildGenerator():
            try:
                if element.name in ['input', 'select', 'textarea', 'button']:
                    this_form.add_element(element.name, element.attrs, element.string)
            except AttributeError, e:
                pass
        f.append(this_form)
    return f

def get_page(url):
    return urllib2.urlopen(url)