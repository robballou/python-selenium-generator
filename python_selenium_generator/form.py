try: import json
except ImportError, e: import simplejson as json

class SetAttributes(object):
    def __init__(self):
        self.attrs = {}
    
    def set_attributes(self, attrs):
        for attr in attrs:
            self.attrs[attr[0]] = attr[1]
    
class Form(SetAttributes):
    def __init__(self):
        super(Form, self).__init__()
        self.elements = []
        pass
    
    def add_element(self, tag, attrs, value):
        self.elements.append(FormElement(tag, attrs, value))
    
    def to_json(self):
        obj = {
            'attributes':self.attrs, 
            'elements': []
        }
        for element in self.elements:
            obj['elements'].append(element.to_json())
        return json.dumps(obj)
    

class FormElement(SetAttributes):
    def __init__(self, tag, attrs, value):
        super(FormElement, self).__init__()
        self.tag = tag
        self.set_attributes(attrs)
        self.value = value
    
    def __repr__(self):
        return self.tag
    
    def to_json(self):
        return {'tag': self.tag, 'attributes': self.attrs, 'value': self.value}