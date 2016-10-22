#!/usr/bin/env python

import sys, subprocess, socket

locations = {
    '172.31.99.0/23': 'Starbucks',
    '172.20.10.0/28': 'Tullys'
}

def get_activenetwork():
    '''Returns the active network interface of the Mac'''
    output = subprocess.check_output(['/usr/sbin/netstat', '-rn'])
    for line in output.splitlines():
        if 'default' in line and not 'utun' in line:
            return line.split(' ')[-1].strip()

def get_cidr(activenetwork):
    '''Returns the cidr of the current network'''
    try:
        ip = subprocess.check_output(['/usr/sbin/ipconfig', 'getifaddr',
                                    activenetwork]).strip()
    except subprocess.CalledProcessError:
        print 'Cannot determine IP Address'
        sys.exit(1)
    output = subprocess.check_output(['/sbin/ifconfig', activenetwork])
    for line in output.splitlines():
        if ip in line:
            netmask = line.split(' ')[3].lower()

    count = int(0)
    count+=int(netmask.count('f')) * 4
    count+=int(netmask.count('e')) * 3
    count+=int(netmask.count('c')) * 2
    count+=int(netmask.count('8')) * 1
    return '%s.%s/%s' % ('.'.join(ip.split('.')[0:3]), '0', count)

def ip_in_cidrs(cidr, d):
    '''Returns whether the current IP is in a tracked cidr'''
    if cidr in d.keys(): return True

def my_location(cidr, d):
    for k, v in d.items():
        if cidr == k:
            return v

def main():
    if get_activenetwork():
        my_cidr = get_cidr(get_activenetwork())
        print True if ip_in_cidrs(my_cidr, locations) else False
        print my_location(my_cidr, locations)

if __name__ == "__main__":
    main()
