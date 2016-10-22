#!/usr/bin/python
# from salajander in slack

from SystemConfiguration import SCDynamicStoreCreate,\
                                SCDynamicStoreCopyValue,\
                                SCNetworkInterfaceCopyAll,\
                                SCNetworkInterfaceGetBSDName,\
                                SCNetworkInterfaceForceConfigurationRefresh

net_config = SCDynamicStoreCreate(None, "net", None, None)

def update_dhcp(interface):
  interfaces = SCNetworkInterfaceCopyAll()
  for i in interfaces:
    if SCNetworkInterfaceGetBSDName(i) == interface:
      return SCNetworkInterfaceForceConfigurationRefresh(i)
  return False

def get_primaryinterface():
    '''Returns the active network interface of the Mac'''
    try:
        states = SCDynamicStoreCopyValue(net_config, "State:/Network/Global/IPv4")
        return states['PrimaryInterface']
    except TypeError:
        return None

interface = get_primaryinterface()
update_dhcp(interface)
