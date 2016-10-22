#!/usr/bin/python

'''
Started on this script and then like a day later Jamf released a similar script
which does most of what I wanted so I shamelessly raided it:
https://github.com/jamfit/Current-User-Password-Age/blob/master/Current-User-Password-Age.py
'''

import os
import sys
import subprocess
import plistlib
import datetime
from SystemConfiguration import SCDynamicStoreCopyConsoleUser

def get_date_changed(username, creation_date=None):
    '''Gets the date of last password change'''
    # return None
    # for 10.10+ or non-migrated accounts
    task = subprocess.check_output(['/usr/bin/dscl', '.', 'read', 'Users/' + username, 'accountPolicyData'])
    plist = plistlib.readPlistFromString('\n'.join(task.split()[1:]))
    if 'creationTime' in plist.keys():
        creation_date = datetime.datetime.utcfromtimestamp(plist['creationTime']).date()
    if 'passwordLastSetTime' in plist.keys():
        return datetime.datetime.utcfromtimestamp(plist['passwordLastSetTime']).date()
    else:
        # for 10.9.x and lower, or migrated accounts
        task = subprocess.Popen(['/usr/bin/dscl', '.', 'read', 'Users/' + username, 'PasswordPolicyOptions'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        (out, err) = task.communicate()
        if not err:
            plist = plistlib.readPlistFromString('\n'.join(out.split()[1:]))
            if 'passwordLastSetTime' in plist.keys():
                return plist['passwordLastSetTime'].date()
    return creation_date

def main():
    username = SCDynamicStoreCopyConsoleUser(None, None, None)[0]
    # username = 'luser'
    if username:
        changed = get_date_changed(username)
        if changed:
            today = datetime.datetime.utcnow().date()
            pw_age = (today - changed).days
            print pw_age
        else:
            print 'Undetermined'

if __name__ == '__main__':
    main()
