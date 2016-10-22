#!/usr/bin/python

from SystemConfiguration import SCDynamicStoreCreate, SCDynamicStoreCopyValue

net_config = SCDynamicStoreCreate(None, "net", None, None)

def get_primaryinterface():
    states = SCDynamicStoreCopyValue(net_config, "State:/Network/Global/IPv4")
    return states['PrimaryInterface']

def get_ip_address(iface):
    addresses = SCDynamicStoreCopyValue(net_config, "State:/Network/Interface/%s/IPv4" % iface)
    return addresses['Addresses'][0]

primary_interface = get_primaryinterface()
print (primary_interface, get_ip_address(primary_interface))

print SCDynamicStoreCopyValue(net_config, "State:/Network/Global/IPv4")
print SCDynamicStoreCopyValue(net_config, "State:/Network/Interface")