#!/usr/bin/env python

import subprocess, socket

ip = subprocess.check_output(['/usr/sbin/ipconfig', 'getifaddr', 'en0']).strip()
output = subprocess.check_output(['/sbin/ifconfig', 'en0'])
for line in output.splitlines():
    if ip in line:
        netmask = line.split(' ')[3].lower()

count = int(0)
count+=int(netmask.count('f')) * 4
count+=int(netmask.count('e')) * 3
count+=int(netmask.count('c')) * 2
count+=int(netmask.count('8')) * 1
print '%s.%s/%s' % ('.'.join(ip.split('.')[0:3]), '0', count)
