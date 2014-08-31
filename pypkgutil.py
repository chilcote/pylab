#!/usr/bin/env python

'''
This script collects data from pkgutil --pkgs
Yes, everything in this script can be done in the shell with the pkgutil
command, but I wanted to play with python.  Sue me.
Inspiration came from a twitter from bruienne linking to this gist:
https://gist.github.com/bruienne/3fd12e07421ac875e747
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

'''
todo:
add a search function
add a forget function
add a function to pull plist of specified pkgs

'''

import os, sys, subprocess
import plistlib


def get_data():
    l = []
    cmd = ['pkgutil', '--pkgs']
    task = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE)
    (out, err) = task.communicate()
    for line in out.splitlines():
        l.append(line)
    return l

def usage():
    return './pypkgutil.py [KEY]'

def main():
    pkgs = get_data()
    if len(sys.argv) == 1:
        for i in pkgs:
            print i
    elif len(sys.argv) == 2:
        for i in pkgs:
            if sys.argv[1].lower() in i.lower():
                print i
    else:
        print usage()
        sys.exit(0)

if __name__ == "__main__":
    main()

