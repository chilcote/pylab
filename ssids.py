#!/usr/bin/python

import subprocess, plistlib, re

d = {}
cmd = ['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-s']
output = re.sub(' +',' ', subprocess.check_output(cmd))
l = []
for line in output.splitlines():
    print len(line.strip().split(' '))
    print line.strip().split(' ')
    offset = len(line.strip().split(' ')) - 7
    if offset:
        print offset
