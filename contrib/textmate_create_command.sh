#
# TextMate command for calling the Selenium test code
#
# Use the selenium test generator to create a test for a form. This
# command will prompt for the URL of the form. If you want to create
# a test case off of the current document, see the 'textmate_create_command.sh'
#
# Install: create a new command and set the values to:
#
#    Save: Nothing
#    Command: (this code)
#    Input: Entire Document
#    Output: Create New Document
#
# You also need to set $SELENIUM_GENERATOR in your TM preferences (Advanced -> Shell Variables)
# 
# Version: 0.1
#

cat $TM_FILEPATH | python $SELENIUM_GENERATOR/example.py --stdin