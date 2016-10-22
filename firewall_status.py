#!/usr/bin/python

from Foundation import CFPreferencesCopyAppValue

plist = '/Library/Preferences/com.apple.alf.plist'
fw_status = CFPreferencesCopyAppValue('globalstate', plist)

print fw_status
