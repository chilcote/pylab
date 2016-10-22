#!/usr/bin/env python

import os
import sys
import subprocess
import plistlib

def get_ioreg():
    '''Returns a dict of all ioreg data'''
    cmd = ['/usr/sbin/ioreg', '-c', 'IOPlatformExpertDevice', '-d', '2', '-a']
    task = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
    (out, err) = task.communicate()
    plist = plistlib.readPlistFromString(out)
    return plist

def main():
    d = get_ioreg()
    # print d['IOPlatformSerialNumber']
    # print type(d['IORegistryEntryChildren'])
    print len(d['IORegistryEntryChildren'])
    for k, v in d['IORegistryEntryChildren'][0].items():
        print k, v
    print d['IORegistryEntryChildren'][0]['IOPlatformSerialNumber']

if __name__ == "__main__":
    main()
