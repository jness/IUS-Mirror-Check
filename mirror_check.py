#!/usr/bin/env python
import urllib2
import sys
from configobj import ConfigObj
from googlevoice import Voice

def sms(text):
    '''Connect to Google Voice API and send SMS message'''
    # Connect to Google API
    voice = Voice()
    voice.login(email='', passwd='') # Fill me in with your Google Voice info
    phoneNumber = []   # Fill me in with Phone Number

    # Send the SMS
    for number in phoneNumber:
        voice.send_sms(number, text)
    return

def has_alerted():
    '''Check if we have already alerted via SMS'''
    c = ConfigObj('.sms_status')
    try:
        alerted = c['alerted']
    except KeyError:
        c['alerted'] = False
        c.write()
        alerted = c['alerted']
    return alerted

def set_alerted(status):
    '''Set the value of .sms_status'''
    c = ConfigObj('.sms_status')
    c['alerted'] = status
    c.write()
    return

# Make URL Request
try:
    link = '' # Fill me in with URL to check
    req = urllib2.urlopen(link)

except urllib2.HTTPError as e:
    results = 'Offline'

except urllib2.URLError as e:
    results = 'Offline'

else:
    response = req.read()

    # Check the status of request
    if 'dMirr Status: OK' in response: 
        results = 'Online'
    else:
        results = 'Offline'

# If results was offline send a SMS
if results == 'Offline':
    if has_alerted() == 'False':
        print 'Sending SMS'
        sms('dMirr Health Check Fail')
        set_alerted(True)
else:
    print 'Check Passed'
    set_alerted(False)
