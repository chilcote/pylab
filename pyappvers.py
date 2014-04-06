#!/usr/bin/env python

'''
This script returns the version of the specified Application

usage:
	./pyappvers.py "VMware Fusion"

Documentation:
https://developer.apple.com/library/mac/documentation/CoreFoundation/Reference/CFPreferencesUtils/Reference/reference.html
'''

##############################################################################
# Copyright 2014 Joseph Chilcote
# 
#  Licensed under the Apache License, Version 2.0 (the "License"); you may not
#  use this file except in compliance with the License. You may obtain a copy
#  of the License at  
# 
#       http://www.apache.org/licenses/LICENSE-2.0
# 
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
##############################################################################

import os, sys, glob, re
from CoreFoundation import CFPreferencesCopyAppValue

DEBUG = False
app_list = []
app_list.extend(glob.glob('/Applications/' '*.app'))
app_list.extend(glob.glob('/Applications/*/' '*.app'))
app_list.extend(glob.glob('/Users/*/Applications/' '*.app'))

def usage():
	print 'Usage: ./pyappvers.py APPLICATION'

def debug(name, path, plist, version):
	print app_list
	print "Application name: %s" % name
	print 'Application path: %s' % path
	print 'Info.plist path: %s' % plist
	print 'Version: %s' % version

def main():
	app_path = ''
	if not len(sys.argv) == 2:
		usage()
		sys.exit(0)
	app_name = sys.argv[1] + '.app'
	for app in app_list:
		if app_name in app:
			app_path = app
	if not os.path.exists(app_path):
		print "Can't find that application!"
		sys.exit(0)
	plist = os.path.join(app_path, 'Contents/Info.plist')
	if not os.path.exists(plist):
		print "Can't find the Info.plist!"
		sys.exit(0)
	version = CFPreferencesCopyAppValue('CFBundleShortVersionString', plist)
	if not version:
		print "No version information found!"
		sys.exit(0)
	if not DEBUG:
		print version
		sys.exit(0)
	debug(app_name, app_path, plist, version)

if __name__ == "__main__":
	main()
