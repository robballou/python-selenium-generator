#
# TextMate command for calling the Selenium test code
#
# Use the selenium test generator to create the JSON data for a form. This
# command will prompt for the URL of the form. If you want to create
# a test case off of the current document, see the 'textmate_create_command.sh'
#
# Install: create a new command and set the values to:
#
#    Save: Nothing
#    Command: (this code)
#    Input: None
#    Output: Insert as Text
#
# Version: 0.1
#
# get URL
res=$(CocoaDialog inputbox --title "Form URL" --informative-text "Please enter the URL for the form:" --button1 "Go" --button2 "Cancel")

# handle the cancel
[[ $(head -n1 <<<"$res") == 2 ]] && exit_discard

# format the URL
url=$(tail -n1 <<<"$res")

python $SELENIUM_GENERATOR/example.py --json $url