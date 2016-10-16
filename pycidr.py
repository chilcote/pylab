#!/usr/bin/python

import subprocess
from SystemConfiguration import SCDynamicStoreCreate, SCDynamicStoreCopyValue

def get_interface(net_config):
    '''Returns the active network interface of the Mac'''
    try:
        states = SCDynamicStoreCopyValue(net_config, "State:/Network/Global/IPv4")
        return states['PrimaryInterface']
    except TypeError:
        print TypeError
        exit(1)

def get_ip(net_config, interface):
    '''Returns the IP address of the primary network interface'''
    addresses = SCDynamicStoreCopyValue(net_config, "State:/Network/Interface/%s/IPv4" % interface)
    try:
        return addresses['Addresses'][0]
    except TypeError:
        print TypeError
        exit(1)

def main():
    net_config = SCDynamicStoreCreate(None, "net", None, None)
    print SCDynamicStoreCopyValue(net_config, "State:/Network/Global/DNS")
    interface = get_interface(net_config)
    ip = get_ip(net_config, interface)

    output = subprocess.check_output(['/sbin/ifconfig', interface])
    for line in output.splitlines():
        if ip in line:
            netmask = line.split(' ')[3].lower()

    count = int(0)
    count+=int(netmask.count('f')) * 4
    count+=int(netmask.count('e')) * 3
    count+=int(netmask.count('c')) * 2
    count+=int(netmask.count('8')) * 1

    print '%s.%s/%s' % ('.'.join(ip.split('.')[0:3]), '0', count)

if __name__ == "__main__":
    main()
