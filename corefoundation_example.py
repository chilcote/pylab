#!/usr/bin/python
#ref: https://macmule.com/2016/12/11/profiles-an-it-admins-best-friend/#more-2645

from CoreFoundation import (
        CFPreferencesCopyAppValue,
        CFPreferencesAppValueIsForced
        )

domain = 'com.apple.appstore'
key = 'restrict-store-require-admin-to-install'

key_value = CFPreferencesCopyAppValue(key, domain)
print 'Key Value: %s' % key_value

key_forced = CFPreferencesAppValueIsForced(key, domain)
print 'Key Forced: %s' % key_forced

