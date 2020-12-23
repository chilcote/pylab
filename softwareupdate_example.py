#!/usr/bin/python

from CoreFoundation import (
        CFPreferencesCopyAppValue,
        CFPreferencesAppValueIsForced
        )

domain = '/Library/Preferences/com.apple.SoftwareUpdate'
key = 'AutomaticCheckEnabled'

key_value = CFPreferencesCopyAppValue(key, domain)
print 'Key Value: %s' % key_value

key_forced = CFPreferencesAppValueIsForced(key, domain)
print 'Key Forced: %s' % key_forced

